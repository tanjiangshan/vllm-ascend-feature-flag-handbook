---
title: pa_shape_list
---

# `pa_shape_list`

> page attention 算子的自定义 shape 列表。

| 属性 | 值 |
|---|---|
| 类型 | `list` |
| 默认值 | `[]` |
| 状态 | ✅ active |

## 说明

向 page attention 算子注册自定义的 shape 组合，用于算子预编译/亲和性优化。一般在官方默认 shape 覆盖不足、且通过 profiling 发现 attention 算子频繁走 fallback 路径时使用。

留空则使用内置默认 shape 集合，**大多数部署无需设置**。
