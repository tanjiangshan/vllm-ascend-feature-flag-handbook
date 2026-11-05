---
title: enable_kv_nz
---

# `enable_kv_nz`

> KV cache 的 NZ 布局开关。注意与权重 NZ（[`weight_nz_mode`](weight-nz-mode.md)）是两个独立开关。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | 使用 MLA 的模型（如 DeepSeek 系列） |

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3 \
  --additional-config='{"enable_kv_nz": true}'
```

## 注意事项

- **仅对 MLA 模型生效**，非 MLA 架构开启无效果；
- KV cache 布局变化会影响 attention 算子的亲和性，建议与 [`weight_nz_mode`](weight-nz-mode.md) 联合调优并实测对比；
- 开启后 KV cache 内存占用与传输带宽特性会变化，长上下文场景请重点验证。

## 相关开关

- [weight_nz_mode](weight-nz-mode.md) — 权重 NZ（独立开关）
