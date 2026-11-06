---
title: tensor-parallel-size
---

# `--tensor-parallel-size`

> 张量并行（TP）组数——最基础的并行参数：把单层权重横切到多卡。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

> Number of tensor parallel groups.

（vLLM 源码：`ParallelConfig.tensor_parallel_size`，`Field(default=1, ge=1)`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)）

## 机制详解

**切什么**：attention 的 Q/K/V/输出投影和 MLP 矩阵乘法，按**头/列**切到不同卡上。每张卡存一部分权重、算一部分结果，每层前后各一次 all-reduce 聚合。模型放不下单卡时的第一道扩容手段。

**它对形状有硬约束**（源码启动校验，[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）：

```
total_num_attention_heads % tensor_parallel_size == 0
否则启动报错："Total number of attention heads (...) must be divisible by tensor parallel size (...)"
```

**它参与 world size 定义**：[arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) 中 `world_size = pipeline_parallel_size × tensor_parallel_size`——总卡数 = TP × PP，再叠 DP 做副本。

**注意 KV 头数**：GQA/MQA 模型 KV 头数远小于 Q 头数。TP 超过 KV 头数时 vLLM 会做 KV 复制（repeat），继续扩大 TP 不再省显存——MoE 大模型此时应转向 [`--enable-expert-parallel`](enable-expert-parallel.md) + DP。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | world size = TP × PP，两者相乘决定单机/集群占卡数 |
| [`--data-parallel-size`](data-parallel-size.md) | MoE 专家按 **TP × PCP × DP** 乘积分片（vLLM 源码 docstring） |
| [`--enable-expert-parallel`](enable-expert-parallel.md) | MoE 模型的显存解法二：EP 切专家，TP 只管 attention |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | DCP 对 GQA/MQA 要求 TP > KV 头数（源码校验） |
| [`--distributed-executor-backend`](distributed-executor-backend.md) | TP 跨机时必须 ray；单机 mp |

**类比**：TP 像把一本厚书的**每一页**裁成多份分给多人同时读——读得快了，但每翻一页大家都要对一次账（all-reduce）。

## Ascend 语境与官方用法

- 官方教程取值 **1 / 2 / 4 / 8 / 16**：
  - 单机 A2：[Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) tp4 + `--distributed-executor-backend mp`
  - A3 大模型：tp8 常见；多机场景 16
- 与细粒度 TP（[`finegrained_tp_config`](../flags/finegrained-tp-config.md)）组合时，oproj/mlp 可用**不同于 attention 的并行度**，代价是 cudagraph 捕获尺寸约束（见其公式）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 4
```

## 相关参数

- [`--pipeline-parallel-size`](pipeline-parallel-size.md) — world size 的另一因子
- [`--data-parallel-size`](data-parallel-size.md) — EP 的规模来源
- [`--enable-expert-parallel`](enable-expert-parallel.md) — MoE 的显存优化搭档
- [`--distributed-executor-backend`](distributed-executor-backend.md) — 单机 mp / 多机 ray
