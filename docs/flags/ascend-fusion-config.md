---
title: ascend_fusion_config
---

# `ascend_fusion_config`

> Ascend 融合算子配置，控制是否使用 GmmSwigluQuant 融合算子。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |
| 适用 | 全部 |

## 用法

```bash
vllm serve <model> \
  --additional-config='{"ascend_fusion_config": {"fusion_ops_gmmswigluquant": true}}'
```

## 子键

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `fusion_ops_gmmswigluquant` | `bool` | `true` | 是否启用 GmmSwigluQuant 融合算子（量化权重下使用） |

## 注意事项

- pydantic `extra="forbid"`：写错子键名会直接启动报错，不会静默忽略。
- 对非量化模型该算子可能不生效，显式设为 `false` 可在调试时关闭融合路径。

## 相关开关

- [`ascend_compilation_config`](ascend-compilation-config.md) — Ascend 编译配置
- [`combine_quant_mode`](combine-quant-mode.md) — Combine 通信量化模式（另一处融合算子开关）
