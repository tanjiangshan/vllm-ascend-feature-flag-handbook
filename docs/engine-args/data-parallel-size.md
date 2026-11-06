---
title: data-parallel-size
---

# `--data-parallel-size`

> 数据并行（DP）组数——在副本维度扩并发；**MoE 专家并行（EP）的规模来源**。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

> Number of data parallel groups. **MoE layers will be sharded according to the product of the tensor, prefill-context, and data parallel sizes.**

（vLLM 源码：`ParallelConfig.data_parallel_size`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)；加粗为源码原文强调）

## 机制详解

**切什么**：请求。每个 DP 副本是完整独立的一套"TP×PP worker + scheduler"，各自服务各自的请求队列。副本间用 RPC 同步元信息（调度、负载均衡等），head 节点对 API 层统一接流。

**对 MoE 的额外含义**（源码 docstring 原文）：开启 [`--enable-expert-parallel`](enable-expert-parallel.md) 后，MoE 层专家按 **TP × PCP × DP 的乘积分片**——DP 每加 1，每 rank 承载的专家就少一份。这就是为什么大 MoE 模型的"EP 规模"主要不是调 TP 而是调 DP。

**多节点 DP 的配套参数（缺一不可）**：

| 参数 | 作用 |
|---|---|
| `--data-parallel-size-local` | 本节点副本数（源码校验：必须 ≤ `data_parallel_size`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)） |
| `--data-parallel-start-rank` | 本节点起始 rank |
| `--data-parallel-address` | head 节点地址 |
| `--data-parallel-rpc-port` | RPC 固定端口 |

非头节点再加 `--headless`（只跑推理不开 API）。

**另一个源码校验**：`data_parallel_size_external_lb` 仅在 `data_parallel_size > 1` 时可用（[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)）。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--enable-expert-parallel`](enable-expert-parallel.md) | DP 是 EP 规模的主要调节量（专家按 TP×PCP×DP 切分） |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | 与 DP 相乘决定 MoE 每 rank 专家数 |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | 专家分片的第三个因子 |
| Ascend [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md) | DP 副本间的请求均衡调度 |

**类比**：DP 像多开几家分店——每家店完整复制（完整 worker 栈），分店数 = 并发接待能力；对 MoE 而言，分店多了后"总部的稀缺人才（专家）可以分得更细"。

## Ascend 语境与官方用法

- 官方 MoE 教程标配：`--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M`（[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)、[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)、[GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) 等）。
- 官方多节点教程通过 `--data-parallel-*` 系列参数做节点寻址；非头节点 `--headless`。
- Ascend 专属：DP 副本间均衡调度见 [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md)。

## 用法

```bash
# 双节点 DP=8，每节点 4 副本（第二个节点示例）
vllm serve Qwen/Qwen3-8B \
  --enable-expert-parallel --data-parallel-size 8 \
  --data-parallel-size-local 4 --data-parallel-start-rank 4 \
  --data-parallel-address $HEAD_IP --data-parallel-rpc-port 29500 \
  --tensor-parallel-size 8
```

## 相关参数

- [`--enable-expert-parallel`](enable-expert-parallel.md) — DP 是 EP 的规模来源
- [`--tensor-parallel-size`](tensor-parallel-size.md) — 与 DP 相乘决定每 rank 专家数
- [`--headless`](index.md) / [`--distributed-executor-backend`](distributed-executor-backend.md) — 多节点部署配套
