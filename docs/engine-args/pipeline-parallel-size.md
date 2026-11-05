---
title: pipeline-parallel-size
---

# `--pipeline-parallel-size`

> 流水线并行（PP）组数，用于跨机部署超大模型。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

Number of pipeline parallel groups.（vLLM 源码 `ParallelConfig.pipeline_parallel_size`）

## Ascend 语境与官方用法

- 官方教程取值：**1 / 2 / 4**。超大模型（如 [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)）多机部署时启用，把模型层切到不同节点。
- Ascend 的**动态分块流水线并行（CPP）**针对 PP 场景优化 micro-batch 切分，见 [`profiling_chunk_config`](../flags/profiling-chunk-config.md) 与[官方 CPP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)。
- PP 与 DP/TP 可叠加；PP 会带来 pipeline bubble，通常仅在模型放不进单机时启用。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --pipeline-parallel-size 2 --tensor-parallel-size 8
```

## 相关参数

- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--data-parallel-size`](data-parallel-size.md)
