---
title: kv-cache-dtype
---

# `--kv-cache-dtype`

> KV cache storage dtype — directly determines KV bytes per token; the #1 lever for trading precision for concurrency.

| Property | Value |
|---|---|
| Type | `str` (CacheDType) |
| Default | `"auto"` (follows model dtype) |
| Category | Scheduling & Memory |

## Official definition

> Data type for kv cache storage. If "auto", will use model data type. CUDA 11.8+ supports fp8 (=fp8_e4m3) and fp8_e5m2. ROCm (AMD GPU) supports fp8 (=fp8_e4m3). Intel Gaudi (HPU) supports fp8 (using fp8_inc). Some models (namely DeepSeekV3.2) default to fp8, set to bfloat16 to use bfloat16 instead...

(vLLM source: `CacheConfig.cache_dtype`, [cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py))

## How it works

**The quantization target is the KV cache, not the weights**: the two are independent. Weight quantization is controlled by [`--quantization`](quantization.md); this arg controls the storage format of the K/V tensors during attention. fp8 KV halves bytes per token vs bf16 — effectively doubling the KV pool.

**Three points from the source docstring**:

1. `auto` = follow the model weight dtype;
2. **Some models default to fp8** (the source names DeepSeekV3.2) — on those, pass `bfloat16` explicitly to opt out;
3. Explicit `fp16`/`bfloat16` **must match the model dtype**, otherwise an error is raised;
4. Platform backends can register custom KV dtypes via `register_kv_cache_dtype` — **Ascend fp8/int8 KV support uses this mechanism**.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | KV quantization = effectively enlarging the pool; both stack |
| [`--block-size`](block-size.md) | commonly configured together in official tutorials (fp8 + block 32) |
| [`--max-num-seqs`](max-num-seqs.md) | a bigger pool means less preemption at the same concurrency |
| Weight NZ ([`weight_nz_mode`](../flags/weight-nz-mode.md)) | don't confuse: that one is for weights, this one is KV cache |

**The memory math**: KV tokens that fit ≈ pool capacity ÷ (2 × layers × KV heads × head dim × bytes per element). `kv-cache-dtype fp8` drops "bytes per element" from 2 to 1 — capacity ×2.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| MoE large models, long context (mainstream official pattern) | fp8 (see the DeepSeek-V4-Pro recipe); validate precision regression |
| Precision-sensitive | auto / bfloat16; free memory via other levers |
| Mamba/SSM models | the counterpart is `--mamba-ssm-cache-dtype`, default auto |

## Ascend context & official usage

- Explicit values in official tutorials:
  - **fp8** — [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html): `--kv-cache-dtype fp8` with `--attention_config.indexer_kv_dtype fp8`
  - **int8** / **mxfp8** — other quantized-model tutorials
- The precision/memory tradeoff is explicit: fp8 KV halves memory, but validate accuracy for your workload.

## Usage

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## Related args

- [`--quantization`](quantization.md) — weight quantization (independent of this arg)
- [`--block-size`](block-size.md) — commonly configured together
- [`--mamba-ssm-cache-dtype`](index.md) — the Mamba-family counterpart
