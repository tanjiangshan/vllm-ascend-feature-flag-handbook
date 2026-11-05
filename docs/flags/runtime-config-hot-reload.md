---
title: runtime_config_hot_reload
---

# `runtime_config_hot_reload`

> Runtime Guard JSON 配置热重载开关。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（main 分支新增，下一版本发布） |

## 说明

启用后，Runtime Guard 允许在运行期重载 `runtime_config.json`，无需重启服务即可调整检测器与配额。

!!! note "仅启动时生效"
    该开关本身只在启动时读取一次；它不是 JSON 配置内的字段。

详见 [Runtime Guard 配置三件套](runtime-config.md)。
