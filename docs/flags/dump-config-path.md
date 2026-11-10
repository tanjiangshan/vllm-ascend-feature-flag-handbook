---
title: dump_config_path
---

# `dump_config_path`

> msprobe dump 配置文件路径。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None` |
| 状态 | ✅ active |

## 说明

指定外部 msprobe dump 配置文件的路径（兼容旧版选项）。与 [`dump_config`](dump-config.md)（内联字典）二选一。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"dump_config_path": "/etc/vllm/msprobe_dump.json"}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
