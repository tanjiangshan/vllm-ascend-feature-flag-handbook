---
title: rejection_sampler_config
---

# `rejection_sampler_config`

> 拒绝采样器配置（RL 采样场景）。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | RL rollout / 投机解码验收 |

## 子键

| 子键 | 类型 | 说明 |
|---|---|---|
| `enable_block_verify` | bool | block 验证模式 |
| `enable_entropy_verify` | bool | 熵验证模式 |

## 说明

控制拒绝采样器的验证策略，用于 RL 训练中 rollout 样本的验收。常与 [`dynamic_spec_config`](dynamic-spec-config.md)、[`rl_config`](rl-config.md) 配合使用。
