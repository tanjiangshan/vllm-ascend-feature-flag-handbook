---
title: prefill-context-parallel-size
---

# `--prefill-context-parallel-size`

> Prefill 上下文并行（PCP）：把长请求的 prefill token 切到多卡并行计算，降低 TTFT。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

> Prefill Context Parallel (PCP) splits the prefill tokens of a long prefill request across additional ranks. Each rank computes a different part of the sequence, reducing time to first token (TTFT).

（vLLM-Ascend [官方上下文并行指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)；上游概念见 vLLM [Context Parallel Deployment](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/)）

## 机制详解

**与 TP 的区别**：TP 把"每层的矩阵"切开（所有 token 都过每卡的一部分）；PCP 把"一条序列"切开（不同卡算这条序列的不同**片段**，attention 层做跨卡交换）。TP 降的是单层计算量，PCP 降的是单条 prefill 的**时延**——长请求本来要一张卡串行算完，现在 N 张卡各算 1/N。

**与 DCP 的分工**：PCP 加速 prefill；[`--decode-context-parallel-size`](index.md)（DCP）把 KV 按 decode 组切分，降重复 KV 存储、提 decode 吞吐。两者可叠加复用同一批卡。

**当前状态**：**PCP 在 vLLM-Ascend 上是 experimental**（官方指南原文）。

## 参数联动

**官方兼容性矩阵**（[Ascend 上下文并行指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)，A2/A3 MLA 全兼容）：

| 组合 | 兼容性 |
|---|---|
| MLA / GQA 基本 PCP | ✅ |
| 前缀缓存 / 分块 prefill / PD 分离（MooncakeConnectorV1/V2）+ PCP | ✅ 全兼容 |
| 图模式 + PCP | 部分（FULL 模式不支持） |
| 投机解码 + PCP | 部分：MLA 仅 MTP，GQA 仅 Eagle3 |
| 序列并行（SP）+ PCP | ✅（即 DSA-PCP，MRv2 推荐路径） |

**源码硬约束**（DCP 侧，[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）：

```
DCP > 1 且非 MLA（GQA/MQA）时：tensor_parallel_size 必须 > KV 头总数，
且 dcp_size ≤ TP // KV头数，且 每 KV 头的 Q 头数 % dcp_size == 0
```

**专家分片**：PCP 是 MoE 专家切分乘积 TP × **PCP** × DP 的第二个因子——开 PCP 同样会改变每 rank 专家数。

## Ascend 语境与官方用法

- 官方教程取值 **1 / 2 / 8**，常与 `--decode-context-parallel-size` 叠加。
- **DSA-PCP**（PCP + 序列并行）是 Ascend MRv2 的推荐长上下文路径，替代旧的环境变量开关 `enable_context_parallel`。
- experimental 状态下，升级 vllm-ascend 版本后应重新核对上表兼容性。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --prefill-context-parallel-size 2 --tensor-parallel-size 4
```

## 相关参数

- [`--decode-context-parallel-size`](index.md) — decode 阶段 KV 分片
- [`--cp-kv-cache-interleave-size`](index.md) — CP 的 KV 交错粒度
- [`--tensor-parallel-size`](tensor-parallel-size.md) — DCP 的上界约束
- [`--data-parallel-size`](data-parallel-size.md) — 专家分片的第三个因子
