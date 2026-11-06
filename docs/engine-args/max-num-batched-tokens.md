---
title: max-num-batched-tokens
---

# `--max-num-batched-tokens`

> 单次迭代最大可处理的 token 数——prefill 分块与调度批大小的**核心旋钮**。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（自动，按设备显存与用途分档解析，见下） |
| 分类 | 调度与内存 |

## 官方定义

> Maximum number of tokens that can be processed in a single iteration.

（vLLM 源码：`EngineArgs.max_num_batched_tokens`，[arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) / `SchedulerConfig.max_num_batched_tokens`，[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）

## 机制详解

**它在调度流水线中的位置**：每个调度步的可分配"token 预算"。调度器按预算把 RUNNING 请求拼进 batch：prefill 请求按剩余预算切块（chunked prefill），decode 请求每条每步至少占 1 个 token。预算用尽即停止本轮扩批。

**它与 `max_num_seqs` 的分工**：`max_num_seqs` 管"多少条"，`max_num_batched_tokens` 管"总共多少 token"。一条 8000 token 的长 prompt 可以在一个步内完成 prefill（预算够），也可以被切成 4 块跨 4 步处理（预算只有 2000）——块大小就是它。

**默认值解析**（CLI 不传时，由 [`get_batch_defaults()`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) 解析；两档分别对应离线 `LLM` 类与 API server 用途）：

| 设备显存 | LLM（离线） | OpenAI API server |
|---|---|---|
| ≥ 160 GB（B200/B300 等） | 16384 | 16384 |
| ≥ 70 GB 且非 A100（H100/H200 等） | 16384 | 8192 |
| 其他 | 8192 | 2048 |
| batched-DP MoE 特殊路径 | **256**（`DEFAULT_MAX_NUM_BATCHED_TOKENS_FOR_BATCHED_DP`） | 同左 |

用户未显式设置时的后续修正（[arg_utils.py `_set_default_max_num_seqs_and_batched_tokens_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)）：

1. `performance_mode = "throughput"` → 翻倍；
2. 未开 chunked prefill 时 → `max(解析值, max_model_len)`（保证单条能进）；
3. 钳制：`min(max_num_seqs × max_model_len, 解析值)`。

调度器实际下发的 token 数还可能更小：源码中的 `max_num_scheduled_tokens`（调度器每步真正发射的 token 上限）"通常等于 `max_num_batched_tokens`，但在模型会往 batch 里追加 token 的情况下（如投机解码）可以更小"（[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py) 字段说明）。

## 参数联动

**与 `max_num_seqs` 的硬约束**（启动校验，[scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）：

```
max_num_batched_tokens ≥ max_num_seqs    （不满足直接拒绝启动）
```

逻辑很直白：每条序列每步至少 1 个 token，条数不可能超过 token 数。

**与 `max_model_len` 的联动**：开启 chunked prefill 后，长 prompt 切块消化，因此 `max_num_batched_tokens` 可以远小于 `max_model_len`；**关闭** chunked prefill 时若 `max_num_batched_tokens < max_model_len`，启动直接报错。换言之：想用小预算跑长上下文，chunked prefill 必须开。

**与抢占的关系**：预算越大，单步内能同时推进的长请求越多，KV 池消耗越快；预算越小，长请求被拉长到更多步，单步 KV 增量小但排队久。两者失衡都会体现为 `vllm:num_preemptions` 上升。

**Ascend 专属联动**：开启 [`enable_prefill_mc2`](../flags/enable-prefill-mc2.md) 时，`max_num_batched_tokens` 被用于计算 mc2_token_capacity，官方建议此时**不超过 `tp_size × 512`**（[additional_config 官方配置表](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)）。

## 调优思路

| 目标 | 怎么调 |
|---|---|
| **TTFT 敏感** | 设为略大于典型 prompt 长度，让单条 prefill 一步完成 |
| **TPOT 敏感** | 适当调小，避免大块 prefill 挤占 decode 步；配合 chunked prefill 平滑混部 |
| **吞吐优先** | 调大（注意 `≥ max_num_seqs` 约束）；`performance_mode=throughput` 可让默认值翻倍 |
| **CPP 动态分块** | 先固定分块在 **[8192, 16384, 24576, 32768]** 中扫最优；再开动态分块，最优值通常是固定值的 **2–4 倍**（[官方 CPP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)） |

## Ascend 语境与官方用法

- 官方教程典型值：**1024（小模型）/ 10240 / 16384 / 20480 / 32768**。
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html)：10240
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html)：20480（配 `--max-num-seqs 64`）
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：1024
- **CPP（动态分块流水线并行）对该参数最敏感**：过大引入计算浪费，过小降低算子效率（官方指南原话）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-num-batched-tokens 16384
```

## 相关参数

- [`--max-num-seqs`](max-num-seqs.md) — 条数上限，必须 ≤ 本参数
- [`--enable-chunked-prefill`](enable-chunked-prefill.md) — 本参数是实际分块大小
- [`--max-model-len`](max-model-len.md) — 关闭 chunked prefill 时本参数不能小于它
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend 动态分块配置
