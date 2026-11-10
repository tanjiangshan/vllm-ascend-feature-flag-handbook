---
title: enable_context_parallel
---

# `enable_context_parallel`

> 上下文并行开关。**已移除**，功能由 `enable_dsa_cp` 等接替。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ **removed** |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` |

## 生命周期

- **v0.18 及更早**：以环境变量 `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` 提供；
- **v0.23.0 起**：环境变量与配置键均已移除；
- **替代方案**：DeepSeek V3.2 / V4 等模型的上下文并行请使用 **`enable_dsa_cp`**（仅 MRv1 + 序列并行；MRv2 请用 PCP）。

## 升级指引

| 旧配置 | 新配置 |
|---|---|
| `export VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL=1` | `{"enable_dsa_cp": true}`（DSA 模型）或 PCP 方案 |

详见官方[上下文并行特性指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
