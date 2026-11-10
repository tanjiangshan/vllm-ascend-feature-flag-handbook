---
title: dyntra_lb_config
---

# `dyntra_lb_config`

> DyntraLB：PD 分离架构 D 节点的负载均衡配置。
> 📚 所属专题：[2. 负载均衡与调度](../feature-topics.md#t-scheduling)

!!! warning \"顶层键已废弃\"
    v0.30.0 起该顶层键迁移至 `scheduler_config.<key>`，直接设置顶层键会收到 deprecation 警告。官方文档写法见 [`scheduler_config`](scheduler-config.md)。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 嵌套位置 | `scheduler_config.dyntra_lb_config` |

## 说明

在 PD（Prefill/Decode）分离部署中，动态将解码请求分发到负载更低的 D 节点，缓解请求倾斜导致的尾延迟。

具体子字段以对应版本的官方文档为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | — 不适用 |
| PD 分离 | ✅ D 节点 |

官方 DyntraLB 指南：仅在 PD 分离 D 节点（kv_role="kv_consumer"）开启，且要求 DP>1、DP ranks 同节点；「Do not add dyntra_lb_config with enabled=true to Prefill nodes」；不能与 enable_balance_scheduling / profiling_chunk_config 同开（启动拒绝）。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dyntra_lb.html)
<!-- DEPLOY_END -->
