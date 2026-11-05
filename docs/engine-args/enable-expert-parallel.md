---
title: enable-expert-parallel
---

# `--enable-expert-parallel`

> MoE 层改用专家并行（EP）切分，替代默认的张量并行切分。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `False` |
| 分类 | 并行策略 |

## 官方定义

Use expert parallelism instead of tensor parallelism for MoE layers.（vLLM 源码 `ParallelConfig.enable_expert_parallel`）

## Ascend 语境与官方用法

- 官方 MoE 教程（DeepSeek-V4 全系、Kimi-K3 系、GLM5.2、Qwen3.5-397B、MiniMax-M3 等）**默认开启**，与 `--data-parallel-size` 配合实现大规模 EP。
- 专家按 TP × PCP × DP 乘积分片：EP 越大，每 rank 的专家越少、显存越省，但跨节点通信越多。
- Ascend 专属配套开关：
  - 动态专家均衡：[`dynamic_eplb`](../flags/dynamic-eplb.md) / [`enable_force_eplb`](../flags/enable-force-eplb.md)（additional-config）
  - MoE 通信优化：[`enable_fused_mc2`](../flags/enable-fused-mc2.md)、[`mc2_comm_alg`](../flags/mc2-comm-alg.md)

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enable-expert-parallel --data-parallel-size 4
```

## 相关参数

- [`--data-parallel-size`](data-parallel-size.md) — EP 的规模来源
- [`--tensor-parallel-size`](tensor-parallel-size.md) — 与 EP 共同决定专家分片
