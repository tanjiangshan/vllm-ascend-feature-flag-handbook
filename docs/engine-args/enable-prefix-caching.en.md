---
title: enable-prefix-caching
---

# `--enable-prefix-caching` / `--no-enable-prefix-caching`

> Prefix caching: reuse KV blocks of shared prefixes — a big TTFT win for multi-turn chat and shared system prompts.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `None` (auto per model/backend — see below) |
| Category | Scheduling & Memory |

## Official definition

> Whether to enable prefix caching.

(vLLM source: `CacheConfig.enable_prefix_caching`, [cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py))

## How it works

**The principle**: if request 1 and request 2 share a prompt prefix (same system prompt, or a multi-turn history), their KV blocks over that span are identical. When enabled, the scheduler hashes block contents and reuses identical blocks — request 2 skips prefill over the whole shared span, cutting that part of TTFT entirely.

**Default auto-resolution** (when omitted from the CLI, `EngineArgs` judges by model capability, [arg_utils.py `_set_default_chunked_prefill_and_prefix_caching_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)):

```
None → model_config.is_prefix_caching_supported (auto-on when the model/backend supports it)
```

So on main, "unset" usually means "on" — unless the model or backend explicitly lacks support.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--block-size`](block-size.md) | Hit granularity = block boundary; `prefix_match_unit` must divide the block size (source-level hard check) |
| [`--kv-transfer-config`](kv-transfer-config.md) | **explicitly disabled under PD disaggregation** (below) |
| Ascend KV-layout flags ([`enable_kv_nz`](../flags/enable-kv-nz.md)) | Affect the underlying block layout used by prefix caching |

**Conflict with PD disaggregation** (important): in the official [PD disaggregation (Mooncake) tutorial](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html), both prefill and decode nodes pass **`--no-enable-prefix-caching`**. Reason: under PD, KV moves between nodes and prefix-reuse semantics are owned by the KV transfer layer; enabling local prefix caching on top creates duplicated/conflicting semantics. Rule of thumb: **PD on → local prefix caching off**.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Multi-turn chat / shared system prompt | **Enable** (the auto default is usually enough) — significant TTFT gains |
| PD disaggregation | **Disable** (`--no-enable-prefix-caching`, per the official tutorial) |
| Single-turn short prompts, no shared prefix | Zero benefit either way |

## Ascend context & official usage

- PD disaggregation tutorials (Mooncake single/multi-node): both prefill and decode nodes use `--no-enable-prefix-caching`.
- General online serving: rely on auto-resolution (on by default).

## Usage

```bash
# general serving (explicit on)
vllm serve Qwen/Qwen3-8B --enable-prefix-caching

# PD disaggregation nodes (off, per official tutorial)
vllm serve Qwen/Qwen3-8B --no-enable-prefix-caching --kv-transfer-config '{...}'
```

## Related args

- [`--block-size`](block-size.md) — hit granularity
- [`--kv-transfer-config`](kv-transfer-config.md) — PD interplay
