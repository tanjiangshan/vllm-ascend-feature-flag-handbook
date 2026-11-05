---
title: enable-chunked-prefill
---

# `--enable-chunked-prefill` / `--no-enable-chunked-prefill`

> 分块 prefill：长 prompt 按 `max_num_batched_tokens` 的剩余额度切成多块调度，避免长请求饿死 decode。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `None`（vLLM main `SchedulerConfig.enable_chunked_prefill = True`，默认开启） |
| 分类 | 调度与内存 |

## 官方定义

If True, prefill requests can be chunked based on the remaining `max_num_batched_tokens`.（vLLM 源码 `SchedulerConfig`）

## Ascend 语境与官方用法

- vLLM main 默认开启；encoder-decoder 模型自动禁用（vLLM 源码 `scheduler.py`）。
- 官方教程显式传 `--enable-chunked-prefill` 的场景：大模型长上下文（如 Qwen3.5-397B 系），配合 [`--max-num-batched-tokens`](max-num-batched-tokens.md) 控制块大小。
- 与 **CPP 动态分块流水线并行**联动：分块大小即 `max_num_batched_tokens`，调优空间 [8192, 16384, 24576, 32768]（[CPP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enable-chunked-prefill --max-num-batched-tokens 16384
```

## 相关参数

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — 实际块大小
- [`--long-prefill-token-threshold`](index.md) — 长请求判定阈值
