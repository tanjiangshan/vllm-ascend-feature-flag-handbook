---
title: multistream_overlap_gate
---

# `multistream_overlap_gate`

> 门控多流重叠。**已在 v0.30.0 移除**。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ **removed**（v0.30.0 移除） |

## 生命周期

- **v0.23.0**：配置键存在（仅对含共享专家的 MoE 模型有意义）；
- **v0.30.0 起**：源码与文档中均已移除。

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

共享专家优化仍可使用：

- [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) — 共享专家多流重叠（仍在）；
- [`enable_shared_expert_dp`](enable-shared-expert-dp.md) — 共享专家数据并行。
