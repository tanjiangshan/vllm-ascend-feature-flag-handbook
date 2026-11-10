---
title: runtime_report_dir
---

# `runtime_report_dir`

> Runtime Guard 报告根目录覆盖。
> 📚 所属专题：[8. 稳定性与监控：Runtime Guard](../feature-topics.md#t-guard)

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（默认 `/runtime/report`） |
| 状态 | ✅ active |

## 说明

覆盖 Runtime Guard 的报告输出根目录。`runtime_dump_dir` 未显式设置时，dump 目录由本目录派生。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"runtime_report_dir": "/data/runtime/report"}'
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
