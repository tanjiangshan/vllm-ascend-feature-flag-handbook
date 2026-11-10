---
title: Ascend Configuration Entry Points
---

# Ascend Configuration Entry Points

> vLLM-Ascend configuration lives in **more places than `--additional-config`**. This page is the map of all 6 entry points: what each is, who reads it, typical keys, and the traps — with links to the deep-dives.

## Entry-point map

| # | Entry point | Form | Read by | Deep dive |
|---|---|---|---|---|
| 1 | Top-level vLLM CLI args | `--key val` | vLLM engine (cross-platform) | [Engine args overview](engine-args/index.md) |
| 2 | `--additional-config` JSON | `'{"key": val}'` | Ascend plugin (`AscendConfig`) | [Feature flags overview](flags/index.md) |
| 3 | Ascend patches to CLI value domains | Ascend-only values of #1 args | Ascend platform patches | [§3 below](#3-ascend-patches-to-cli-value-domains) |
| 4 | Connector fields inside `--kv-transfer-config` | nested JSON | Ascend connector implementations | [kv-transfer-config page](engine-args/kv-transfer-config.md) |
| 5 | Environment variables | `export X=y` | build scripts / runtime | [Environment variables](env-vars.md) |
| 6 | `runtime_config.json` file | JSON(C) file | Runtime Guard | [§6 below](#6-runtime_configjson-runtime-guard) |

The six entries are not disjoint: one arg can be both #1 and #3 (a patch widened its value domain), and `runtime_config`'s startup keys go through #2 while its content lives in the #6 file. Crossings are flagged below.

## 1. Top-level vLLM CLI args (cross-platform engine args)

`vllm serve --max-num-seqs 256 --kv-cache-dtype fp8 ...` — args defined by upstream vLLM, shared across CUDA/ROCm/NPU, validated and consumed by the vLLM engine itself.

- The handbook covers 78: each **evidenced in official vLLM-Ascend tutorial command lines** and defined in the vLLM source CLI.
- Note: some arg values are re-consumed by the Ascend plugin to derive #2 flags (see the [kv-cache-dtype](engine-args/kv-cache-dtype.md) page) — hence the cross-links between the two overviews.
- Canonical example: `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` — the mainstream official recipe for graphing decode only on PD-disaggregated D nodes. Deep dive: [compilation-config detail page](engine-args/compilation-config.md).

## 2. `--additional-config` JSON (AscendConfig feature flags)

`vllm serve --additional-config '{"enable_kvpp": true, "eplb_config": {...}}'` — the Ascend plugin's own config keys, defined in `AscendConfig` (`vllm_ascend/ascend_config.py`), **Ascend-only**, pydantic-validated (`extra="forbid"` — a typo'd key fails startup).

- The handbook covers 64, organized by status (active/deprecated/removed/planned) and version support (v0.23.0/v0.30.0/main).
- The three Runtime Guard startup keys (`runtime_config` / `runtime_config_path` / `runtime_config_hot_reload`) also go here, but their **content** lives in the #6 file.

## 3. Ascend patches to CLI value domains

The easiest category to miss: vLLM-Ascend **adds no CLI args of its own** — instead it **widens the accepted values of existing args** (`vllm_ascend/patch/platform/`, applied at platform activation).

| Arg | Upstream values | Ascend patch adds | Purpose |
|---|---|---|---|
| `--kv-cache-dtype` | auto / fp8 / fp8_e5m2 / bf16 / fp16 … | `int8`, `mxfp8` | `int8`: KV cache of DeepSeek V4-style sparse MLA models; `mxfp8`: C8-MXFP layout (FP8 KV + E8M0 scales) on the A5 QFA path |
| `--attention_config.indexer_kv_dtype` | auto / bf16 / fp8 / mxfp4 / nvfp4 | `int8` | DeepSeek V4's indexer K cache |

**Trap**: reading vLLM's official docs alone, you'd never know these values are legal — validation lives in the patch-rebuilt pydantic Literal. The `--kv-cache-dtype int8 --attention_config.indexer_kv_dtype int8` pair in the official GLM5/5.2 tutorials is the evidence.

Details: [kv-cache-dtype page](engine-args/kv-cache-dtype.md), [enable_sparse_li_c8](flags/enable-sparse-li-c8.md), [enable_sparse_sfa_c8](flags/enable-sparse-sfa-c8.md).

## 4. Connector fields inside `--kv-transfer-config`

The KV transfer config itself is a #1 CLI arg, but the **connector fields inside its value are Ascend implementations**:

- `AscendStoreConnector`: `backend` (mooncake/memcache/yuanrong), `use_layerwise`, `lookup_rpc_port` — the KV pooling entry
- `MooncakeConnectorV2`: `use_ascend_direct`, prefill/decode topology declarations
- `MultiConnector`: composes multiple connectors (P2P transfer + pooling write)

Field-by-field anatomy: the "KV pooling" section of the [kv-transfer-config page](engine-args/kv-transfer-config.md).

## 5. Environment variables

Two families:

- **Runtime**: `VLLM_ASCEND_ENABLE_BATCH_MEMCPY` (no additional-config equivalent — env-only), `DYNAMIC_EPLB`, `EXPERT_MAP_RECORD`
- **Build-time**: `COMPILE_CUSTOM_KERNELS`, `MAX_JOBS`, `SOC_VERSION`, `ASCEND_HOME_PATH`, `HCCL_SO_PATH`, etc.

Full list: [Environment variables](env-vars.md). Rule of thumb: **if a config has an additional-config key, don't use the env var**; env vars only cover key-less switches and build behavior.

## 6. `runtime_config.json` (Runtime Guard)

vLLM-Ascend's **online anomaly detection and incident-response layer**: it watches decode-time signals (token repetition, garbled output, non-finite logits, speculative acceptance drift and more), writes structured reports under `runtime/report/` on trigger, and can optionally capture per-request KV cache blocks (`dump_kv`).

- **Content via file**: defaults to `<cwd>/runtime/config/runtime_config.json`, JSONC comments OK; top-level keys `actions` / `dump` / `ascend_log` / `report` / `detector`
- **Startup keys via #2**: `runtime_config_path` (relocate), `runtime_config_hot_reload` (startup hot-reload), `runtime_config` (startup overlay — **overwrites** any pre-existing file; start first then edit the live file, or put everything in the overlay)
- Default deployment keeps detectors off and hot-reload off — negligible overhead

Official docs: [Runtime Guard](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/runtime_guard.html) · [runtime_config JSON schema](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/runtime_config.html). Related flags: [runtime_config](flags/runtime-config.md), [runtime_config_path](flags/runtime-config-path.md), [runtime_config_hot_reload](flags/runtime-config-hot-reload.md).

## Which entry should I use

| What you want to configure | Entry point |
|---|---|
| Concurrency, parallelism, memory, quantization (generic behavior) | #1 CLI args |
| Ascend-only features (KVPP, EPLB, RL mode…) | #2 additional-config |
| Sparse-model KV dtype values (int8/mxfp8) | #1 + #3 (patched domains) |
| PD disaggregation / KV pooling transport | #1's `--kv-transfer-config` + #4 connector fields |
| Key-less build/runtime switches | #5 env vars |
| Online quality monitoring & incident dumps | #6 runtime_config.json |
