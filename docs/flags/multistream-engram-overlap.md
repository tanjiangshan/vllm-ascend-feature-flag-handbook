---
title: multistream_engram_overlap
---

# `multistream_engram_overlap`

> Engram 模块多流重叠，把 Engram 子模块的计算与通信分配到多条 NPU 流并行执行。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | 硬件派生（A5 默认 `true`，其余 `false`） |
| 状态 | ✅ active |
| 适用 | DeepSeek V4.1 等 Engram 模型 |

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V4.1 \
  --additional-config='{"multistream_engram_overlap": false}'  # 显式关闭 A5 默认开启的重叠
```

## 注意事项

- **默认策略因硬件而异**：仅 A5（FP8 优化设备家族）默认开启；显式设置会覆盖默认策略。
- FULL 图需在消费者侧等待描述符相关的外部事件，与 [`multistream_dsv4_dsa_overlap`](multistream-dsv4-dsa-overlap.md) 等图捕获行为叠加时需注意调度顺序。
- 仅 Engram 模型（如 DeepSeek V4.1）有该模块，其他模型开启无效果。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

仅见 DeepSeek-V4.1-Flash P 配方显式置 false，未见部署形态语义说明。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4.1-Flash.html)
<!-- DEPLOY_END -->

## 相关开关

- [`multistream_dsv4_dsa_overlap`](multistream-dsv4-dsa-overlap.md) — DSV4 DSA 多流重叠
- [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) — 共享专家多流重叠
