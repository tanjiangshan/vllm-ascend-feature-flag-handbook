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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
