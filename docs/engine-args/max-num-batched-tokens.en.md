---
title: max-num-batched-tokens
---

# `--max-num-batched-tokens`

> Max tokens processed per iteration — the core knob for prefill chunking and batch scheduling.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto) |
| Category | Scheduling & Memory |

## Official definition

Maximum number of tokens that can be processed in a single iteration. (vLLM source: `EngineArgs` / `SchedulerConfig`)

## Ascend context & official usage

- Typical tutorial values: **1024 (small models) / 10240 / 16384 / 20480 / 32768** — e.g. [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) uses 10240; [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) uses 20480.
- **Most sensitive knob for CPP (dynamic chunked pipeline parallelism)** ([dynamic_chunk_pipeline_parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)):
  - Recommended fixed-chunk search space: **[8192, 16384, 24576, 32768]**;
  - With dynamic chunking enabled, the optimum is typically **2–4×** the fixed-chunk optimum;
  - Longer sequences need larger `--max-num-batched-tokens`.
- Interacts with [`enable_prefill_mc2`](../flags/enable-prefill-mc2.md): officially recommended ≤ `tp_size × 512` when enabled.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-num-batched-tokens 16384
```

## Related args

- [`--max-num-seqs`](max-num-seqs.md)
- [`--enable-chunked-prefill`](enable-chunked-prefill.md)
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md)
