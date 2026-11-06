---
title: data-parallel-size
---

# `--data-parallel-size`

> Data parallel (DP) group count — scaling concurrency via replicas; **the scale source for MoE expert parallelism (EP)**.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

> Number of data parallel groups. **MoE layers will be sharded according to the product of the tensor, prefill-context, and data parallel sizes.**

(vLLM source: `ParallelConfig.data_parallel_size`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py); emphasis in the original source)

## How it works

**What gets sliced**: requests. Each DP replica is a complete, independent stack of "TP×PP workers + scheduler", serving its own request queue. Replicas sync metadata (scheduling, load balancing) over RPC; the head node fronts the API layer.

**The extra meaning for MoE** (source docstring): with [`--enable-expert-parallel`](enable-expert-parallel.md) on, MoE experts are sharded by **the product TP × PCP × DP** — each +1 of DP divides the per-rank expert count further. This is why large-MoE "EP scale" is tuned mainly via DP, not TP.

**Multi-node DP companions (all required)**:

| Argument | Role |
|---|---|
| `--data-parallel-size-local` | replicas on this node (source check: must be ≤ `data_parallel_size`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)) |
| `--data-parallel-start-rank` | this node's starting rank |
| `--data-parallel-address` | head node address |
| `--data-parallel-rpc-port` | fixed RPC port |

Non-head nodes additionally take `--headless` (inference only, no API server).

**Another source check**: `data_parallel_size_external_lb` is only valid with `data_parallel_size > 1` ([parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py)).

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--enable-expert-parallel`](enable-expert-parallel.md) | DP is the primary EP scale knob (experts split by TP×PCP×DP) |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | multiplies with DP to set per-rank expert count |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | the third factor in expert sharding |
| Ascend [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md) | request balancing across DP replicas |

**Analogy**: DP is opening more branch stores — each store is a full copy (full worker stack), store count = concurrent serving capacity. For MoE, more stores means the HQ's scarce talent (experts) can be divided more thinly.

## Ascend context & official usage

- Standard combination in official MoE tutorials: `--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M` ([DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html), [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html), [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html), etc.).
- Official multi-node tutorials use the `--data-parallel-*` family for node addressing; non-head nodes take `--headless`.
- Ascend-specific: replica balancing via [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md).

## Usage

```bash
# 2-node DP=8, 4 replicas per node (second node shown)
vllm serve Qwen/Qwen3-8B \
  --enable-expert-parallel --data-parallel-size 8 \
  --data-parallel-size-local 4 --data-parallel-start-rank 4 \
  --data-parallel-address $HEAD_IP --data-parallel-rpc-port 29500 \
  --tensor-parallel-size 8
```

## Related args

- [`--enable-expert-parallel`](enable-expert-parallel.md) — DP is the EP scale source
- [`--tensor-parallel-size`](tensor-parallel-size.md) — multiplies with DP for per-rank expert count
- [`--headless`](index.md) / [`--distributed-executor-backend`](distributed-executor-backend.md) — multi-node companions
