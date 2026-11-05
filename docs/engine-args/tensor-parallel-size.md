---
title: tensor-parallel-size
---

# `--tensor-parallel-size`

> 张量并行（TP）组数，最基础的并行参数。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

Number of tensor parallel groups.（vLLM 源码 `ParallelConfig.tensor_parallel_size`，`Field(default=1, ge=1)`）

## Ascend 语境与官方用法

- 官方教程取值：**1 / 2 / 4 / 8 / 16**。单机 A2 常用 2–8（如 [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) tp4 + `--distributed-executor-backend mp`）；A3 大模型常见 tp8；多机场景 16。
- MoE 模型注意：专家按 **TP × PCP × DP** 的乘积分片（vLLM 源码 `data_parallel_size` 说明），TP 取值影响 EP 切分布局。
- 与细粒度 TP（[`finegrained_tp_config`](../flags/finegrained-tp-config.md)）组合时，子模块可设不同并行度。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 4
```

## 相关参数

- [`--data-parallel-size`](data-parallel-size.md) — EP 部署的核心组合
- [`--pipeline-parallel-size`](pipeline-parallel-size.md) — 多机大模型
- [`--distributed-executor-backend`](distributed-executor-backend.md) — 单机 mp / 多机 ray
