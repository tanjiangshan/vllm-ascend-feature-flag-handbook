---
title: weight_prefetch_config
---

# `weight_prefetch_config`

> 权重预取配置。**已在 v0.30.0 移除**。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ❌ **removed**（v0.30.0 移除） |

## 生命周期

- **v0.23.0 及更早**：作为顶层配置键提供权重预取能力；
- **v0.30.0 起**：源码与文档中均已移除。

## 升级指引

升级到 v0.30.0+ 时，请从配置中删除 `weight_prefetch_config`。权重加载阶段的性能优化可关注 v0.30.0 新增的 [`ascend_warmup_config`](ascend-warmup-config.md)（启动预热与权重加载重叠）。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
