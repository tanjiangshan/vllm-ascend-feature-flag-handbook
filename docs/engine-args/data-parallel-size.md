---
title: data-parallel-size
---

# `--data-parallel-size`

> 数据并行（DP）组数。MoE 模型专家并行（EP）的核心参数。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

Number of data parallel groups. **MoE layers will be sharded according to the product of the tensor, prefill-context, and data parallel sizes.**（vLLM 源码 `ParallelConfig.data_parallel_size`）

## Ascend 语境与官方用法

- 官方 MoE 教程的标配组合：`--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M`（[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)、[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)、[GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) 等）。
- 多节点 DP 时必须配套：
  - `--data-parallel-size-local`（本节点副本数）
  - `--data-parallel-start-rank`（本节点起始 rank）
  - `--data-parallel-address`（head 节点地址）
  - `--data-parallel-rpc-port`（RPC 端口）
- 非头节点可配 `--headless` 只跑推理不开 API。
- Ascend 专属：DP 均衡调度见 [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md)。

## 用法

```bash
# 双节点 DP=8，每节点 4 副本
vllm serve Qwen/Qwen3-8B \
  --enable-expert-parallel --data-parallel-size 8 \
  --data-parallel-size-local 4 --data-parallel-start-rank 4 \
  --data-parallel-address $HEAD_IP --data-parallel-rpc-port 29500 \
  --tensor-parallel-size 8
```

## 相关参数

- [`--enable-expert-parallel`](enable-expert-parallel.md)
- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--headless`](index.md) / [`--distributed-executor-backend`](distributed-executor-backend.md)
