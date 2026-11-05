---
title: gpu-memory-utilization
---

# `--gpu-memory-utilization`

> Fraction of device memory the model executor may use (0–1). Applies to NPU memory on Ascend.

| Property | Value |
|---|---|
| Type | `float` |
| Default | `None` → resolves to **1.0** (extensible KV cache) or **0.92** (otherwise) — vLLM main source, `resolved_gpu_memory_utilization` |
| Category | Scheduling & Memory |

## Official definition

The fraction of GPU memory to be used for the model executor... On non-GPU installs, this value controls the corresponding device memory utilization. (vLLM source: `CacheConfig`)

## Ascend context & official usage

- Almost all official tutorials set it explicitly; observed range **0.80–0.90**:
  - 0.80: [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)
  - 0.85: [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html), [Qwen3.5-27B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html)
  - 0.90: many A2/A3 tutorials
- This is a **per-instance** limit; split proportionally when co-locating instances.
- Available KV cache ≈ total HBM × this value − weights − activations, which sets the concurrency/context ceiling.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --gpu-memory-utilization 0.9
```

## Related args

- [`--kv-cache-memory-bytes`](index.md)
- [`--max-num-seqs`](max-num-seqs.md)
