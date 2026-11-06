---
title: max-model-len
---

# `--max-model-len`

> Maximum context length served by the model (prompt + output) — requests beyond it are rejected outright.

| Property | Value |
|---|---|
| Type | `int` (accepts `k/m/g/t` suffix shorthand) |
| Default | `None` (auto-derived from the model config) |
| Category | Scheduling & Memory |

## Official definition

> Model context length (prompt and output). If unspecified, will be automatically derived from the model config.

(vLLM source: `ModelConfig.max_model_len`, [model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py))

## How it works

**Two paths**:

1. **Unset**: takes the context limit from the model config (the exact source field varies by model — `max_position_embeddings`, rope-derived values, etc. — whatever the actual config provides);
2. **Set explicitly**: becomes a service-level hard cap. Requests exceeding it are **rejected at admission** (an error says the sequence is too long) and never reach the scheduler.

**k/m/g/t suffix shorthand**: vLLM's CLI layer expands bare numeric suffixes ([`human_readable_int`](https://github.com/vllm-project/vllm/blob/main/vllm/utils/argparse_utils.py)); the same expansion is applied inside JSON-valued args by [`_expand_json_human_readable_numbers`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py):

| Form | Meaning | Result |
|---|---|---|
| `--max-model-len 128k` | lowercase = decimal | 128000 |
| `--max-model-len 128K` | uppercase = binary | 131072 |

> ⚠️ Case matters: lowercase `k/m/g/t` are powers of 10; uppercase `K/M/G/T` are powers of 2. Mind the case in configs.

## Parameter interplay

**Versus KV cache capacity**: a sequence's peak memory need ≈ `max_model_len × KV bytes per token`. This parameter is therefore the first input to KV pool planning: the pool must hold at least a few sequences near `max_model_len`, or effective concurrency collapses toward zero.

**Startup validation against `max_num_batched_tokens`** ([scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)):

```
chunked prefill off: max_num_batched_tokens < max_model_len → startup error
```

Reason: without chunking, a single prefill must complete in one step, so the budget must fit the longest sequence. With chunked prefill on, the constraint is lifted — which is why nearly all long-context deployments enable it.

**Preemption linkage**: a larger `max_model_len` means more KV per sequence at worst case; mixed long/short traffic fills the pool sooner and raises `vllm:num_preemptions`. Shrinking it is the most direct way to trade context for concurrency.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Long-document / agent workloads | Set to business max input + max output; rejecting overlong requests beats letting one giant sequence degrade everyone |
| Tight memory | Shrink this first (caps per-request peak), then concurrency |
| Aligning with official recipes | Copy the value from the model's official tutorial (below) — safest baseline |

## Ascend context & official usage

- Nearly all official tutorials set it explicitly (it is the #1 driver of KV cache memory pressure):
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) / [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html) / [Kimi-K3.1-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html): `1048576` (1M)
  - [GLM5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) / [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): `131072`
  - Also `133120`, `135168`, `40000`, etc., trimmed per model
- Long prefills on Ascend can be further split across ranks with [`prefill-context-parallel-size`](prefill-context-parallel-size.md) (see its compatibility matrix).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-model-len 131072
vllm serve Qwen/Qwen3-8B --max-model-len 128K   # 131072
```

## Related args

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — startup constraint when chunked prefill is off
- [`--enable-chunked-prefill`](enable-chunked-prefill.md) — the key that lifts the constraint
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) — multi-card prefill acceleration for long contexts
- [`--gpu-memory-utilization`](gpu-memory-utilization.md) — source of the KV pool capacity
