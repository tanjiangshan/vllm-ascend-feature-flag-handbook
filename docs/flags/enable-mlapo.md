---
title: enable_mlapo
---

# `enable_mlapo`

> MLAPO（Model Layer-wise Adaptive Parallel Optimization，模型逐层自适应并行优化）。

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

## 相关开关

- 迁移信息见[迁移对照表](../migration.md)
