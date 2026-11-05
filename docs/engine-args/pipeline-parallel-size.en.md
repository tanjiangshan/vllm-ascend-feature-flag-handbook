---
title: pipeline-parallel-size
---

# `--pipeline-parallel-size`

> Pipeline parallel (PP) group count, for multi-node deployments of very large models.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

Number of pipeline parallel groups. (vLLM source: `ParallelConfig.pipeline_parallel_size`)

## Ascend context & official usage

- Tutorial values: **1 / 2 / 4**. Enabled for multi-node super-large models (e.g. [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)) to spread layers across nodes.
- Ascend's **dynamic chunked pipeline parallelism (CPP)** optimizes micro-batch splitting for PP — see [`profiling_chunk_config`](../flags/profiling-chunk-config.md) and the [official CPP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html).
- PP stacks with DP/TP; it introduces pipeline bubbles, so enable it only when the model doesn't fit on one node.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --pipeline-parallel-size 2 --tensor-parallel-size 8
```

## Related args

- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--data-parallel-size`](data-parallel-size.md)
