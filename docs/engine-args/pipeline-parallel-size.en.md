---
title: pipeline-parallel-size
---

# `--pipeline-parallel-size`

> Pipeline parallel (PP) group count — spreading the model's **layers** across devices, for when a model doesn't fit on one machine.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

> Number of pipeline parallel groups.

(vLLM source: `ParallelConfig.pipeline_parallel_size`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py))

## How it works

**What gets sliced, and how data flows**: TP slices *inside* each layer; PP slices *between* layers. The model is divided into layer stages, one per device; a micro-batch flows through the stages like an assembly line, with different devices working on different micro-batches at the same time.

**Two costs**:

1. **Pipeline bubbles**: devices idle waiting for the previous stage's output; bubble fraction grows with stage count;
2. **Scheduling complexity**: the batch must be split into rotating micro-batches.

**Source hard constraint** ([model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)):

```
PP > 1 requires the model to implement the SupportsPP interface,
otherwise NotImplementedError: "Pipeline parallelism is not supported for this model."
```

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--tensor-parallel-size`](tensor-parallel-size.md) | world size = TP × PP; stack PP only when one node can't hold the model |
| [`--data-parallel-size`](data-parallel-size.md) | DP/PP compose; large-scale MoE commonly uses TP×PP×DP |
| Ascend [`profiling_chunk_config`](../flags/profiling-chunk-config.md) | **CPP dynamic chunking** exists specifically to optimize micro-batch splitting for PP, easing bubbles |

**Analogy**: PP is a factory assembly line — each station (device) owns a fixed set of processes (layers), and products (micro-batches) flow through. More stations don't always mean faster: conveyor idle time (bubbles) eats the gains. Add stations only when one station can't finish a product alone.

## Ascend context & official usage

- Tutorial values: **1 / 2 / 4**: enabled for super-large multi-node deployments (e.g. [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)).
- Ascend's **CPP (dynamic chunked pipeline parallelism)** is the dedicated PP optimization: per-step token splitting of micro-batches is tuned to device load; the tuning target is [`--max-num-batched-tokens`](max-num-batched-tokens.md) (search space [8192, 16384, 24576, 32768]; the dynamic-chunking optimum is typically 2–4× the fixed-chunk value).
- Rule of thumb: don't enable PP if the model fits on one node (pure bubble loss); when it doesn't fit, PP is mandatory — and CPP above it recovers some bubble loss.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --pipeline-parallel-size 2 --tensor-parallel-size 8
```

## Related args

- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--data-parallel-size`](data-parallel-size.md)
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend's dedicated PP optimization
