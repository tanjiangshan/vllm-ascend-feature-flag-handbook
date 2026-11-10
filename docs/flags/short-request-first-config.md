---
title: short_request_first_config
---

# `short_request_first_config`

> ShortRequestFirst：短请求优先的 prefill 调度策略。

!!! warning \"顶层键已废弃\"
    v0.30.0 起该顶层键迁移至 `scheduler_config.<key>`，直接设置顶层键会收到 deprecation 警告。官方文档写法见 [`scheduler_config`](scheduler-config.md)。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |
| 嵌套位置 | `scheduler_config.short_request_first_config` |

## 适用场景

FCFS 同步/异步、PD-prefill（P 节点）或 PD-mixed 节点上的 prefill 调度：将短请求优先调度，降低短请求的排队延迟，改善 TTFT 分布。

## 迁移

过渡期顶层键 `short_request_first_config` 仍兼容但已弃用，推荐迁移至 `scheduler_config` 下：

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"short_request_first_config": {}}}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ P 节点 |

官方 ShortRequestFirst 指南：支持普通部署、PD 分离 P 节点与 PD 混部；「not supported … on PD-disaggregated D nodes」；不依赖 recompute_scheduler_enable。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/short_request_first.html)
<!-- DEPLOY_END -->
