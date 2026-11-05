---
title: multistream_overlap_shared_expert
---

# `multistream_overlap_shared_expert`

> 共享专家计算与主流程的多流重叠。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | 含共享专家的 MoE 模型 |

## 作用

将共享专家的计算调度到独立 NPU 流上，与 MoE 路由专家的主计算流并行执行，掩盖共享专家的计算延迟。

!!! note "模型限制"
    仅对**含共享专家的 MoE 模型**生效；无共享专家的模型开启后无任何效果。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"multistream_overlap_shared_expert": true}'
```

## 相关开关

- [enable_shared_expert_dp](enable-shared-expert-dp.md) — 共享专家数据并行（正交，可组合）
- [dynamic_eplb](dynamic-eplb.md) — 专家负载均衡
