---
title: rejection_sampler_config
---

# `rejection_sampler_config`

> 拒绝采样器配置（RL 采样场景）。
> 📚 所属专题：[9. 训练与 RL](../feature-topics.md#t-rl)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
