---
title: vLLM-Ascend Feature Flag Handbook
hide:
  - navigation
---

<div class="hero" markdown>

# vLLM-Ascend Feature Flag Handbook

**A community-maintained deep reference of vLLM-Ascend feature flags:**

`--additional-config` keys ｜ Environment variables ｜ Migration ｜ Version history

</div>

## What is this?

vLLM-Ascend controls a large set of experimental, scenario-specific optimizations via **feature flags**: fused MoE operators (MC2), dynamic EPLB, weight NZ layout, balance scheduling, RL mode, and more.

The official docs scatter these flags across several pages in the form of terse tables. This handbook aims to be:

1. **Complete**: every `--additional-config` key and every active environment variable;
2. **Searchable**: one overview table plus per-flag pages;
3. **Traceable**: introduction version, migration status (PR #9064 env-var migration), applicable hardware;
4. **Machine-readable**: `docs/flags.json` for scripts and tools.

!!! note "Relationship with official docs"
    This handbook is a **community supplement**, not a replacement for the [official documentation](https://docs.vllm.ai/projects/ascend/en/latest/). When in doubt, trust the official docs — and please open an issue here so we can fix the handbook.

## Quick links

<div class="grid cards" markdown>

-   :material-flag-outline:{ .lg .middle } **Feature flags overview**

    ---

    64 vLLM-Ascend proprietary flags: keys / defaults / status / version support

    [:octicons-arrow-right-24: Open](flags/index.md)

-   :material-tune:{ .lg .middle } **Engine args**

    ---

    78 `vllm serve` args with Ascend context, evidenced from official tutorials

    [:octicons-arrow-right-24: Open](engine-args/index.md)

-   :material-table:{ .lg .middle } **Version support matrix**

    ---

    Which of v0.23.0 / v0.30.0 / main supports each flag

    [:octicons-arrow-right-24: Open](version-matrix.md)

-   :material-swap-horizontal:{ .lg .middle } **Migration table**

    ---

    10 environment variables → `--additional-config` quick reference

    [:octicons-arrow-right-24: Open](migration.md)

-   :material-console:{ .lg .middle } **Quick start**

    ---

    Online/offline usage of `--additional-config` and common pitfalls

    [:octicons-arrow-right-24: Open](quick-start.md)

-   :material-history:{ .lg .middle } **Version history**

    ---

    When each flag was introduced, deprecated or removed

    [:octicons-arrow-right-24: Open](version-history.md)

</div>

## Contributing

The data source lives in [`data/flags/`](https://github.com/tanjiangshan/vllm-ascend-feature-flag-handbook/tree/main/data/flags) as YAML files. Fixing a default, adding a risk note, or documenting a new flag are all welcome contributions. See [Contributing](contributing.md).
