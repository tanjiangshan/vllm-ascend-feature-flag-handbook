---
title: dynamic_spec_config
---

# `dynamic_spec_config`

> 动态投机解码（Dynamic Speculative Decoding）配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |

## 说明

动态投机解码的参数入口：根据运行时状态自动调整投机解码的 draft 长度等参数，在收益与开销间自适应平衡，替代固定的投机解码配置。

具体子字段（如 `posterior_threshold`、`posterior_alpha` 等）以对应版本的官方文档与动态投机解码特性指南为准。
