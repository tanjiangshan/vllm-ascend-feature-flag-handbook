---
title: Contributing
---

# Contributing

## Repository layout

```
├── data/flags/            # Single source of truth: one YAML per flag
├── docs/                  # MkDocs sources
│   └── flags/             # Per-flag detail pages (auto-stubbed when missing)
├── scripts/generate_tables.py   # Renders overview tables + stubs + flags.json
├── docs/flags.json        # Machine-readable export (auto-generated, do not edit)
└── mkdocs.yml
```

## Adding a flag

1. Create `data/flags/<key>.yaml` with the required fields:

```yaml
key: enable_xxx
type: bool            # bool | int | float | str | dict | list
default: false
status: active        # active | deprecated | removed | planned
version_support:      # per-version support (true/false)
  v0.23.0: false
  v0.30.0: true
  main: true
desc:
  zh: 一句话中文说明。
  en: One-line English description.
```

   Common optional fields: `legacy_env`, `hardware`, `models`, `requires` / `conflicts`, `values`, `version_note` (bilingual), `source`.

2. Run the generator:

```bash
pip install -r requirements.txt
python scripts/generate_tables.py
```

   It validates the YAML, updates the overview table, stubs missing detail pages, and exports `flags.json`.

3. (Recommended) Replace the stub `docs/flags/<key>.md` with a full page: rationale, usage, applicable scenarios, risks, interactions.
4. Open a PR. CI regenerates and validates everything.

## Updating a flag

- **Defaults / status / migration info**: edit only `data/flags/*.yaml`. Never hand-edit the overview table (it is regenerated).
- **Detail page prose**: edit the matching `docs/flags/*.md`.
- **Commit the regenerated `docs/flags.json` and `docs/includes` changes** — CI enforces this via `git diff --exit-code`.

## Content guidelines

1. **Accuracy first**: defaults, status and hardware support must be verifiable (official docs, source code, release notes). Cite the source in the YAML `source` field.
2. **Official docs win conflicts**: if this handbook disagrees with the official docs, open an issue here.
3. **Surface risks explicitly**: flags that break accuracy, are profiling-only, or carry memory costs must use a `!!! warning` admonition.
4. **Bilingual**: YAML `desc` needs both `zh` and `en`. Detail pages may start Chinese-first; English translations welcome.

## Local preview

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000>.
