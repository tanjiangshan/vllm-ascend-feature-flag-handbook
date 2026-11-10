---
title: enable_mlapo
---

# `enable_mlapo`

> MLAPO（Model Layer-wise Adaptive Parallel Optimization，模型逐层自适应并行优化）。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_MLAPO`（`"1"` → `true`） |

## 用法

```bash
# 关闭 MLAPO
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_mlapo": false}'
```

## 注意事项

- 默认开启，一般无需显式设置。排查精度或性能问题时，可临时关闭以做对照实验。
- 旧环境变量 `VLLM_ASCEND_ENABLE_MLAPO` 在新版本中不再受支持，请迁移至配置键。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ D 节点 |

Kimi-K2.6 与 GLM5 教程原文：「in PD scenarios enable MLAPO only on decode nodes」；混部高吞吐场景可用（GLM5 表「A3 co-located high-throughput / PD decode nodes」）；注意消耗更多 NPU 显存。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K2.6.html)
<!-- DEPLOY_END -->

## 相关开关

- 迁移信息见[迁移对照表](../migration.md)
