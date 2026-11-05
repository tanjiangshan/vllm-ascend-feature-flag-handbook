---
title: multistream_overlap_gate
---

# `multistream_overlap_gate`

> 门控多流重叠。**已在 v0.30.0 移除**。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ **removed**（v0.30.0 移除） |

## 生命周期

- **v0.23.0**：配置键存在（仅对含共享专家的 MoE 模型有意义）；
- **v0.30.0 起**：源码与文档中均已移除。

## 相关开关

共享专家优化仍可使用：

- [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) — 共享专家多流重叠（仍在）；
- [`enable_shared_expert_dp`](enable-shared-expert-dp.md) — 共享专家数据并行。
