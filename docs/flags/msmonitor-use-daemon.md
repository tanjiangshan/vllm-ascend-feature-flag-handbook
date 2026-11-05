---
title: msmonitor_use_daemon
---

# `msmonitor_use_daemon`

> msmonitor 的守护进程模式开关。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 旧环境变量 | `MSMONITOR_USE_DAEMON`（`"1"` → `true`） |

## 作用

控制 Ascend 监控组件 msmonitor 是否以守护进程方式运行。守护进程模式适合长时间服务监控；短暂调试任务可用默认模式。

## 迁移

| 迁移前 | 迁移后 |
|---|---|
| `export MSMONITOR_USE_DAEMON=1` | `{"msmonitor_use_daemon": true}` |
