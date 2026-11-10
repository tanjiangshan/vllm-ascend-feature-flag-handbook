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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
