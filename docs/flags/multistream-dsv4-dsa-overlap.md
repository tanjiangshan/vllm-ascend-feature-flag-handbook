---
title: multistream_dsv4_dsa_overlap
---

# `multistream_dsv4_dsa_overlap`

> DeepSeek V4 的 DSA 多流重叠优化。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active |
| 适用 | DeepSeek V4 架构模型 |

## 说明

默认开启。将 DSA（DeepSeek Sparse Attention）相关计算调度到独立 NPU 流上与主流程重叠，降低稀疏注意力对端到端延迟的影响。

非 DeepSeek V4 模型开启无效果；排查 DSA 精度问题时可临时关闭做对照。
