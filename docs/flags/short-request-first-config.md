---
title: short_request_first_config
---

# `short_request_first_config`

> ShortRequestFirst：短请求优先的 prefill 调度策略。

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
