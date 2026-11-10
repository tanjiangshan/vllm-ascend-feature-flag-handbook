---
title: pa_shape_list
---

# `pa_shape_list`

> page attention 算子的自定义 shape 列表。

| 属性 | 值 |
|---|---|
| 类型 | `list` |
| 默认值 | `[]` |
| 状态 | ✅ active |

## 说明

向 page attention 算子注册自定义的 shape 组合，用于算子预编译/亲和性优化。一般在官方默认 shape 覆盖不足、且通过 profiling 发现 attention 算子频繁走 fallback 路径时使用。

留空则使用内置默认 shape 集合，**大多数部署无需设置**。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
