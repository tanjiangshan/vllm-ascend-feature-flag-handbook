---
title: distributed-executor-backend
---

# `--distributed-executor-backend`

> Distributed executor backend: multi-process (mp) or Ray.

| Property | Value |
|---|---|
| Type | `str` |
| Default | `None` (auto) |
| Category | Parallelism |

## Official definition

Backend to use for distributed model workers, either "mp" (multi-process) or "ray" (Ray, distributed). (vLLM source: `ParallelConfig.distributed_executor_backend`)

## Ascend context & official usage

- Explicit values in official tutorials: **mp** (single node, e.g. [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) `--distributed-executor-backend "mp"`) and **ray** (multi-node large models, e.g. [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)).
- Rule of thumb, matching official usage: **mp for single node** (fast startup, low overhead), **ray for multi-node**.
- Distinct from `--data-parallel-backend`: that one is the DP-layer backend; this one is the TP/PP worker executor.

## Usage

```bash
# single node
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 8 --distributed-executor-backend mp
# multi-node
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 16 --distributed-executor-backend ray
```

## Related args

- [`--data-parallel-backend`](index.md)
- [`--tensor-parallel-size`](tensor-parallel-size.md)
