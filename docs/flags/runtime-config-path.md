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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
