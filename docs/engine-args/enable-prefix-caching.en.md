---
title: enable-prefix-caching
---

# `--enable-prefix-caching` / `--no-enable-prefix-caching`

> Prefix caching: reuse KV blocks of shared prefixes to cut TTFT on long-prompt workloads.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `None` (auto per model/backend) |
| Category | Scheduling & Memory |

## Official definition

Whether to enable prefix caching. (vLLM source: `CacheConfig.enable_prefix_caching`)

## Ascend context & official usage

- In the official [PD disaggregation (Mooncake) tutorial](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html), both prefill and decode nodes pass **`--no-enable-prefix-caching`** — under PD, prefix-cache semantics are owned by the KV transfer layer; do not enable both.
- Recommended for general online serving (multi-turn chat, shared system prompts).
- Ascend-specific: KV cache layout flags such as [`enable_kv_nz`](../flags/enable-kv-nz.md) affect the underlying layout.

## Usage

```bash
# general serving
vllm serve Qwen/Qwen3-8B --enable-prefix-caching
# PD disaggregation nodes (per official tutorial)
vllm serve Qwen/Qwen3-8B --no-enable-prefix-caching --kv-transfer-config '{...}'
```

## Related args

- [`--block-size`](block-size.md) — hit granularity
- [`--kv-transfer-config`](kv-transfer-config.md) — PD interplay
