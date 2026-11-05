---
title: runtime_config / runtime_config_path / runtime_config_hot_reload
---

# Runtime Guard 配置三件套

> 运行时守护（Runtime Guard）的启动配置入口。

| 配置键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `runtime_config_path` | str | `None` | Runtime Guard JSON 配置路径，默认 `/runtime/config/runtime_config.json` |
| `runtime_config` | dict | `None` | 启动时叠加层，与运行时配置默认值合并（检测器、dump 配额、报告标志） |
| `runtime_config_hot_reload` | bool | `false` | 启用 `runtime_config.json` 热重载（仅启动时生效；不是 JSON 字段） |

## 说明

Runtime Guard 是 vLLM-Ascend 的运行时检测与保护机制。三者关系：

1. `runtime_config_path` 指定 JSON 配置文件位置；
2. `runtime_config` 以字典形式提供与文件合并的叠加配置（适合不便落盘的部署）；
3. `runtime_config_hot_reload` 允许运行期重载上述 JSON。

具体检测器与配额字段以对应版本的 Runtime Guard 特性文档为准。
