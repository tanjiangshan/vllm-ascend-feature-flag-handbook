---
title: block-size
---

# `--block-size`

> Physical KV cache block size in tokens; prefix-cache hit granularity depends on it.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto; typically 16, depends on attention backend page size) |
| Category | Scheduling & Memory |

## Official definition

Size of a contiguous cache block in number of tokens. (vLLM source: `CacheConfig.block_size`, `Field(default=None, gt=0)`)

## Ascend context & official usage

- Explicit values in official tutorials: **32** ([DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html), with fp8 KV cache), **128**, **1536** (KVPP scenarios).
- Affects:
  - Prefix-cache hit boundaries (`hash_block_size` must divide block_size);
  - KV cache internal/external fragmentation.
- When combined with Ascend KV-layout flags (e.g. [`enable_kv_nz`](../flags/enable-kv-nz.md), KVPP), follow the values given in the feature docs.

## Usage

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --block-size 32 --kv-cache-dtype fp8
```

## Related args

- [`--kv-cache-dtype`](kv-cache-dtype.md)
- [`--enable-prefix-caching`](enable-prefix-caching.md)
