---
title: max-num-batched-tokens
---

# `--max-num-batched-tokens`

> 单次迭代最大可处理的 token 数，是 prefill 分块与调度批大小的核心旋钮。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（自动） |
| 分类 | 调度与内存 |

## 官方定义

Maximum number of tokens that can be processed in a single iteration.（vLLM 源码 `EngineArgs` / `SchedulerConfig`）

## Ascend 语境与官方用法

- 官方教程典型值：**1024（小模型）/ 10240 / 16384 / 20480 / 32768**（大模型），如 [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) 用 10240，[Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) 用 20480。
- **动态分块流水线并行（CPP）对该参数最敏感**（[dynamic_chunk_pipeline_parallel 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)）：
  - 固定分块调优的推荐搜索空间为 **[8192, 16384, 24576, 32768]**；
  - 开启动态分块时，最优值通常是固定分块最优值的 **2–4 倍**；
  - 序列越长，应设置越大的 `--max-num-batched-tokens`。
- 与特性开关联动：开 [`enable_prefill_mc2`](../flags/enable-prefill-mc2.md) 时官方建议该值 ≤ `tp_size × 512`。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-num-batched-tokens 16384
```

## 相关参数

- [`--max-num-seqs`](max-num-seqs.md) — 每迭代序列数上限
- [`--enable-chunked-prefill`](enable-chunked-prefill.md) — 分块 prefill 依赖该值切块
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend 动态分块配置
