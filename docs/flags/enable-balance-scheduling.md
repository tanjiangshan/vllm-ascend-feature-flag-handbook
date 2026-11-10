---
title: enable_balance_scheduling
---

# `enable_balance_scheduling`

> 均衡调度：在多实例/多节点场景下平衡请求分布。
> 📚 所属专题：[2. 负载均衡与调度](../feature-topics.md#t-scheduling)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 仅 PD 混部 |

设计文档注明「supports PD-mixed mode only」；GLM5 优化表：适用 A3 单节点/共置/非 PD 场景，「not recommended when Prefill-Decode is separated」。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html)
<!-- DEPLOY_END -->

## 相关开关

- [`recompute_scheduler_enable`](recompute-scheduler-enable.md) — 同位于 `scheduler_config` 下的重计算调度
