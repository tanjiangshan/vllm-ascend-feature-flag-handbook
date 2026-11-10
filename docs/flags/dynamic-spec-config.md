---
title: dynamic_spec_config
---

# `dynamic_spec_config`

> 动态投机解码（Dynamic Speculative Decoding）配置。
> 📚 所属专题：[7. 投机解码](../feature-topics.md#t-spec)

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |

## 说明

动态投机解码的参数入口：根据运行时状态自动调整投机解码的 draft 长度等参数，在收益与开销间自适应平衡，替代固定的投机解码配置。

具体子字段（如 `posterior_threshold`、`posterior_alpha` 等）以对应版本的官方文档与动态投机解码特性指南为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
