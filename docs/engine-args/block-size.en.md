---
title: block-size
---

# `--block-size`

> Physical KV cache block size (in tokens) — affects prefix-cache hit granularity and fragmentation.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` ("use default"; the engine resolves it from the attention backend page size — source comment in [cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)) |
| Category | Scheduling & Memory |

## Official definition

> Size of a contiguous cache block in number of tokens.

(vLLM source: `CacheConfig.block_size`, `Field(default=None, gt=0)`, comment "Accepts None (meaning 'use default'). After construction, always int.", [cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py))

## How it works

**Blocks are the KV allocation unit**: vLLM does not allocate KV token-by-token; it takes/releases memory in whole fixed-size blocks. A request asks for N blocks; on completion, blocks are returned.

**Two direct consequences**:

1. **Fragmentation**: a sequence of length L occupies `ceil(L / block_size)` blocks — the last block wastes half on average. Bigger blocks mean more internal fragmentation;
2. **Prefix-cache granularity**: prefix caching hits at block boundaries. Bigger blocks mean coarser hits (shared boundaries must align to a block) but less metadata overhead.

In source, `prefix_match_unit` (the finest token boundary a prefix hit can land on) has a divisibility check: "prefix-cacheable KV cache group block sizes must be divisible by prefix_match_unit" ([kv_cache_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/v1/core/kv_cache_utils.py)) — the coupling between block size and hit granularity is a hard constraint in code.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--enable-prefix-caching`](enable-prefix-caching.md) | Hit granularity = block boundary; fine-grained hits need both tuned |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | KV quantization changes bytes per token; together with block size it sets per-block memory |
| Ascend KV-layout flags ([`enable_kv_nz`](../flags/enable-kv-nz.md), KVPP) | Layout features impose their own block-size/alignment requirements — follow the feature docs |

Rule of thumb: smaller blocks → less fragmentation, finer hits, more metadata overhead; larger blocks → less overhead, more fragmentation and coarser hits. The resolved default suits most workloads — **official tutorials that set it explicitly do so for a specific reason** (below).

## Ascend context & official usage

- Explicit values and their context in official tutorials:
  - **32** — [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html), paired with `--kv-cache-dtype fp8` (fp8 KV block layout)
  - **128** / **1536** — KVPP and other KV-pooling scenarios
- Don't copy those values blindly: 128/1536 belong to specific feature combinations. For general deployment, the resolved default is the right baseline.

## Usage

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --block-size 32 --kv-cache-dtype fp8
```

## Related args

- [`--kv-cache-dtype`](kv-cache-dtype.md) — commonly configured together
- [`--enable-prefix-caching`](enable-prefix-caching.md) — hit granularity depends on block boundaries
