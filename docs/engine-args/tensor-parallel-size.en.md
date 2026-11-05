---
title: tensor-parallel-size
---

# `--tensor-parallel-size`

> Tensor parallel (TP) group count — the most basic parallelism parameter.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

Number of tensor parallel groups. (vLLM source: `ParallelConfig.tensor_parallel_size`, `Field(default=1, ge=1)`)

## Ascend context & official usage

- Tutorial values: **1 / 2 / 4 / 8 / 16**. Single-node A2 commonly 2–8 (e.g. [Qwen3-Dense](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html) tp4 with `--distributed-executor-backend mp`); A3 large models often tp8; 16 for multi-node.
- For MoE: experts are sharded by the product **TP × PCP × DP** (vLLM source, `data_parallel_size` docstring).
- With fine-grained TP ([`finegrained_tp_config`](../flags/finegrained-tp-config.md)), sub-modules can use different degrees.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --tensor-parallel-size 4
```

## Related args

- [`--data-parallel-size`](data-parallel-size.md)
- [`--pipeline-parallel-size`](pipeline-parallel-size.md)
- [`--distributed-executor-backend`](distributed-executor-backend.md)
