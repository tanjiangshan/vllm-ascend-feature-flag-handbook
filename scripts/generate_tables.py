#!/usr/bin/env python3
"""Generate overview tables and JSON exports from data files.

Flags (data/flags/*.yaml):
  1. Validates every YAML entry against a small schema.
  2. Renders the Chinese/English overview tables in docs/flags/index.md(+en).
  3. Generates docs/flags/{key}.md stubs for flags that don't have a
     handwritten page yet.
  4. Emits docs/flags.json (machine-readable export for the community).

Engine args (data/engine-args.yaml):
  5. Validates entries (arg/category/type/desc/sources).
  6. Renders category-grouped tables in docs/engine-args/index.md(+en).
  7. Emits docs/engine-args.json.

Run locally:  python scripts/generate_tables.py
CI runs it and fails if generated files are not committed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "flags"
ENGINE_ARGS_YAML = ROOT / "data" / "engine-args.yaml"
ENGINE_ARGS_DIR = ROOT / "docs" / "engine-args"
ENGINE_ARGS_INDEX_MD = ENGINE_ARGS_DIR / "index.md"
ENGINE_ARGS_INDEX_EN_MD = ENGINE_ARGS_DIR / "index.en.md"
ENGINE_ARGS_JSON = ROOT / "docs" / "engine-args.json"
FLAGS_DIR = ROOT / "docs" / "flags"
INDEX_MD = FLAGS_DIR / "index.md"
INDEX_EN_MD = FLAGS_DIR / "index.en.md"
JSON_OUT = ROOT / "docs" / "flags.json"

TYPES = {"bool", "int", "float", "str", "dict", "list"}
STATUSES = {"active", "deprecated", "removed", "planned"}
HARDWARE = {"A1", "A2", "A3", "A4", "A5"}

CATEGORY_ORDER = [
    "parallel", "cache", "scheduling", "compilation", "model", "speculative",
    "kvtransfer", "multimodal", "serving", "rl",
]
CATEGORY_LABELS = {
    "zh": {
        "parallel": "并行策略", "cache": "KV 缓存与内存", "scheduling": "调度与内存",
        "compilation": "编译与图",
        "model": "模型与加载", "speculative": "投机解码", "kvtransfer": "KV 传输与 PD 分离",
        "multimodal": "多模态", "serving": "服务端", "rl": "RL 训练",
    },
    "en": {
        "parallel": "Parallelism", "cache": "KV Cache & Memory", "scheduling": "Scheduling & Memory",
        "compilation": "Compilation & Graphs",
        "model": "Model & Loading", "speculative": "Speculative Decoding", "kvtransfer": "KV Transfer & PD",
        "multimodal": "Multimodal", "serving": "Server", "rl": "RL Training",
    },
}

S = {
    "zh": {
        "key": "配置键",
        "name": "中文名",
        "type": "类型",
        "default": "默认值",
        "status": "状态",
        "legacy_env": "旧环境变量",
        "versions": "v0.23 / v0.30 / main",
        "hardware": "适用芯片",
        "desc": "说明",
    },
    "en": {
        "key": "Config key",
        "name": "Short name",
        "type": "Type",
        "default": "Default",
        "status": "Status",
        "legacy_env": "Legacy env var",
        "versions": "v0.23 / v0.30 / main",
        "hardware": "Hardware",
        "desc": "Description",
    },
}

STATUS_BADGE = {
    "active": ":white_check_mark:",
    "deprecated": ":warning:",
    "removed": ":x:",
    "planned": ":construction:",
}


def fail(msg: str) -> None:
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(1)


def validate(name: str, entry: dict) -> list[str]:
    """Return a list of validation errors (empty means ok)."""
    errors = []
    required = ("key", "name", "type", "default", "status", "desc", "version_support")
    for field in required:
        if field not in entry:
            errors.append(f"{name}: missing required field '{field}'")

    if entry.get("type") not in TYPES:
        errors.append(f"{name}: type must be one of {sorted(TYPES)}, got {entry.get('type')!r}")
    if entry.get("status") not in STATUSES:
        errors.append(f"{name}: status must be one of {sorted(STATUSES)}, got {entry.get('status')!r}")

    vs = entry.get("version_support")
    if not isinstance(vs, dict) or set(vs) != {"v0.23.0", "v0.30.0", "main"}:
        errors.append(f"{name}: 'version_support' must map exactly {{v0.23.0, v0.30.0, main}} to booleans")

    hw = entry.get("hardware", [])
    if not isinstance(hw, list):
        errors.append(f"{name}: 'hardware' must be a list")
    else:
        unknown = set(hw) - HARDWARE
        if unknown:
            errors.append(f"{name}: unknown hardware values {sorted(unknown)}")

    for list_field in ("models", "requires", "conflicts", "deprecated_in", "removed_in"):
        if list_field in entry and not isinstance(entry[list_field], list):
            errors.append(f"{name}: '{list_field}' must be a list")

    desc = entry.get("desc", {})
    if not isinstance(desc, dict) or "zh" not in desc or "en" not in desc:
        errors.append(f"{name}: 'desc' must be a dict with both 'zh' and 'en' keys")
    short = entry.get("name", {})
    if not isinstance(short, dict) or "zh" not in short or "en" not in short:
        errors.append(f"{name}: 'name' must be a dict with both 'zh' and 'en' keys")

    return errors


def load_flags() -> list[dict]:
    if not DATA_DIR.is_dir():
        fail(f"data directory not found: {DATA_DIR}")

    flags = []
    all_errors = []
    for path in sorted(DATA_DIR.glob("*.yaml")):
        try:
            entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            fail(f"{path.name}: invalid YAML: {exc}")
        if not isinstance(entry, dict):
            fail(f"{path.name}: top-level must be a mapping")
        entry["_file"] = path.name
        all_errors.extend(validate(path.name, entry))
        flags.append(entry)

    if all_errors:
        for e in all_errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    keys = [f["key"] for f in flags]
    if len(keys) != len(set(keys)):
        dup = {k for k in keys if keys.count(k) > 1}
        fail(f"duplicate flag keys: {sorted(dup)}")

    return flags


def render_versions_cell(entry: dict) -> str:
    """Compact ✅/— cell for the three tracked versions."""
    vs = entry.get("version_support", {})
    marks = [":white_check_mark:" if vs.get(v) else "—" for v in ("v0.23.0", "v0.30.0", "main")]
    return " ".join(marks)


def render_default(value) -> str:
    """Render a default value matching official docs style (false/true lowercase)."""
    if value is None:
        return "`None`"
    if isinstance(value, bool):
        return f"`{str(value).lower()}`"
    return f"`{json.dumps(value, ensure_ascii=False)}`"


def render_table(flags: list[dict], lang: str) -> str:
    h = S[lang]
    lines = [
        f"| {h['key']} | {h['name']} | {h['type']} | {h['default']} | {h['status']} | {h['legacy_env']} | {h['versions']} | {h['hardware']} | {h['desc']} |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for f in flags:
        key = f"[`{f['key']}`]({f['key'].replace('_', '-')}.md)"
        legacy = f"`{f['legacy_env']}`" if f.get("legacy_env") else "—"
        hw = ", ".join(f.get("hardware", [])) or "All"
        status = f"{STATUS_BADGE[f['status']]} {f['status']}"
        short = f["name"][lang].replace("|", "\\|")
        desc = f["desc"][lang].replace("|", "\\|")
        lines.append(
            f"| {key} | {short} | `{f['type']}` | {render_default(f['default'])} | {status} | {legacy} | {render_versions_cell(f)} | {hw} | {desc} |"
        )
    return "\n".join(lines)


def render_version_matrix(flags: list[dict], lang: str) -> str:
    """Render the v0.23.0 / v0.30.0 / main support matrix table."""
    if lang == "zh":
        key_h, note_h = "配置键", "备注"
    else:
        key_h, note_h = "Config key", "Note"
    lines = [
        f"| {key_h} | v0.23.0 | v0.30.0 | main | {note_h} |",
        "|---|---|---|---|---|",
    ]
    for f in flags:
        key = f"[`{f['key']}`](flags/{f['key'].replace('_', '-')}.md)"
        vs = f.get("version_support", {})
        cells = "".join(
            f" {':white_check_mark:' if vs.get(v) else '—'} |"
            for v in ("v0.23.0", "v0.30.0", "main")
        )
        note = f.get("version_note", {}).get(lang, "")
        lines.append(f"| {key} |{cells} {note} |")
    return "\n".join(lines)


def update_version_matrix(flags: list[dict]) -> None:
    """Rewrite the support matrix inside docs/version-matrix.md and .en.md."""
    for lang, fname in (("zh", "version-matrix.md"), ("en", "version-matrix.en.md")):
        path = ROOT / "docs" / fname
        if not path.exists():
            print(f"[WARN] {fname} not found, skipping")
            continue
        text = path.read_text(encoding="utf-8")
        start, end = "<!-- MATRIX_START -->", "<!-- MATRIX_END -->"
        if start not in text or end not in text:
            fail(f"matrix markers not found in {fname}")
        pre, rest = text.split(start, 1)
        _, post = rest.split(end, 1)
        table = render_version_matrix(flags, lang)
        path.write_text(f"{pre}{start}\n{table}\n{end}{post}", encoding="utf-8")
        print(f"Updated {fname} ({len(flags)} flags)")


def update_index(flags: list[dict]) -> None:
    zh_table = render_table(flags, "zh")
    en_table = render_table(flags, "en")

    def replace_block(text: str, start_marker: str, end_marker: str, body: str, path: Path) -> str:
        if start_marker not in text or end_marker not in text:
            fail(f"markers not found in {path}: {start_marker} ... {end_marker}")
        pre, rest = text.split(start_marker, 1)
        _, post = rest.split(end_marker, 1)
        return f"{pre}{start_marker}\n{body}\n{end_marker}{post}"

    if not INDEX_MD.exists():
        fail(f"index not found: {INDEX_MD}")
    text = INDEX_MD.read_text(encoding="utf-8")
    text = replace_block(text, "<!-- TABLE_ZH_START -->", "<!-- TABLE_ZH_END -->", zh_table, INDEX_MD)
    INDEX_MD.write_text(text, encoding="utf-8")
    print(f"Updated {INDEX_MD.relative_to(ROOT)} ({len(flags)} flags)")

    if INDEX_EN_MD.exists():
        etext = INDEX_EN_MD.read_text(encoding="utf-8")
        etext = replace_block(etext, "<!-- TABLE_EN_START -->", "<!-- TABLE_EN_END -->", en_table, INDEX_EN_MD)
        INDEX_EN_MD.write_text(etext, encoding="utf-8")
        print(f"Updated {INDEX_EN_MD.relative_to(ROOT)} ({len(flags)} flags)")


def ensure_stubs(flags: list[dict]) -> None:
    """Create a stub page for any flag missing a handwritten doc."""
    created = 0
    for f in flags:
        slug = f["key"].replace("_", "-")
        path = FLAGS_DIR / f"{slug}.md"
        if path.exists():
            continue
        stub = f"""---
title: {f['key']}
---

# `{f['key']}`

> **状态 / Status**: {f['status']} ｜ **类型 / Type**: `{f['type']}` ｜ **默认值 / Default**: `{json.dumps(f['default'], ensure_ascii=False)}`

{f['desc']['zh']}

{f['desc']['en']}

---

*本页为自动生成的占位页，欢迎补充原理、示例与实测数据。见 [贡献指南](../contributing.md)。*

*This page is an auto-generated stub. Contributions welcome — see [Contributing](../contributing.md).*
"""
        path.write_text(stub, encoding="utf-8")
        created += 1
    if created:
        print(f"Created {created} stub page(s) under docs/flags/")


def export_json(flags: list[dict]) -> None:
    clean = [{k: v for k, v in f.items() if not k.startswith("_")} for f in flags]
    JSON_OUT.write_text(
        json.dumps(clean, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {JSON_OUT.relative_to(ROOT)}")


# ---------------- engine args (data/engine-args.yaml) ----------------

EA_REQUIRED = ("arg", "category", "type", "default", "desc", "sources")
EA_CATEGORIES = set(CATEGORY_ORDER)


def validate_engine_args(name: str, entry: dict) -> list[str]:
    errors = []
    for field in EA_REQUIRED:
        if field not in entry:
            errors.append(f"{name}: missing required field '{field}'")
    if entry.get("category") not in EA_CATEGORIES:
        errors.append(f"{name}: category must be one of {sorted(EA_CATEGORIES)}, got {entry.get('category')!r}")
    if not isinstance(entry.get("type"), str) or "|" in entry.get("type", ""):
        errors.append(f"{name}: 'type' must be a simple type string")
    desc = entry.get("desc", {})
    if not isinstance(desc, dict) or "zh" not in desc or "en" not in desc:
        errors.append(f"{name}: 'desc' must be a dict with both 'zh' and 'en' keys")
    if not isinstance(entry.get("sources"), list) or not entry["sources"]:
        errors.append(f"{name}: 'sources' must be a non-empty list")
    arg = entry.get("arg", "")
    if arg and not all(c.isalnum() or c == "-" for c in arg):
        errors.append(f"{name}: 'arg' has invalid characters: {arg!r}")
    return errors


def load_engine_args() -> list[dict]:
    if not ENGINE_ARGS_YAML.exists():
        fail(f"engine args data not found: {ENGINE_ARGS_YAML}")
    data = yaml.safe_load(ENGINE_ARGS_YAML.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("args"), list):
        fail(f"{ENGINE_ARGS_YAML.name}: top level must be a mapping with an 'args' list")
    args = data["args"]
    all_errors = []
    for i, entry in enumerate(args):
        if not isinstance(entry, dict):
            fail(f"{ENGINE_ARGS_YAML.name}: args[{i}] must be a mapping")
        all_errors.extend(validate_engine_args(f"args[{i}]", entry))
    if all_errors:
        for e in all_errors:
            print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    names = [a["arg"] for a in args]
    if len(names) != len(set(names)):
        dup = {n for n in names if names.count(n) > 1}
        fail(f"duplicate engine args: {sorted(dup)}")
    return args


def render_engine_arg_row(entry: dict, lang: str) -> str:
    slug = entry["arg"]
    label = f"`--{entry['arg']}`"
    if entry.get("detail_page"):
        label = f"[`--{entry['arg']}`]({slug}.md)"
    default = render_default(entry["default"])
    desc = entry["desc"][lang].replace("|", "\\|")
    src = f"[docs×{entry.get('doc_count', len(entry['sources']))}]({entry['sources'][0]})"
    return f"| {label} | `{entry['type']}` | {default} | {desc} | {src} |"


def render_engine_tables(entries: list[dict], lang: str) -> str:
    h = {"zh": {"arg": "参数", "type": "类型", "default": "默认值", "desc": "说明", "src": "官方文档出处"},
         "en": {"arg": "Argument", "type": "Type", "default": "Default", "desc": "Description", "src": "Official docs"}}[lang]
    by_cat: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}
    for e in entries:
        by_cat[e["category"]].append(e)
    out = []
    for cat in CATEGORY_ORDER:
        items = by_cat[cat]
        if not items:
            continue
        out.append(f"### {CATEGORY_LABELS[lang][cat]}\n")
        out.append(f"| {h['arg']} | {h['type']} | {h['default']} | {h['desc']} | {h['src']} |")
        out.append("|---|---|---|---|---|")
        for e in items:
            out.append(render_engine_arg_row(e, lang))
        out.append("")
    return "\n".join(out).rstrip()


def update_engine_args_index(entries: list[dict]) -> None:
    for lang, path in (("zh", ENGINE_ARGS_INDEX_MD), ("en", ENGINE_ARGS_INDEX_EN_MD)):
        if not path.exists():
            fail(f"engine args index not found: {path}")
        text = path.read_text(encoding="utf-8")
        start, end = "<!-- EA_TABLE_START -->", "<!-- EA_TABLE_END -->"
        if start not in text or end not in text:
            fail(f"markers not found in {path.name}")
        pre, rest = text.split(start, 1)
        _, post = rest.split(end, 1)
        table = render_engine_tables(entries, lang)
        path.write_text(f"{pre}{start}\n{table}\n{end}{post}", encoding="utf-8")
        print(f"Updated {path.relative_to(ROOT)} ({len(entries)} args)")


def ensure_engine_arg_stubs(entries: list[dict]) -> None:
    """Stub only for args marked detail_page that lack a handwritten page."""
    created = 0
    for e in entries:
        if not e.get("detail_page"):
            continue
        path = ENGINE_ARGS_DIR / f"{e['arg']}.md"
        if path.exists():
            continue
        path.write_text(f"""---
title: {e['arg']}
---

# `--{e['arg']}`

> **类型 / Type**: `{e['type']}` ｜ **默认值 / Default**: `{json.dumps(e['default'], ensure_ascii=False)}`

{e['desc']['zh']}

{e['desc']['en']}

---

*本页为自动生成的占位页，欢迎补充。见 [贡献指南](../contributing.md)。 / Auto-generated stub — contributions welcome.*
""", encoding="utf-8")
        created += 1
    if created:
        print(f"Created {created} engine-arg stub page(s) under docs/engine-args/")


def export_engine_args_json(entries: list[dict]) -> None:
    ENGINE_ARGS_JSON.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Exported {ENGINE_ARGS_JSON.relative_to(ROOT)}")


def main() -> None:
    flags = load_flags()
    update_index(flags)
    update_version_matrix(flags)
    ensure_stubs(flags)
    export_json(flags)
    engine_args = load_engine_args()
    update_engine_args_index(engine_args)
    ensure_engine_arg_stubs(engine_args)
    export_engine_args_json(engine_args)
    print(f"OK: {len(flags)} flag(s), {len(engine_args)} engine arg(s).")


if __name__ == "__main__":
    main()
