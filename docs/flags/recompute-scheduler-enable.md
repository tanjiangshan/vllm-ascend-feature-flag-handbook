---
title: recompute_scheduler_enable
---

# `recompute_scheduler_enable`

> 重计算调度器：PD 分离架构 D 节点上的显存节省方案。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（顶层键已弃用，请用 `scheduler_config.recompute_scheduler_enable`） |

!!! warning "节点类型限制"
    仅在 **PD 分离的 D 节点**（`kv_role = kv_consumer`，仅 decode）上有效。在 P 节点或 PD-mixed 模式下启用，**启动时会报明确错误并失败**。

## 作用

D 节点本地 prefill 路径（recompute / fallback / preempt）触发时，通过重计算调度策略降低 KV cache 与激活的显存占用，换取更长上下文或更大批次的承载能力。

## 推荐用法（v0.30.0+ 规范层级）

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"recompute_scheduler_enable": true}}'
```

## 迁移

| 迁移前 | 迁移后 |
|---|---|
| `{"recompute_scheduler_enable": true}`（顶层键） | `{"scheduler_config": {"recompute_scheduler_enable": true}}` |

顶层键过渡期仍兼容，与 `scheduler_config` 同时提供时以后者为准。

## 相关开关

- [scheduler_config](scheduler-config.md) — 规范层级
- [enable_balance_scheduling](enable-balance-scheduling.md) — 同层级调度开关
