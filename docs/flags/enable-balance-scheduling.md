---
title: enable_balance_scheduling
---

# `enable_balance_scheduling`

> 均衡调度：在多实例/多节点场景下平衡请求分布。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ⚠️ **deprecated（顶层键已弃用）** |
| 旧环境变量 | `VLLM_ASCEND_BALANCE_SCHEDULING` |
| 规范位置 | `scheduler_config.enable_balance_scheduling` |

!!! warning "已弃用"
    PR #9064 起，本键迁移至 `scheduler_config.enable_balance_scheduling`。过渡期顶层键仍可用，但会在未来版本移除；两种格式同时提供时以 `scheduler_config` 为准。移除计划见 [issue #10381](https://github.com/vllm-project/vllm-ascend/issues/10381)。main 分支环境变量已清理完毕。

## 版本支持

| 版本 | 顶层键 | 环境变量 | `scheduler_config` 子键 |
|---|---|---|---|
| v0.23.0 | ✅ | ✅ `VLLM_ASCEND_BALANCE_SCHEDULING` | —（scheduler_config 未引入） |
| v0.30.0 | ✅（deprecated） | ✅（deprecated） | ✅ **推荐** |
| main | ✅（deprecated） | ❌ 已移除 | ✅ **推荐** |

## 推荐用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"enable_balance_scheduling": true}}'
```

## 迁移对照

| 迁移前 | 迁移后 |
|---|---|
| `export VLLM_ASCEND_BALANCE_SCHEDULING=1` | `{"scheduler_config": {"enable_balance_scheduling": true}}` |
| `{"enable_balance_scheduling": true}`（顶层键） | `{"scheduler_config": {"enable_balance_scheduling": true}}` |

详见[迁移对照表](../migration.md)。

## 相关开关

- [`recompute_scheduler_enable`](recompute-scheduler-enable.md) — 同位于 `scheduler_config` 下的重计算调度
