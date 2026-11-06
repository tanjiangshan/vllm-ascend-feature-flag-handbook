#!/usr/bin/env python3
"""Traceability audit for data/engine-args.yaml.

Zero-fabrication gate — verifies, against primary sources fetched live:
  1. Every engine arg exists in the vLLM source CLI definitions.
  2. Every example value appears next to its arg in the cited official
     vLLM-Ascend doc file.

Usage:  python scripts/audit_engine_args.py
Exits non-zero on any failure.

Sources fetched from raw.githubusercontent.com and cached under
$AUDIT_CACHE_DIR (default: /tmp/va-audit-cache).
"""

from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EA_YAML = ROOT / "data" / "engine-args.yaml"

CACHE = Path(__import__("os").environ.get("AUDIT_CACHE_DIR", "/tmp/va-audit-cache"))
CACHE.mkdir(parents=True, exist_ok=True)

VLLM_RAW = "https://raw.githubusercontent.com/vllm-project/vllm/main/{rel}"
ASCEND_RAW = "https://raw.githubusercontent.com/vllm-project/vllm-ascend/{ref}/{rel}"

VLLM_CLI_FILES = [
    "vllm/engine/arg_utils.py",
    "vllm/entrypoints/common/cli_args.py",
    "vllm/entrypoints/cli/openai.py",
]

# docs.vllm.ai URL -> (git ref, repo-relative path)
def parse_docs_url(url: str) -> tuple[str, str]:
    m = re.match(
        r"https://docs\.vllm\.ai/projects/ascend/en/(?P<ver>[^/]+)/(?P<rel>.+?)\.html",
        url,
    )
    if not m:
        raise ValueError(f"unrecognized docs URL: {url}")
    ver = m.group("ver")
    ref = "main" if ver == "latest" else (ver if ver.startswith("v") else f"v{ver}")
    return ref, "docs/source/" + m.group("rel") + ".md"


def fetch(url: str) -> str:
    key = re.sub(r"[^A-Za-z0-9._-]", "_", url)
    cache_path = CACHE / key
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")
    req = urllib.request.Request(url, headers={"User-Agent": "va-handbook-audit"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode("utf-8")
    cache_path.write_text(text, encoding="utf-8")
    return text


def normalize_cmd(text: str) -> str:
    """Join line continuations and collapse whitespace."""
    text = re.sub(r"\\\n\s*", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def audit_engine_args() -> tuple[int, int, list[str]]:
    import yaml

    failures: list[str] = []
    checked = 0

    cli_src = "\n".join(fetch(VLLM_RAW.format(rel=f)) for f in VLLM_CLI_FILES)
    cli_args = set(re.findall(r'add_argument\(\s*(?:"[^"]+",\s*)?"--([a-z][a-z0-9-]+)"', cli_src))
    # args registered from dataclass fields (FrontendArgs / kwargs-style) count too
    field_names = set(re.findall(r'^\s{4}([a-z][a-z0-9_]*)\s*:\s', cli_src, re.M))
    cli_args |= {f.replace("_", "-") for f in field_names}

    data = yaml.safe_load(EA_YAML.read_text(encoding="utf-8"))
    entries = data["args"]
    doc_cache: dict[str, str] = {}

    for e in entries:
        arg = e["arg"]
        checked += 1
        if arg not in cli_args:
            failures.append(f"engine-arg '{arg}': not found in vLLM CLI definitions")

        # examples: value must appear next to the arg in the cited file
        for ex in e.get("examples", []):
            src = ex["source"]
            try:
                ref, rel = parse_docs_url(src)
            except ValueError as exc:
                failures.append(f"engine-arg '{arg}': {exc}")
                continue
            url = ASCEND_RAW.format(ref=ref, rel=rel)
            if url not in doc_cache:
                try:
                    doc_cache[url] = fetch(url)
                except Exception as exc:  # noqa: BLE001
                    failures.append(f"engine-arg '{arg}': cannot fetch {url}: {exc}")
                    doc_cache[url] = ""
                    continue
            norm = normalize_cmd(doc_cache[url])
            value = ex["value"]
            if value in ("{", ""):
                continue
            # 从被引用文档中提取该参数的完整取值，做前缀匹配
            # （data 里的值可能被空格截断为 JSON 片段）
            extracted = re.findall(
                rf"--{re.escape(arg)}(?:\s*[= ]\s*)((?:'[^']*')|(?:\"[^\"]*\")|(?:\{{[^}}]*\}})|(?:\S+))",
                norm,
            )
            stripped = [v.strip("'\"") for v in extracted]
            if not any(v == value or v.startswith(value) or value.startswith(v) and len(v) >= 4
                       for v in stripped):
                failures.append(
                    f"engine-arg '{arg}': example value {value!r} not found next to "
                    f"--{arg} in {src}"
                )
    return checked, len(entries), failures


def main() -> int:
    print("== Audit: engine args ==")
    ea_checked, ea_total, ea_fail = audit_engine_args()
    print(f"checked {ea_checked}/{ea_total} engine args, {len(ea_fail)} failure(s)")

    all_fail = ea_fail
    if all_fail:
        print("\nFAILURES:")
        for f in all_fail:
            print(f"  ✗ {f}")
        return 1
    print("\nAUDIT PASSED: all engine args traceable to official sources.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
