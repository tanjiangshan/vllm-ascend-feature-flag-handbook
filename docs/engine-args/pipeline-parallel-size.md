---
title: pipeline-parallel-size
---

# `--pipeline-parallel-size`

> 流水线并行（PP）组数——把模型的**层**分段铺到不同设备，专攻"模型放不进单机"。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

> Number of pipeline parallel groups.

（vLLM 源码：`ParallelConfig.pipeline_parallel_size`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)）

## 机制详解

**切什么、怎么流**：TP 切"每一层内部"，PP 切"层与层之间"。模型按层分成若干段，每卡持有一段；一个 micro-batch 像流水线一样逐段流过全部设备，同一时间不同设备处理不同 micro-batch 的不同层段。

**两个代价**：

1. **流水线气泡**：设备在等上一段的输出时空转，气泡占比随段数上升；
2. **调度复杂度**：需要把 batch 拆成 micro-batch 轮转。

**源码硬约束**（[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）：

```
PP > 1 时，模型必须实现 SupportsPP 接口，否则 NotImplementedError：
"Pipeline parallelism is not supported for this model."
```

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--tensor-parallel-size`](tensor-parallel-size.md) | world size = TP × PP；单机放不下才叠 PP |
| [`--data-parallel-size`](data-parallel-size.md) | DP/PP 可叠加，大规模 MoE 常见 TP×PP×DP 组合 |
| Ascend [`profiling_chunk_config`](../flags/profiling-chunk-config.md) | **CPP 动态分块**专门为 PP 优化 micro-batch 切分，缓解气泡 |

**类比**：PP 像工厂流水线——每个工位（设备）负责固定的几道工序（层段），产品（micro-batch）依次流过。工位越多单件越快？不一定：工位间传送带空转（气泡）吃掉收益。所以只在"一件产品一个工位做不完"时增加工位。

## Ascend 语境与官方用法

- 官方教程取值 **1 / 2 / 4**：超大模型（如 [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)）多机部署时启用。
- Ascend 的 **CPP（动态分块流水线并行）** 是 PP 场景的专属优化：按设备负载动态调整每步 micro-batch 的 token 切分，官方指南的调优对象是 [`--max-num-batched-tokens`](max-num-batched-tokens.md)（搜索空间 [8192, 16384, 24576, 32768]，动态分块最优值为固定值的 2–4 倍）。
- 经验法则：模型能单机放下就别开 PP（气泡纯亏）；放不下时 PP 是必选项，再叠 CPP 减少气泡损失。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --pipeline-parallel-size 2 --tensor-parallel-size 8
```

## 相关参数

- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--data-parallel-size`](data-parallel-size.md)
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend PP 的专属优化
