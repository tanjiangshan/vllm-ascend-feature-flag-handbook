---
title: data-parallel-size
---

# `--data-parallel-size`

> Data parallel (DP) group count — the core parameter for MoE expert parallelism (EP).

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

Number of data parallel groups. **MoE layers will be sharded according to the product of the tensor, prefill-context, and data parallel sizes.** (vLLM source: `ParallelConfig.data_parallel_size`)

## Ascend context & official usage

- Standard combination in official MoE tutorials: `--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M` ([DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html), [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html), [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html), etc.).
- Multi-node DP requires the companions:
  - `--data-parallel-size-local` (replicas on this node)
  - `--data-parallel-start-rank` (this node's starting rank)
  - `--data-parallel-address` (head node address)
  - `--data-parallel-rpc-port` (RPC port)
- Non-head nodes can use `--headless` (inference only, no API server).
- Ascend-specific: DP balancing via [`enable_balance_scheduling`](../flags/enable-balance-scheduling.md).

## Usage

```bash
# 2-node DP=8, 4 replicas per node
vllm serve Qwen/Qwen3-8B \
  --enable-expert-parallel --data-parallel-size 8 \
  --data-parallel-size-local 4 --data-parallel-start-rank 4 \
  --data-parallel-address $HEAD_IP --data-parallel-rpc-port 29500 \
  --tensor-parallel-size 8
```

## Related args

- [`--enable-expert-parallel`](enable-expert-parallel.md)
- [`--tensor-parallel-size`](tensor-parallel-size.md)
- [`--headless`](index.md) / [`--distributed-executor-backend`](distributed-executor-backend.md)
