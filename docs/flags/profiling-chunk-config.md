---
title: profiling_chunk_config
---

# `profiling_chunk_config`

> 动态分块流水线并行（profiling chunk）配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |
| 嵌套位置 | `scheduler_config.profiling_chunk_config`（v0.30.0 起） |

## 说明

面向流水线并行的动态分块调度：按 profiling 结果动态切分 micro-batch，平衡各 stage 的执行时间。

过渡期内顶层键 `profiling_chunk_config` 仍兼容但已弃用，推荐迁移至 `scheduler_config` 下：

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"profiling_chunk_config": {}}}'
```
