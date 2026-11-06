---
title: max-num-batched-tokens
---

# `--max-num-batched-tokens`

> Max tokens processed per iteration — the core knob for prefill chunking and batch scheduling.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto, resolved by device memory tier and usage context — see below) |
| Category | Scheduling & Memory |

## Official definition

> Maximum number of tokens that can be processed in a single iteration.

(vLLM source: `EngineArgs.max_num_batched_tokens`, [arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) / `SchedulerConfig.max_num_batched_tokens`, [scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py))

## How it works

**Where it sits in the scheduling pipeline**: it is the per-step token budget. The scheduler packs RUNNING requests into the batch against this budget: prefill requests are chunked to fit the remaining budget (chunked prefill), decode requests take at least 1 token each per step. Packing stops when the budget is exhausted.

**Division of labor with `max_num_seqs`**: `max_num_seqs` caps *how many* sequences; `max_num_batched_tokens` caps *how many tokens in total*. An 8000-token prompt can prefill in one step (budget permitting) or be split across 4 steps at a budget of 2000 — that chunk size is this parameter.

**Default resolution** (when omitted from the CLI; resolved by [`get_batch_defaults()`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py); columns are the offline `LLM` class vs the API server usage context):

| Device memory | LLM (offline) | OpenAI API server |
|---|---|---|
| ≥ 160 GB (B200/B300 etc.) | 16384 | 16384 |
| ≥ 70 GB and not A100 (H100/H200 etc.) | 16384 | 8192 |
| Everything else | 8192 | 2048 |
| batched-DP MoE path | **256** (`DEFAULT_MAX_NUM_BATCHED_TOKENS_FOR_BATCHED_DP`) | same |

Subsequent corrections when the user did not set it ([arg_utils.py `_set_default_max_num_seqs_and_batched_tokens_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)):

1. `performance_mode = "throughput"` → doubled;
2. chunked prefill off → `max(resolved, max_model_len)` (so a single sequence fits);
3. clamp: `min(max_num_seqs × max_model_len, resolved)`.

The scheduler may issue even fewer tokens: `max_num_scheduled_tokens` (the true per-step emission cap) "is usually equal to `max_num_batched_tokens`, but can be smaller in cases when the model might append tokens into the batch (such as speculative decoding)" ([scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py) field docstring).

## Parameter interplay

**Hard constraint with `max_num_seqs`** (startup validation, [scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)):

```
max_num_batched_tokens ≥ max_num_seqs    (refuses to start otherwise)
```

The logic is plain: every sequence needs at least 1 token per step, so the count can never exceed the token budget.

**Interplay with `max_model_len`**: with chunked prefill on, long prompts are chunked, so `max_num_batched_tokens` may be far below `max_model_len`; with chunked prefill **off**, `max_num_batched_tokens < max_model_len` is a startup error. In other words: to run long contexts on a small budget, chunked prefill must be on.

**Preemption linkage**: a larger budget advances more long requests per step (faster KV consumption); a smaller budget stretches long requests over more steps (slower per-step KV growth, longer queues). Either imbalance shows up as a rising `vllm:num_preemptions`.

**Ascend-specific**: with [`enable_prefill_mc2`](../flags/enable-prefill-mc2.md) on, `max_num_batched_tokens` feeds the mc2_token_capacity calculation; officially recommended **≤ `tp_size × 512`** in that scenario ([additional_config reference](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)).

## Tuning guidance

| Goal | How |
|---|---|
| **TTFT-sensitive** | Set slightly above the typical prompt length so a single prefill finishes in one step |
| **TPOT-sensitive** | Shrink it so large prefills don't crowd out decode steps; pair with chunked prefill for smooth mixing |
| **Throughput first** | Raise it (mind the `≥ max_num_seqs` constraint); `performance_mode=throughput` doubles the default |
| **CPP dynamic chunking** | Sweep the fixed-chunk optimum in **[8192, 16384, 24576, 32768]** first; with dynamic chunking on, the optimum is typically **2–4×** the fixed-chunk value ([official CPP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)) |

## Ascend context & official usage

- Typical tutorial values: **1024 (small models) / 10240 / 16384 / 20480 / 32768**.
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html): 10240
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html): 20480 (with `--max-num-seqs 64`)
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): 1024
- **This knob is the most sensitive one for CPP (dynamic chunked pipeline parallelism)**: too large introduces compute waste, too small hurts operator efficiency (the official guide's own words).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-num-batched-tokens 16384
```

## Related args

- [`--max-num-seqs`](max-num-seqs.md) — count cap, must be ≤ this arg
- [`--enable-chunked-prefill`](enable-chunked-prefill.md) — this arg is the actual chunk size
- [`--max-model-len`](max-model-len.md) — with chunked prefill off, this arg must not be below it
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend dynamic chunking config
