---
title: distributed-executor-backend
---

# `--distributed-executor-backend`

> 分布式执行后端：单机多进程（mp）还是 Ray（ray）。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（自动选择） |
| 分类 | 并行策略 |

## 官方定义

Backend to use for distributed model workers, either "mp" (multi-process) or "ray" (Ray, distributed).（vLLM 源码 `ParallelConfig.distributed_executor_backend`）

## Ascend 语境与官方用法

- 官方教程明确取值：**mp**（单机，如 [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) `--distributed-executor-backend "mp"`）和 **ray**（多机大模型，如 [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)）。
- 经验法则与官方用法一致：**单机用 mp（启动快、开销小），跨机用 ray**。
- 与 `--data-parallel-backend` 区分：后者是 DP 层后端，本参数是 TP/PP worker 执行后端。

## 用法

```bash
# 单机
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 8 --distributed-executor-backend mp
# 多机
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 16 --distributed-executor-backend ray
```

## 相关参数

- [`--data-parallel-backend`](index.md) — DP 后端（mp/ray）
- [`--tensor-parallel-size`](tensor-parallel-size.md)
