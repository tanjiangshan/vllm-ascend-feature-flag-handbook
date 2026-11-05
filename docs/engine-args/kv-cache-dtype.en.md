---
title: kv-cache-dtype
---

# `--kv-cache-dtype`

> KV cache storage dtype — directly determines KV cache memory footprint.

| Property | Value |
|---|---|
| Type | `str` (CacheDType) |
| Default | `"auto"` (follows model dtype) |
| Category | Scheduling & Memory |

## Official definition

Data type for kv cache storage. If "auto", will use model data type... Some models (namely DeepSeekV3.2) default to fp8. (vLLM source: `CacheConfig.cache_dtype`)

## Ascend context & official usage

- Explicit values in official tutorials: **fp8** ([DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html): `--kv-cache-dtype fp8` with `--attention_config.indexer_kv_dtype fp8`), **int8**, **mxfp8**.
- Platform backends can register custom KV cache dtypes (`register_kv_cache_dtype`); Ascend fp8/int8 support uses this mechanism.
- Explicit fp16/bfloat16 must match the model dtype, otherwise an error is raised.
- Distinct from weight NZ ([`weight_nz_mode`](../flags/weight-nz-mode.md)): that one is for weights, this one is for KV cache.

## Usage

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## Related args

- [`--block-size`](block-size.md) — commonly configured together
- [`--mamba-ssm-cache-dtype`](index.md) — the Mamba-family counterpart
