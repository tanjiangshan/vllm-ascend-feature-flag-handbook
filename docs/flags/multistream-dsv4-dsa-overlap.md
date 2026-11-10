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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
