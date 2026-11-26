---
title: async-scheduling
---

# `--async-scheduling`

> Async scheduling: overlaps the next step's CPU scheduling and output processing with the current step's GPU execution, eliminating "GPU waits for CPU" gaps.

| Property | Value |
|---|---|
| Type | `bool` (`--async-scheduling` / `--no-async-scheduling`) |
| Default | `None` (auto) |
| Category | Scheduling & Memory |

## Official definition

> If set to False, disable async scheduling. Async scheduling helps to avoid gaps in GPU utilization, leading to better latency and throughput.

(vLLM source: `SchedulerConfig.async_scheduling`, [scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py))

## How it works

**What problem it solves**: synchronous scheduling is serial per step — GPU finishes → results return → CPU processes outputs and picks the next batch → next step starts. The GPU idles during that host work, and the smaller the batch (decode steps), the larger the idle share. Async scheduling lets `AsyncScheduler` prepare the next step's scheduling decisions and inputs ahead of time, in parallel with the current step's GPU compute.

**Steps in flight**: `--async-scheduling-depth` (default `2`, min `2`) controls how many steps are in flight — one on the GPU plus `depth-1` scheduled ahead; the default 2 overlaps one step's host work. Deeper queues only help when the host round trip exceeds a GPU step (low-batch cross-node decode, speculative decoding). Ignored when async scheduling is off.

**How the default `None` resolves** (vLLM `VllmConfig` post-processing):

| Condition | Result |
|---|---|
| Regular model + supporting executor + not ROCm DeepEP HT DBO | auto-enabled |
| Pooling model (embedding/rerank) | auto-disabled (current implementation slows pooling down) |
| Distributed executor backend without support | auto-disabled + warning |
| ROCm DeepEP high-throughput DBO | auto-disabled (that combination can corrupt DP+EP generation accuracy) |

When `--async-scheduling` is passed explicitly, incompatibilities above **fail startup hard** instead of silently downgrading — one reason official tutorials pass it explicitly: risks surface at launch time.

**Side effect**: with async scheduling on, DP>1 and a MoE model, vLLM automatically sets `disable_nccl_for_dp_synchronization=True` (DP sync moves to the CPU group).

## Parameter interplay

- `--async-scheduling-depth`: steps in flight, default 2; effective only with async scheduling on.
- `--max-num-seqs` / `--max-num-batched-tokens`: per-step batch size, directly affecting host scheduling cost and overlap payoff.
- `--speculative-config`: low-batch spec decoding makes host round trips dominant — the source docstring names this as a case for a deeper queue.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Default deployment | Pass nothing — `None` auto-enables; official PD tutorials also spell `--async-scheduling` out (16 tutorial pages, 124 occurrences) |
| Determinism comparisons / scheduler debugging | `--no-async-scheduling` as a baseline |
| Low-batch cross-node decode, spec decoding | Tune `--async-scheduling-depth` only if the default depth falls short |
| Pooling / rerank models | Leave it auto-disabled; do not enable explicitly |

## Ascend context & official usage

- Frequent in official Ascend tutorials: Qwen3.8-Flash-Next, Qwen3.5-397B-A17B, GLM5/5.2/5.3, MiniMax-M3, DeepSeek-V4 family, Hy4, etc. (16 pages, 124 occurrences), on both P and D sides of PD recipes.
- Commonly paired with `--max-num-seqs`, `--max-num-batched-tokens`, `--no-disable-hybrid-kv-cache-manager`, `--model-loader-extra-config '{"enable_multithread_load":true,...}'`.

## Usage

```bash
vllm serve <model> --async-scheduling
# disable (debugging / baseline)
vllm serve <model> --no-async-scheduling
```

## Related args

- [`--speculative-config`](speculative-config.md) — host round trips under low-batch speculation
- [`--max-num-seqs`](max-num-seqs.md) — per-step batch size
- Related topic: [Load Balancing & Scheduling](../feature-topics.md#t-scheduling)
