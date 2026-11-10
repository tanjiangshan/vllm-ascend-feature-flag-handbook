---
title: pa_shape_list
---

# `pa_shape_list`

> page attention 算子的自定义 shape 列表。
> 📚 所属专题：[3. KV Cache 量化与内存格式](../feature-topics.md#t-kvfmt)

| 属性 | 值 |
|---|---|
| 类型 | `list` |
| 默认值 | `[]` |
| 状态 | ✅ active |

## 说明

向 page attention 算子注册自定义 shape 列表。官方配置文档原文仅一行："The custom shape list of page attention ops."；源码中仅见定义与默认值序列化，未见独立读取点。

- 留空（默认 `[]`）使用内置 shape 集合，**大多数部署无需设置**。
- 列表元素的具体格式未见官方文档说明；确需配置时建议先在测试环境验证。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
