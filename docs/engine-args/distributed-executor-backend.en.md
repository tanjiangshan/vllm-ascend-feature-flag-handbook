---
title: distributed-executor-backend
---

# `--distributed-executor-backend`

> Distributed executor backend: how workers are spawned and communicate — `mp` (multi-process) or `ray`.

| Property | Value |
|---|---|
| Type | `str` |
| Default | `None` (auto-selected) |
| Category | Parallelism |

## Official definition

> Backend to use for distributed model workers, either "mp" (multi-process) or "ray" (Ray, distributed).

(vLLM source: `ParallelConfig.distributed_executor_backend`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py))

## How it works

**It governs the worker lifecycle**: once TP/PP is decided, this backend manages how each worker process is created, how they discover each other, and how they run collective communication.

- **mp (multi-process)**: vLLM spawns local processes via `multiprocessing`. Zero external dependency, fast startup, low overhead — but processes stay **on one node**;
- **ray**: workers become Ray actors. Requires a Ray cluster and starts heavier, but natively supports **multi-node** — workers can land on any cluster node.

**Distinct from `--data-parallel-backend`**: this arg selects the executor backend for the TP/PP worker layer; `--data-parallel-backend` (mp/ray) selects the backend for the DP replica layer. The two are chosen independently.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--tensor-parallel-size`](tensor-parallel-size.md) | TP across nodes → ray required; single-node allows either |
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | PP across nodes → ray required |
| [`--data-parallel-backend`](index.md) | DP-layer backend, chosen independently |

**Rule of thumb (matching official usage)**: **mp for a single node, ray for multi-node**. mp starts faster with fewer dependencies; once workers must span nodes, ray is the only option.

## Ascend context & official usage

- Explicit values in official tutorials:
  - **mp** — single node, e.g. [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html): `--distributed-executor-backend "mp"`
  - **ray** — multi-node large models, e.g. [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)
- Ascend multi-node tutorials pair with the Ray cluster docs ([tutorials/features/ray](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html)).

## Usage

```bash
# single node
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 8 --distributed-executor-backend mp
# multi-node
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 16 --distributed-executor-backend ray
```

## Related args

- [`--data-parallel-backend`](index.md) — DP-layer backend (mp/ray)
- [`--tensor-parallel-size`](tensor-parallel-size.md) — the single-node vs multi-node factor
