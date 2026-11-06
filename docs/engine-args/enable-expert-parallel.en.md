---
title: enable-expert-parallel
---

# `--enable-expert-parallel`

> Shard MoE layers with expert parallelism (EP): experts are distributed across devices instead of being tensor-parallel-sliced.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `False` |
| Category | Parallelism |

## Official definition

> Use expert parallelism instead of tensor parallelism for MoE layers.

(vLLM source: `ParallelConfig.enable_expert_parallel`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py))

## How it works

**Why MoE needs it**: the weight bulk of a large MoE model lives in the expert FFNs (many experts, large per-layer parameter count). The default TP slicing splits **every expert** across all TP devices — memory shrinks by 1/TP, but expert compute for every token needs a cross-device all-reduce, and once TP exceeds the KV head count, the attention side stops saving memory (see [`tensor-parallel-size`](tensor-parallel-size.md)).

EP switches the approach: **whole experts are assigned to different devices** (sharded by the TP × PCP × DP product with DP), and each token routes only to a few experts on the local device. Cross-device communication changes from "two all-reduces per layer" to "routing-driven dispatch/combine".

**Source hard constraint** ([model.py `_verify_with_expert_parallelism`](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)):

```
with enable_expert_parallel, the model must be is_moe (num experts > 0),
otherwise ValueError
```

Enabling this on a Dense model fails at startup.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--data-parallel-size`](data-parallel-size.md) | experts sharded by the **TP × PCP × DP** product — DP is the main EP scale knob |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | multiplies with DP to set per-rank expert count |
| Ascend [`enable_fused_mc2`](../flags/enable-fused-mc2.md) / [`mc2_comm_alg`](../flags/mc2-comm-alg.md) | fused MoE dispatch/combine and its communication algorithm |
| Ascend [`dynamic_eplb`](../flags/dynamic-eplb.md) / [`enable_force_eplb`](../flags/enable-force-eplb.md) | expert load balancing (EPLB) |
| Ascend [`mega_moe_max_tokens`](../flags/index.md) | per-rank token capacity cap for the fused MC2/MegaMoe path |

**The cost, said plainly**: EP changes the communication pattern from "fixed all-reduce per layer" to "routing-driven all-to-all", and load imbalance is an inherent risk — a routing-hot device hits its compute ceiling first. That is exactly why the EPLB flag family exists.

## Ascend context & official usage

- **Enabled by default** in official MoE tutorials (DeepSeek-V4 family, Kimi-K3 family, GLM5.2, Qwen3.5-397B, MiniMax-M3, etc.), combined with `--data-parallel-size N --tensor-parallel-size M` (M×DP sets per-rank expert count).
- Official MoE communication optimization goes through [`enable_fused_mc2`](../flags/enable-fused-mc2.md) (dispatch-FFN-combine fusion) and `mc2_comm_alg`.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enable-expert-parallel --data-parallel-size 4
```

## Related args

- [`--data-parallel-size`](data-parallel-size.md) — EP scale source (expert sharding product factor)
- [`--tensor-parallel-size`](tensor-parallel-size.md) — multiplies with DP for per-rank expert count
- [`enable_fused_mc2`](../flags/enable-fused-mc2.md) — MoE communication fusion (Ascend flag)
