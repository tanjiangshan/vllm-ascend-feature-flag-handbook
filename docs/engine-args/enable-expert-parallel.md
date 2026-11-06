---
title: enable-expert-parallel
---

# `--enable-expert-parallel`

> MoE 层改用专家并行（EP）切分：每层专家分到多卡，替代默认的张量并行切分。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `False` |
| 分类 | 并行策略 |

## 官方定义

> Use expert parallelism instead of tensor parallelism for MoE layers.

（vLLM 源码：`ParallelConfig.enable_expert_parallel`，[parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)）

## 机制详解

**为什么 MoE 需要它**：大 MoE 模型的权重主体在专家 FFN 里（专家数多、单层参数量大）。默认 TP 切法会把**每个专家**都横切到所有 TP 卡上——显存按 1/TP 省，但每个 token 的专家计算都要跨卡 all-reduce，且 TP 超过 KV 头数后 attention 侧不再省显存（见 [`tensor-parallel-size`](tensor-parallel-size.md)）。

EP 换成另一种切法：**专家整体分给不同卡**（配合 DP 的 TP×PCP×DP 乘积分片），每个 token 只路由到本卡的少数专家。跨卡通信从"每层两次 all-reduce"变成"按路由的 dispatch/combine"。

**源码硬约束**（[model.py `_verify_with_expert_parallelism`](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）：

```
enable_expert_parallel 时模型必须 is_moe（专家数 > 0），否则 ValueError
```

对 Dense 模型开这个参数会直接启动失败。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--data-parallel-size`](data-parallel-size.md) | 专家按 **TP × PCP × DP** 乘积分片——DP 是 EP 规模的主调节量 |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | 与 DP 相乘决定每 rank 专家数 |
| Ascend [`enable_fused_mc2`](../flags/enable-fused-mc2.md) / [`mc2_comm_alg`](../flags/mc2-comm-alg.md) | MoE dispatch/combine 通信的融合与算法选择 |
| Ascend [`dynamic_eplb`](../flags/dynamic-eplb.md) / [`enable_force_eplb`](../flags/enable-force-eplb.md) | 专家负载均衡（EPLB） |
| Ascend [`mega_moe_max_tokens`](../flags/index.md) | 融合 MC2/MegaMoe 路径的每 rank token 容量上限 |

**代价要说清**：EP 把通信模式从"每层固定 all-reduce"变成"按 token 路由的 all-to-all"，负载不均是天然风险——路由热点卡会先顶到算力上限，这就是 EPLB 系列开关存在的原因。

## Ascend 语境与官方用法

- 官方 MoE 教程（DeepSeek-V4 全系、Kimi-K3 系、GLM5.2、Qwen3.5-397B、MiniMax-M3 等）**默认开启**，与 `--data-parallel-size N --tensor-parallel-size M` 组合（M×DP 决定每 rank 专家数）。
- 官方教程的 MoE 通信优化多走 [`enable_fused_mc2`](../flags/enable-fused-mc2.md)（dispatch-FFN-combine 融合）与 `mc2_comm_alg`。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enable-expert-parallel --data-parallel-size 4
```

## 相关参数

- [`--data-parallel-size`](data-parallel-size.md) — EP 的规模来源（专家分片乘积因子）
- [`--tensor-parallel-size`](tensor-parallel-size.md) — 与 DP 相乘决定每 rank 专家数
- [`enable_fused_mc2`](../flags/enable-fused-mc2.md) — MoE 通信融合（Ascend 特性开关）
