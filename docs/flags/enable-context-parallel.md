---
title: enable_context_parallel
---

# `enable_context_parallel`

> 上下文并行开关。**已移除**，功能由 `enable_dsa_cp` 等接替。

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
