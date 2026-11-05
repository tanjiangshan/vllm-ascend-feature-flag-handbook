---
title: max-num-seqs
---

# `--max-num-seqs`

> 单次迭代最大处理的序列数，即并发请求上限。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（自动，由调度器按显存推断） |
| 分类 | 调度与内存 |

## 官方定义

Maximum number of sequences to be processed in a single iteration.（vLLM 源码 `EngineArgs` / `SchedulerConfig`）

## Ascend 语境与官方用法

- 官方教程实测取值跨度大：**12 / 16 / 32 / 64 / 128** 均有出现，取决于芯片显存、模型大小和 TTFT/TPOT 目标。
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：12
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html)：64（配 `--max-num-batched-tokens 20480`）
  - [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / Qwen3.5-27B 系列：128
- **细粒度 TP 联动**（[Fine_grained_TP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)）：最大 cudagraph 捕获尺寸必须覆盖 `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))`，否则 oproj/mlp 细粒度 TP 会在启动时被自动禁用并告警。
- 开启动态 EPLB / 均衡调度时，该值影响均衡粒度。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-num-seqs 32
```

## 相关参数

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — 共同决定每迭代计算量
- [`--gpu-memory-utilization`](gpu-memory-utilization.md) — 显存给得越多，可承载的 seqs 越多
