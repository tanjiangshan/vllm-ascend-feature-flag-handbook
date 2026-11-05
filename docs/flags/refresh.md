---
title: refresh
---

# `refresh`

> 刷新全局 Ascend 配置内容。

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
