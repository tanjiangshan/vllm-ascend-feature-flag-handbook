---
title: tensor-parallel-size
---

# `--tensor-parallel-size`

> Tensor parallel (TP) group count — the most basic parallelism parameter: slicing each layer's weights across devices.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

> Number of tensor parallel groups.

(vLLM source: `ParallelConfig.tensor_parallel_size`, `Field(default=1, ge=1)`, [parallel.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/parallel.py))

## How it works

**What gets sliced**: Q/K/V/output projections of attention and the MLP matmuls are split across devices by head/column. Each device holds a slice of the weights, computes a partial result, and an all-reduce aggregates per layer (twice per layer). The first scaling option when a model doesn't fit on one device.

**A hard shape constraint** (startup validation, [model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)):

```
total_num_attention_heads % tensor_parallel_size == 0
otherwise: "Total number of attention heads (...) must be divisible by tensor parallel size (...)"
```

**It defines the world size**: in [arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py), `world_size = pipeline_parallel_size × tensor_parallel_size` — total devices = TP × PP, then DP stacks replicas on top.

**Mind the KV heads**: GQA/MQA models have far fewer KV heads than Q heads. When TP exceeds the KV head count, vLLM replicates KV heads so every device holds at least one (`max(1, total_num_kv_heads // tp_size)`, source comment in [model.py `get_num_kv_heads`](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)) — beyond that point, more TP no longer saves KV memory. For MoE large models, the escape is [`--enable-expert-parallel`](enable-expert-parallel.md) + DP.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | world size = TP × PP; their product sets per-node/cluster device count |
| [`--data-parallel-size`](data-parallel-size.md) | MoE experts sharded by **TP × PCP × DP** (vLLM source docstring) |
| [`--enable-expert-parallel`](enable-expert-parallel.md) | the alternative for MoE: EP slices experts, TP keeps attention only |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | DCP on GQA/MQA requires TP > total KV heads (source validation) |
| [`--distributed-executor-backend`](distributed-executor-backend.md) | TP across nodes needs ray; single-node mp |

**Analogy**: TP is like cutting **every page** of a thick book into pieces handed to several people reading simultaneously — faster, but every page turn requires a reconciliation (all-reduce).

## Ascend context & official usage

- Tutorial values: **1 / 2 / 4 / 8 / 16**:
  - Single-node A2: [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) tp4 with `--distributed-executor-backend mp`
  - A3 large models: tp8 common; 16 for multi-node
- Combined with fine-grained TP ([`finegrained_tp_config`](../flags/finegrained-tp-config.md)), oproj/mlp can use a **different degree than attention** — at the cost of the cudagraph capture-size constraint (see its formula).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 4
```

## Related args

- [`--pipeline-parallel-size`](pipeline-parallel-size.md) — the other world-size factor
- [`--data-parallel-size`](data-parallel-size.md) — EP scale source
- [`--enable-expert-parallel`](enable-expert-parallel.md) — the MoE memory partner
- [`--distributed-executor-backend`](distributed-executor-backend.md) — single-node mp / multi-node ray
