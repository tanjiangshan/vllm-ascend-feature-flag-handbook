---
title: dump_config
---

# `dump_config`

> 内联 msprobe dump 配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `None` |
| 状态 | ✅ active |

## 说明

以字典形式直接提供 msprobe dump 配置。vLLM-Ascend 会将其物化为临时 JSON 文件并传给调试器，适合不便落盘临时文件的场景。

与 [`dump_config_path`](dump-config-path.md)（指定外部配置文件）二选一。
