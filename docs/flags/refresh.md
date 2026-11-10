---
title: refresh
---

# `refresh`

> 刷新全局 Ascend 配置内容。
> 📚 所属专题：[9. 训练与 RL](../feature-topics.md#t-rl)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |

## 说明

每次初始化时重新加载并刷新全局 Ascend 配置，而不是沿用进程内缓存的旧配置。

**典型使用场景**：

- **RLHF**：rollout 与训练交替进行时，确保每轮推理拿到最新配置；
- **ut / e2e 测试**：测试用例间需要隔离配置副作用。

常规在线服务无需开启。[`rl_config`](rl-config.md) 的 `enabled: true` 会隐式强制此行为。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
