---
title: profiling_chunk_config
---

# `profiling_chunk_config`

> 动态分块流水线并行（profiling chunk）配置。**main 分支已移除该特性**，见[版本历史](../version-history.md)。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

!!! warning "顶层键已废弃（v0.30.0）；main 已移除"
    v0.30.0 起该顶层键迁移至 `scheduler_config.<key>`，直接设置顶层键会收到 deprecation 警告。官方文档写法见 [`scheduler_config`](scheduler-config.md)。**main 分支 ascend_config.py 已无 profiling_chunk 读取点，官方功能页同步从 main 文档删除**——新部署请勿依赖该特性。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ⚠️ deprecated（v0.30.0 顶层键废弃；main 已移除） |
| 嵌套位置 | `scheduler_config.profiling_chunk_config`（v0.30.0 起） |

## 说明

面向流水线并行的动态分块调度：按 profiling 结果动态切分 micro-batch，平衡各 stage 的执行时间。

过渡期内顶层键 `profiling_chunk_config` 仍兼容但已弃用，推荐迁移至 `scheduler_config` 下：

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"profiling_chunk_config": {}}}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ P 节点 |

要求 pipeline-parallel-size>1；GLM5.2 配方在 P 节点（kv_producer）开启；不能与 dyntra_lb_config / enable_balance_scheduling 同开，可与 ShortRequestFirst 组合。

[出处](https://docs.vllm.ai/projects/ascend/en/v0.30.0/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)
<!-- DEPLOY_END -->
