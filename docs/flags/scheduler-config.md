---
title: scheduler_config
---

# `scheduler_config`

> Ascend 调度器扩展配置的**规范层级**（v0.30.0 新增）。均衡调度、重计算调度、DyntraLB、ShortRequestFirst、动态分块流水线并行等开关的统一入口。
> 📚 所属专题：[2. 负载均衡与调度](../feature-topics.md#t-scheduling)

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |

## 子键

| 子键 | 类型 | 默认值 | 说明 | 详情页 |
|---|---|---|---|---|
| `enable_balance_scheduling` | bool | `false` | 均衡调度 | [enable_balance_scheduling](enable-balance-scheduling.md) |
| `recompute_scheduler_enable` | bool | `false` | 重计算调度器（仅 PD 分离 D 节点） | [recompute_scheduler_enable](recompute-scheduler-enable.md) |
| `short_request_first_config` | dict | `{}` | ShortRequestFirst prefill 调度 | [short_request_first_config](short-request-first-config.md) |
| `profiling_chunk_config` | dict | `{}` | 动态分块流水线并行 | [profiling_chunk_config](profiling-chunk-config.md) |
| `batch_job_sched_config` | dict | `{}` | batch-job-aware 调度 | [batch_job_sched_config](batch-job-sched-config.md) |
| `dyntra_lb_config` | dict | `{}` | PD 分离 D 节点负载均衡 | [dyntra_lb_config](dyntra-lb-config.md) |

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"enable_balance_scheduling": true, "recompute_scheduler_enable": false}}'
```

## 迁移背景

PR #9064 迁移期，以下**顶层键仍兼容但已弃用**，未来版本移除：

- `enable_balance_scheduling`
- `recompute_scheduler_enable`
- `short_request_first_config`
- `profiling_chunk_config`

!!! note "优先级"
    过渡期若同一字段顶层键与 `scheduler_config` 都提供，**以 `scheduler_config` 内的值为准**。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 双端 |

聚合键，放置由子键决定：recompute_scheduler_enable 仅 D、short_request_first_config 仅 P/混部、dyntra_lb_config 仅 D、enable_balance_scheduling 仅混部、profiling_chunk_config 见 P 侧实证。详见各子键详情页。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_balance_scheduling](enable-balance-scheduling.md) — 顶层旧键（deprecated）
- [recompute_scheduler_enable](recompute-scheduler-enable.md) — 顶层旧键（deprecated）
