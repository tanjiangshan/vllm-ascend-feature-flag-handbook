---
title: enable-chunked-prefill
---

# `--enable-chunked-prefill` / `--no-enable-chunked-prefill`

> 分块 prefill：长 prompt 按 `max_num_batched_tokens` 的剩余预算切块，跨多个调度步消化——长请求不再饿死 decode。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `None` → 按模型支持情况自动判断（支持的模型默认开启） |
| 分类 | 调度与内存 |

## 官方定义

> If True, prefill requests can be chunked based on the remaining `max_num_batched_tokens`.

（vLLM 源码：`SchedulerConfig.enable_chunked_prefill`，[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）

## 机制详解

**不分块的世界**：一条 32K token 的长 prompt 到来，scheduler 必须在一个步内为它腾 32K token 的预算——同刻所有 decode 请求都得排队。长请求一来，全场 TPOT 恶化。这就是"prefill 饿死 decode"。

**分块的世界**：长 prompt 按预算切块，一块一块跨步推进；块间正常穿插 decode 请求。两个后果：

- ✅ TPOT 平滑：decode 不再被长 prefill 长时间压制；
- ⚠️ TTFT 变长：长 prompt 的总 prefill 时间被拉长（块间要抢预算）。

**默认值的自动解析**（[arg_utils.py `_set_default_chunked_prefill_and_prefix_caching_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)）：

```
None → model_config.is_chunked_prefill_supported（支持则默认开）
```

即 main 上支持的模型**默认开启**。两条例外路径（同函数）：

- 对支持分块的模型**手动关闭** → 打 warning：*"This model does not officially support disabling chunked prefill... may cause the engine to crash or produce incorrect outputs"*；
- encoder-decoder 类模型源码自动禁用（[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)：disable_chunked_mm_input 分支）。

## 参数联动

**与 `max_num_batched_tokens`——分块大小就是它**：开分块后，"块"= 每步分给该请求的预算额度。调 `max_num_batched_tokens` 就是调块大小。

**与 `max_model_len` 的启动校验**（[scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）：

```
分块关闭时：max_num_batched_tokens < max_model_len → 启动报错
分块开启时：该约束解除（长序列可以切块消化）
```

这是长上下文部署几乎必开分块的原因：**用小预算跑长上下文的前提**。

**与抢占的关系**：分块让长请求的单步 KV 增量变小（每步只写一块），池子压力更平滑；`vllm:num_preemptions` 波动会小于不分块场景。

## 调优思路

| 场景 | 建议 |
|---|---|
| 长短请求混部（在线服务常态） | **保持开启**（默认） |
| TTFT 优先且 prompt 长度已知 | 可以关，但需保证 `max_num_batched_tokens ≥ max_model_len`（否则启动报错），且接受 decode 抖动 |
| CPP 动态分块（Ascend PP 场景） | 开分块是前提，再配 [`profiling_chunk_config`](../flags/profiling-chunk-config.md) 做动态块大小 |

## Ascend 语境与官方用法

- vLLM main 默认行为：支持的模型自动开。官方教程在**大模型长上下文**场景显式传 `--enable-chunked-prefill`（如 Qwen3.5-397B 系），配合大 `max_num_batched_tokens`（16384+）控制块大小。
- Ascend 的 **CPP（动态分块流水线并行）**建立在分块之上：分块大小即 `max_num_batched_tokens`，调优空间 [8192, 16384, 24576, 32768]（[官方 CPP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enable-chunked-prefill --max-num-batched-tokens 16384
```

## 相关参数

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — 实际块大小
- [`--max-model-len`](max-model-len.md) — 关闭分块时的启动约束
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend 动态分块配置
