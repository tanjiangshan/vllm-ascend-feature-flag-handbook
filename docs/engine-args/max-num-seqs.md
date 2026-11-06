---
title: max-num-seqs
---

# `--max-num-seqs`

> 单次迭代最大处理的序列数——推理引擎的**并发闸门**。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（自动，按设备显存分档解析，见下） |
| 分类 | 调度与内存 |

## 官方定义

> Maximum number of sequences to be processed in a single iteration.

（vLLM 源码：`EngineArgs.max_num_seqs`，[arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) / `SchedulerConfig.max_num_seqs`，[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）

## 机制详解

**它在调度流水线中的位置**：每个调度步（scheduler step），调度器从 RUNNING 队列中挑选序列组成 batch，`max_num_seqs` 就是这个 batch 的**条数上限**。它是硬上限——即使 KV cache 还装得下，调度器也不会超过这个数放请求。

**它不只影响调度，还影响运行时的资源预分配**。vLLM 源码对相邻参数 `max_num_active_seqs` 的说明写得很直白：

> `max_num_seqs` sizes the model runner (per-request buffers and CUDA graph capture) and is also the default admission limit.

即：`max_num_seqs` 决定了 model runner 的**每请求缓冲区大小**和 **CUDA Graph 捕获尺寸**。所以调大它不是"免费的"——图捕获内存和运行时 buffer 都会随之增长；这也解释了为什么捕获尺寸公式里会出现它（见下文细粒度 TP 联动）。

**默认值到底是多少**（CLI 不传时，`EngineArgs.max_num_seqs = None`，由 [`get_batch_defaults()`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) 按设备显存分档解析）：

| 设备显存 | 解析结果 |
|---|---|
| ≥ 160 GB（B200/B300 等） | **1024** |
| ≥ 70 GB 且非 A100（H100/H200 等） | **1024** |
| 其他（含 A100、小显存卡、设备查询失败） | **256** |

解析后还有两步修正（同函数内，[arg_utils.py `_set_default_max_num_seqs_and_batched_tokens_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)）：

1. `performance_mode = "throughput"` 时，用户未显式设置的两项默认值**翻倍**（吞吐模式专用）；
2. 最终钳制：`max_num_seqs = min(max_num_seqs, max_num_batched_tokens)`——每迭代条数不可能超过每迭代 token 数。

## 参数联动

把推理引擎想象成一个工厂：

| 参数 | 工厂类比 | 控制维度 | 默认值（vLLM main） |
|---|---|---|---|
| `--max-num-seqs` | 流水线上同时放的工件数 | **条数**：每步并发序列上限 | 256 / 1024（按显存分档，见上） |
| [`--max-num-batched-tokens`](max-num-batched-tokens.md) | 每个节拍加工的材料量 | **token 数**：每步计算量上限 | 2048–16384（按显存与用途分档） |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | 厂房面积 | **显存**：KV cache 池的大小来源 | 0.92 / 1.0（可扩展 KV 时） |
| [`--max-model-len`](max-model-len.md) | 单件工件的最大尺寸 | **长度**：单序列上下文上限 | 从模型 config 自动推断 |

**核心公式**——实际可达并发数：

```
实际并发 ≈ min(max_num_seqs, KV cache 池容量 ÷ 平均上下文长度)
```

KV cache 池容量由 `gpu-memory-utilization` 决定（显存减去权重与激活后的剩余）。即使把 `max_num_seqs` 调得很大，KV 池放不下时并发照样上不去——多余的请求会在队列里等待，或触发抢占。

**源码强制的两条启动校验**（[`SchedulerConfig.verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)，不满足直接拒绝启动）：

1. `max_num_batched_tokens < max_num_seqs` → 报错：*"max_num_batched_tokens must be greater than or equal to max_num_seqs"*。每步 token 数不可能比条数还少（每条至少 1 个 token）；
2. 未开启 chunked prefill 时 `max_num_batched_tokens < max_model_len` → 报错，提示增大前者或减小后者。

**与抢占（preemption）的关系**：当 KV 池被占满、新 token 无处安放时，调度器会暂停（换出）部分 RUNNING 请求——这就是抢占。它是上面公式失衡的运行时表现：并发 × 平均上下文长度持续超过 KV 池容量。vLLM 暴露 **`vllm:num_preemptions`** 指标（[v1/metrics/loggers.py](https://github.com/vllm-project/vllm/blob/main/vllm/v1/metrics/loggers.py)），压测和调优时应观察它——**不为 0 就说明系统过载**，此时应降并发或扩 KV 池，而不是继续加压力。

**细粒度 TP 联动**（Ascend 特有，[Fine_grained_TP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)）：最大 cudagraph 捕获尺寸必须覆盖

```
min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))
```

否则 `oproj`/`mlp` 细粒度 TP 会在启动时被**自动禁用并告警**（`max_cudagraph_capture_size` 也会截断该值）。

## 调优思路

| 目标 | 怎么调 | 观察指标 |
|---|---|---|
| **追吞吐** | 调高 `max_num-seqs`（同时保证 `max_num_batched_tokens ≥ max_num_seqs`），显存给足 | `vllm:num_preemptions` 应为 0；不为 0 即过载 |
| **降延迟** | 调低 `max_num_seqs` 减少排队；`max_num_batched_tokens` 设为略大于典型 prompt 长度 | TTFT / TPOT |
| **显存不足 / OOM** | 调低本参数或减少 `gpu_memory_utilization` 压力；或换量化权重、缩小 `max_model_len` | 启动 profiling 日志 |

## Ascend 语境与官方用法

- 官方教程取值跨度大：**12 / 16 / 32 / 64 / 128** 均有出现，取决于芯片显存、模型大小和 TTFT/TPOT 目标。
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：12
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html)：64（配 `--max-num-batched-tokens 20480`）
  - [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / Qwen3.5-27B 系列：128
- 注意 Ascend 官方教程普遍显式设置该值（12–128），普遍**低于** vLLM 按大显存硬件解析的 1024 默认值——NPU 部署不要迷信默认值，按官方教程起点实测调整。
- 开启动态 EPLB / 均衡调度时，该值影响均衡粒度。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-num-seqs 32
```

## 相关参数

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — 共同决定每迭代计算量，且必须 ≥ 本参数
- [`--gpu-memory-utilization`](gpu-memory-utilization.md) — 决定 KV 池大小，间接约束实际并发
- [`--max-model-len`](max-model-len.md) — 单序列长度上限，与抢占直接相关
- [`--compilation-config`](compilation-config.md) — 图捕获尺寸公式包含本参数
