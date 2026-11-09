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
| `--attention_config.indexer_kv_dtype` | **Ascend-side C8 derivation pair**: since v0.30.0, the C8 layout of SFA sparse-attention models is derived from this arg (cache_dtype ∈ {fp8, int8}), while the Lightning-Indexer sparse layers' C8 layout is derived from `indexer_kv_dtype ∈ {fp8, int8}` — official tutorials set both together (e.g. `--kv-cache-dtype fp8 --attention_config.indexer_kv_dtype fp8`); P and D sides must use identical values |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | KV quantization = effectively enlarging the pool; both stack |
| [`--block-size`](block-size.md) | commonly configured together in official tutorials (fp8 + block 32) |
| [`--max-num-seqs`](max-num-seqs.md) | a bigger pool means less preemption at the same concurrency |
| Weight NZ ([`weight_nz_mode`](../flags/weight-nz-mode.md)) | don't confuse: that one is for weights, this one is KV cache |
| Ascend-derived flags | since v0.30.0, `cache_dtype ∈ {fp8, int8}` derives [`enable_sparse_sfa_c8`](../flags/enable-sparse-sfa-c8.md) on SFA models; `cache_dtype == turboquant_4bit_nc` derives `enable_sparse_sfa_turboquant` |

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
  - **int8** / **mxfp8** — see the patched value domain below
- The precision/memory tradeoff is explicit: fp8 KV halves memory, but validate accuracy for your workload.

## Ascend-patched values (int8 / mxfp8)

The upstream `CacheDType` values (auto / fp8 / fp8_e5m2 / fp8_e4m3 / bf16 / fp16…) **do not include int8**. vLLM-Ascend appends two Ascend-only values to the `CacheConfig.cache_dtype` Literal via the platform patch [`patch/platform/patch_kv_cache_dtype.py`](https://github.com/vllm-project/vllm-ascend/blob/main/vllm_ascend/patch/platform/patch_kv_cache_dtype.py) — **the same `--kv-cache-dtype` arg gains two extra legal values on Ascend**:

| Patched value | Meaning | Applies to |
|---|---|---|
| `int8` | KV cache stored in int8 | MLA KV cache of DeepSeek V4-style sparse MLA models; derives [`enable_sparse_sfa_c8`](../flags/enable-sparse-sfa-c8.md) on SFA models (since v0.30.0) |
| `mxfp8` | C8-MXFP layout: FP8 KV + E8M0 scales | A5-chip QFA path (verbatim from the patch header: "the A5 QFA path"); the C8-MXFP backend requires 512-token pages |

**Patch mechanics**: it rewrites the Literal in three places (the module symbol `CacheDType`, the class annotation, the dataclass field type) and then calls `rebuild_dataclass(force=True)` to regenerate the pydantic schema; on main it also appends both values to the `KV_CACHE_DTYPES` mirror list (read by the `is_known_kv_cache_dtype` validator), and CLI choices are widened in `platform.py::pre_register_and_update`; worker processes re-apply it via `patch/worker/patch_kv_cache_dtype.py`. The patch is idempotent.

**Trap**: outside the Ascend environment these two values are illegal — the validation logic is injected at plugin activation, so vLLM's official docs never mention them. v0.30.0's `derive_and_validate` already consumes `int8` (`cache_dtype in ["fp8", "int8"]` deriving SFA-C8), i.e. the int8 domain has been legal at least since v0.30.0.

The companion patch [`patch/platform/patch_indexer_kv_dtype.py`](https://github.com/vllm-project/vllm-ascend/blob/main/vllm_ascend/patch/platform/patch_indexer_kv_dtype.py) does the same for `--attention_config.indexer_kv_dtype`: the upstream Literal is `auto / bf16 / fp8 / mxfp4 / nvfp4`, and the patch appends `int8` (DeepSeek V4 Ascend indexer K cache). This is also the precondition for `indexer_kv_dtype ∈ {fp8, int8}` deriving LI-C8 since v0.30.0.

## Usage

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## Related args

- [`--quantization`](quantization.md) — weight quantization (independent of this arg)
- [`--block-size`](block-size.md) — commonly configured together
- [`--mamba-ssm-cache-dtype`](index.md) — the Mamba-family counterpart
