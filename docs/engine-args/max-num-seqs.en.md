---
title: max-num-seqs
---

# `--max-num-seqs`

> Maximum sequences processed in a single iteration — the **concurrency gate** of the inference engine.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto, resolved by device memory tier — see below) |
| Category | Scheduling & Memory |

## Official definition

> Maximum number of sequences to be processed in a single iteration.

(vLLM source: `EngineArgs.max_num_seqs`, [arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) / `SchedulerConfig.max_num_seqs`, [scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py))

## How it works

**Where it sits in the scheduling pipeline**: every scheduler step, the scheduler picks sequences from the RUNNING queue to form a batch; `max_num_seqs` is the **count cap** of that batch. It is a hard cap — the scheduler will never exceed it, even if the KV cache could hold more.

**It affects more than scheduling — it sizes the runtime itself.** The source docstring for the adjacent `max_num_active_seqs` states it plainly:

> `max_num_seqs` sizes the model runner (per-request buffers and CUDA graph capture) and is also the default admission limit.

So raising it is not free — per-request buffers and CUDA Graph capture memory grow with it. This is also why the capture-size formula below contains it.

**What the default actually is** (when the CLI flag is omitted, `EngineArgs.max_num_seqs = None`, resolved by [`get_batch_defaults()`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) by device memory):

| Device memory | Resolved value |
|---|---|
| ≥ 160 GB (B200/B300 etc.) | **1024** |
| ≥ 70 GB and not A100 (H100/H200 etc.) | **1024** |
| Everything else (A100, small-memory devices, probe failure) | **256** |

Two corrections are applied after resolution (same function, [arg_utils.py `_set_default_max_num_seqs_and_batched_tokens_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)):

1. With `performance_mode = "throughput"`, both auto defaults are **doubled** (throughput mode only);
2. Final clamp: `max_num_seqs = min(max_num_seqs, max_num_batched_tokens)` — a step can never hold more sequences than tokens.

## Parameter interplay

Picture the engine as a factory:

| Parameter | Factory analogy | Dimension controlled | Default (vLLM main) |
|---|---|---|---|
| `--max-num-seqs` | Workpieces on the line at once | **Count**: per-step concurrent sequence cap | 256 / 1024 (memory tier) |
| [`--max-num-batched-tokens`](max-num-batched-tokens.md) | Material processed per cycle | **Tokens**: per-step compute cap | 2048–16384 (tier & usage) |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | Factory floor area | **Memory**: source of the KV cache pool size | 0.92 / 1.0 (extensible KV) |
| [`--max-model-len`](max-model-len.md) | Max size of one workpiece | **Length**: per-sequence context cap | auto-derived from model config |

**The core formula** — effective concurrency:

```
effective concurrency ≈ min(max_num_seqs, KV cache pool capacity ÷ average context length)
```

The KV pool capacity comes from `gpu-memory-utilization` (device memory minus weights and activations). Even with a huge `max_num_seqs`, if the KV pool cannot hold the contexts, concurrency stalls — extra requests queue, or get preempted.

**Two startup validations enforced in source** ([`SchedulerConfig.verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py); violation = refuse to start):

1. `max_num_batched_tokens < max_num_seqs` → error: *"max_num_batched_tokens must be greater than or equal to max_num_seqs"* (each sequence needs at least one token per step);
2. With chunked prefill off, `max_num_batched_tokens < max_model_len` → error, asking you to raise the former or lower the latter.

**Preemption linkage**: when the KV pool is full and new tokens have nowhere to go, the scheduler pauses (swaps out) some RUNNING requests — that is preemption. It is the runtime symptom of the formula above breaking: concurrency × average context length persistently exceeding the KV pool. vLLM exposes the **`vllm:num_preemptions`** metric ([v1/metrics/loggers.py](https://github.com/vllm-project/vllm/blob/main/vllm/v1/metrics/loggers.py)). **A non-zero value means overload** — lower concurrency or grow the KV pool instead of adding more load.

**Fine-grained TP interplay** (Ascend-specific, [Fine_grained_TP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)): the largest cudagraph capture size must cover

```
min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))
```

otherwise oproj/mlp fine-grained TP is **auto-disabled with a warning** at startup (and `max_cudagraph_capture_size` also truncates it).

## Tuning guidance

| Goal | How | Watch |
|---|---|---|
| **Throughput** | Raise `max_num_seqs` (keep `max_num_batched_tokens ≥ max_num_seqs`); give enough memory | `vllm:num_preemptions` should be 0; non-zero = overload |
| **Low latency** | Lower `max_num_seqs` to shorten queues; set `max_num_batched_tokens` slightly above the typical prompt length | TTFT / TPOT |
| **OOM / tight memory** | Lower this arg or relieve `gpu_memory_utilization` pressure; or use quantized weights / smaller `max_model_len` | Startup profiling logs |

## Ascend context & official usage

- Observed tutorial values span **12 / 16 / 32 / 64 / 128**, depending on HBM size, model scale, and TTFT/TPOT targets.
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): 12
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html): 64 (with `--max-num-batched-tokens 20480`)
  - [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / Qwen3.5-27B family: 128
- Note Ascend tutorials almost always set this explicitly (12–128), generally **below** the 1024 the large-memory GPU tier would resolve to — don't trust the default on NPU; start from the official tutorial values and tune by measurement.
- Affects balancing granularity when dynamic EPLB / balance scheduling is on.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-num-seqs 32
```

## Related args

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — co-determines per-step compute; must be ≥ this arg
- [`--gpu-memory-utilization`](gpu-memory-utilization.md) — KV pool size, indirectly bounds effective concurrency
- [`--max-model-len`](max-model-len.md) — per-sequence length cap, directly tied to preemption
- [`--compilation-config`](compilation-config.md) — the capture-size formula includes this arg
