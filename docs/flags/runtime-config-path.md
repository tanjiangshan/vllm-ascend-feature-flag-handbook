---
title: runtime_config_path
---

# `runtime_config_path`

> Runtime Guard JSON 配置文件路径。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（实际默认 `/runtime/config/runtime_config.json`） |
| 状态 | ✅ active（main 分支新增，下一版本发布） |

## 说明

指定 Runtime Guard 的 JSON 配置文件位置。配置内容包括检测器（detectors）、dump 配额、报告标志等。

详见 [Runtime Guard 配置三件套](runtime-config.md)。
