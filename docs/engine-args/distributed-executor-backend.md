---
title: distributed-executor-backend
---

# `--distributed-executor-backend`

> 分布式执行后端：worker 进程怎么拉起、怎么通信——`mp`（多进程）还是 `ray`。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（自动选择） |
| 分类 | 并行策略 |

## 官方定义

> Backend to use for distributed model workers, either "mp" (multi-process) or "ray" (Ray, distributed).

（vLLM 源码：`ParallelConfig.distributed_executor_backend`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)）

## 机制详解

**它决定的是"worker 生命周期管理"**：TP/PP 确定后，每个 worker 进程怎么创建、怎么发现彼此、怎么做集合通信，由这个后端管。

- **mp（multi-process）**：vLLM 自己用 `multiprocessing` 拉本地进程。零外部依赖、启动快、开销小——但进程只在**单机**内；
- **ray**：把 worker 作为 Ray actor 调度。依赖 Ray 集群，启动重一些，但天然支持**跨机**——worker 可以落在集群任意节点。

**与 `--data-parallel-backend` 区分**：本参数管的是 TP/PP 层 worker 的执行后端；`--data-parallel-backend`（mp/ray）管的是 DP 副本层的后端。两层独立选择。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--tensor-parallel-size`](tensor-parallel-size.md) | TP 跨机 → 必须 ray；单机两者皆可 |
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | PP 跨机 → 必须 ray |
| [`--data-parallel-backend`](index.md) | DP 层后端，与本参数独立 |

**经验法则（与官方用法一致）**：**单机 mp，跨机 ray**。mp 启动更快、依赖更少；一旦 worker 需要跨节点，只有 ray 可选。

## Ascend 语境与官方用法

- 官方教程明确取值：
  - **mp**——单机，如 [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html)：`--distributed-executor-backend "mp"`
  - **ray**——多机大模型，如 [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)
- Ascend 官方多机教程配合 Ray 集群文档（[tutorials/features/ray](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html)）使用。

## 用法

```bash
# 单机
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 8 --distributed-executor-backend mp
# 多机
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 16 --distributed-executor-backend ray
```

## 相关参数

- [`--data-parallel-backend`](index.md) — DP 层后端（mp/ray）
- [`--tensor-parallel-size`](tensor-parallel-size.md) — 单机/跨机的决定因素
