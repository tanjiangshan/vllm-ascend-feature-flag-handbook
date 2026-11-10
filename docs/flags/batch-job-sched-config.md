---
title: batch_job_sched_config
---

# `batch_job_sched_config`

> batch-job-aware 调度器配置。

!!! warning \"顶层键已废弃\"
    v0.30.0 起该顶层键迁移至 `scheduler_config.<key>`，直接设置顶层键会收到 deprecation 警告。官方文档写法见 [`scheduler_config`](scheduler-config.md)。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 嵌套位置 | `scheduler_config.batch_job_sched_config` |

## 说明

面向批量作业场景的调度策略：识别并按批组织请求，提升批量推理的整体吞吐与公平性。适用于离线批处理与准在线混合负载。

具体子字段以对应版本的官方文档为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见混部/PD 分离说明；已知约束：与 ShortRequestFirst 不可组合（batch-job-aware 调度下不安装 ShortRequestFirst 等待队列）。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/short_request_first.html)
<!-- DEPLOY_END -->
