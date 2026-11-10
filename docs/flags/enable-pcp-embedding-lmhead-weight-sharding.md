---
title: enable_pcp_embedding_lmhead_weight_sharding
---

# `enable_pcp_embedding_lmhead_weight_sharding`

> PCP 组内 embedding 与 LM Head 权重分片（v0.30.0 新增）。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | PCP size > 1 时生效 |

## 作用

在每个 TP 分片内部，将 embedding 和 LM Head 权重进一步跨 PCP rank 分片，降低这两个大权重模块的显存占用。

## 不兼容性

!!! warning "与以下特性互斥"
    - batch-sharded sampling（`enable_batch_sharded_sampling`）；
    - 这两个模块的细粒度 TP（[`finegrained_tp_config`](finegrained-tp-config.md)）。

    同时启用会冲突，部署前需确认组合。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->

## 相关开关

- [enable_pcp_o_proj_weight_sharding](enable-pcp-o-proj-weight-sharding.md) — O 投影分片
- [finegrained_tp_config](finegrained-tp-config.md) — 细粒度 TP
