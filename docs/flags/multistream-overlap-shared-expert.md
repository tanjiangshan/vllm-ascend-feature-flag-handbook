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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 双端 |

Kimi-K2.6：TP=1 或 enable_shared_expert_dp 时启用额外流重叠 shared-expert 计算；Kimi-K3 配方按侧区分（P false / D true）；GLM5 表列为 A3 通用优化。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K2.6.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_shared_expert_dp](enable-shared-expert-dp.md) — 共享专家数据并行（正交，可组合）
- [dynamic_eplb](dynamic-eplb.md) — 专家负载均衡
