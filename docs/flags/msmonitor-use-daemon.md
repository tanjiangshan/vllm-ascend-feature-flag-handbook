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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
