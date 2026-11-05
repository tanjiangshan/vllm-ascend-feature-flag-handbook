---
title: enable-expert-parallel
---

# `--enable-expert-parallel`

> Shard MoE layers with expert parallelism (EP) instead of tensor parallelism.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `False` |
| Category | Parallelism |

## Official definition

Use expert parallelism instead of tensor parallelism for MoE layers. (vLLM source: `ParallelConfig.enable_expert_parallel`)

## Ascend context & official usage

- **Enabled by default** in official MoE tutorials (DeepSeek-V4 family, Kimi-K3 family, GLM5.2, Qwen3.5-397B, MiniMax-M3, etc.), combined with `--data-parallel-size` for large-scale EP.
- Experts are sharded by TP × PCP × DP: larger EP means fewer experts per rank (less memory) but more cross-node communication.
- Ascend companion flags:
  - Dynamic expert balancing: [`dynamic_eplb`](../flags/dynamic-eplb.md) / [`enable_force_eplb`](../flags/enable-force-eplb.md) (via additional-config)
  - MoE communication: [`enable_fused_mc2`](../flags/enable-fused-mc2.md), [`mc2_comm_alg`](../flags/mc2-comm-alg.md)

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enable-expert-parallel --data-parallel-size 4
```

## Related args

- [`--data-parallel-size`](data-parallel-size.md)
- [`--tensor-parallel-size`](tensor-parallel-size.md)
