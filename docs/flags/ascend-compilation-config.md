---
title: ascend_compilation_config
---

# `ascend_compilation_config`

> Ascend 图编译配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |

## 说明

控制 vLLM-Ascend 的图编译行为（编译缓存、编译选项等）。典型用途：

- 固定编译缓存目录，加速服务重启后的图编译；
- 调整编译选项以适配特定模型结构或 CANN 版本。

具体子字段以对应版本的官方文档为准。
