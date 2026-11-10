---
title: enable_prefill_mc2
---

# `enable_prefill_mc2`

> 为 prefill 批次预留 MC2 token 容量。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（**临时开关**） |

## 作用

默认情况下 `mc2_token_capacity` 按 decode 容量计算。启用本开关后，改用 `max_num_batched_tokens` 计算，为 prefill 批次预留 MC2 容量。

!!! note "临时开关"
    一旦 MC2 算子在所有场景下完备，本开关将被移除且 MC2 默认启用。请勿在长期配置中依赖它。

## 使用约束

启用本开关时，`max_num_batched_tokens` 的**推荐最大值为 `tp_size * 512`**，超出可能导致容量规划失效。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --tensor-parallel-size 4 \
  --max-num-batched-tokens 2048 \
  --additional-config='{"enable_prefill_mc2": true}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ P 节点 |

语义即「为 prefill batch 预留 mc2_token_capacity」；Qwen3.8-Flash-Next 配方 P 节点开启、D 节点不配。官方注明是临时开关，MC2 算子补全后移除。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.8-Flash-Next.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_fused_mc2](enable-fused-mc2.md) — 融合 MC2 路径总开关
- [mega_moe_max_tokens](mega-moe-max-tokens.md) — 每 rank token 容量
