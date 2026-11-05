---
title: batch_job_sched_config
---

# `batch_job_sched_config`

> batch-job-aware 调度器配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 嵌套位置 | `scheduler_config.batch_job_sched_config` |

## 说明

面向批量作业场景的调度策略：识别并按批组织请求，提升批量推理的整体吞吐与公平性。适用于离线批处理与准在线混合负载。

具体子字段以对应版本的官方文档为准。
