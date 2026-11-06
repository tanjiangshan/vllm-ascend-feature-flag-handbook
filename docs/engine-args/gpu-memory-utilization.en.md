---
title: gpu-memory-utilization
---

# `--gpu-memory-utilization`

> Fraction of device memory the model executor may use (0–1) — **the source of the KV cache pool size**.

| Property | Value |
|---|---|
| Type | `float` (0–1) |
| Default | `None` → resolves to **1.0** (extensible KV cache) or **0.92** (otherwise) — vLLM main source, `resolved_gpu_memory_utilization` |
| Category | Scheduling & Memory |

## Official definition

> The fraction of GPU memory to be used for the model executor, which can range from 0 to 1. For example, a value of 0.5 would imply 50% GPU memory utilization. This is a per-instance limit, and only applies to the current vLLM instance... On non-GPU installs, this value controls the corresponding device memory utilization.

(vLLM source: `CacheConfig.gpu_memory_utilization`, [cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py))

Two takeaways:

1. **Per-instance limit**: it constrains the current vLLM instance only. When co-locating multiple instances on one device, each takes its own share;
2. **Applies to NPU too**: "On non-GPU installs, this value controls the corresponding device memory utilization" — on Ascend it controls NPU HBM.

## How it works

**The exact default semantics** ([`resolved_gpu_memory_utilization`](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py), property):

```
explicitly set → use the explicit value
unset          → enable_extensible_kv_cache ? 1.0 : DEFAULT_GPU_MEMORY_UTILIZATION (0.92)
```

So on main, "unset" is not a single number: 1.0 with the extensible KV cache (pool sized from measured memory), 0.92 on the traditional path (`DEFAULT_GPU_MEMORY_UTILIZATION` constant).

**Where the memory goes**: the fraction covers everything the model executor uses — weights, KV cache, activations. vLLM loads the weights and profiles at startup; **the remainder becomes the KV cache pool**:

```
KV pool ≈ total device memory × this arg − model weights − activation/workspace reserve
```

Weights dominate the difference (or shrink it, when quantized) — which is why quantized-model tutorials can afford 0.9 or higher.

## Parameter interplay

**Versus effective concurrency** (from the [`--max-num-seqs`](max-num-seqs.md) formula):

```
effective concurrency ≈ min(max_num_seqs, KV pool capacity ÷ average context length)
                            ↑
                    this parameter decides this term
```

If `max_num_seqs` is maxed out and you still need more concurrency, there are only two levers: raise this arg (bigger pool), or shrink per-request usage (`max_model_len`, `kv-cache-dtype`).

**Preemption linkage**: a full pool triggers preemption (rising `vllm:num_preemptions`). This arg is the #1 pool-size knob — but don't push it to 1.0 and risk runtime OOM: the traditional path's 0.92 default exists precisely to leave headroom for runtime fluctuation.

**Finer-grained alternative**: to cap the KV cache by bytes instead of a ratio, use `kv_cache_memory_bytes`.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Dedicated single-card production | Start at 0.85–0.90 (the official tutorial range); tune upward after confirming no OOM |
| Multiple instances on one card | Split proportionally; sum ≤ 1 minus OS/runtime reserve |
| Quantized weights | Weights take less room — raise this to give the KV pool more |
| OOM / profiling failure | Lower this first; or use quantized weights / smaller `max_model_len` |

## Ascend context & official usage

- Almost all official tutorials set it explicitly; observed range **0.80–0.90**:
  - 0.80: [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)
  - 0.85: [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html), [Qwen3.5-27B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html)
  - 0.90: many A2/A3 tutorials (e.g. [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html))
- Quantized Ascend models (W8A8 etc.) leave more room for KV — one reason tutorials run 0.9 — but always confirm with the startup profiling output.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --gpu-memory-utilization 0.9
```

## Related args

- [`--kv-cache-memory-bytes`](index.md) — cap KV cache by bytes precisely
- [`--max-num-seqs`](max-num-seqs.md) — concurrency cap, indirectly bounded by this arg
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV quantization, effectively enlarges the pool
