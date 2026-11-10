---
title: finegrained_tp_config
---

# `finegrained_tp_config`

> 细粒度张量并行（Fine-Grained Tensor Parallelism）配置。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |

## 说明

将模型按模块（如 MLP、attention、embedding、LM Head）设置不同的 TP 并行粒度，替代全局统一的 TP size。相关字段（如 `embedding_tensor_parallel_size`、`mlp_tensor_parallel_size`、`oproj_tensor_parallel_size` 等）在 v0.23 起逐步收归到本配置下。

## 兼容性

- embedding / LM Head 的细粒度 TP 与 [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) **不兼容**（PCP size > 1 时二选一）。

具体字段清单以对应版本的官方文档为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ⚠️ 需注意 |
| PD 分离 | ✅ D 节点 |

官方 Fine-grained TP 指南：oproj/mlp_tensor_parallel_size>1 仅在 PD 分离 D 节点（kv_consumer）通过启动校验，且要求 recompute_scheduler_enable + PreemptOffloadConnector 组合；生产推荐拓扑即 PD 分离 D 节点。lmhead/embedding 子键限制较宽。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)
<!-- DEPLOY_END -->
