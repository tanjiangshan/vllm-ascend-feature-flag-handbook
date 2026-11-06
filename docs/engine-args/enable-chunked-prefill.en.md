---
title: enable-chunked-prefill
---

# `--enable-chunked-prefill` / `--no-enable-chunked-prefill`

> Chunked prefill: long prompts are split against the remaining `max_num_batched_tokens` budget and digested across scheduler steps — long requests no longer starve decode.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `None` → auto per model support (on for supporting models) |
| Category | Scheduling & Memory |

## Official definition

> If True, prefill requests can be chunked based on the remaining `max_num_batched_tokens`.

(vLLM source: `SchedulerConfig.enable_chunked_prefill`, [scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py))

## How it works

**Without chunking**: a 32K-token prompt forces the scheduler to free a 32K-token budget within a single step — every decode request waits in line meanwhile. One long request degrades TPOT for everyone. This is "prefill starving decode".

**With chunking**: the prompt is split by budget and advanced chunk-by-chunk; decode requests interleave between chunks. Two consequences:

- ✅ Smoother TPOT: decode is no longer suppressed by long prefills;
- ⚠️ Longer TTFT: total prefill time stretches (chunks compete for budget).

**Default auto-resolution** ([arg_utils.py `_set_default_chunked_prefill_and_prefix_caching_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)):

```
None → model_config.is_chunked_prefill_supported (auto-on when supported)
```

So on main, supporting models have it **on by default**. Two exception paths (same function):

- Manually disabling it on a supporting model → warning: *"This model does not officially support disabling chunked prefill... may cause the engine to crash or produce incorrect outputs"*;
- Encoder-decoder models are auto-disabled in source ([scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py), `disable_chunked_mm_input` branch).

## Parameter interplay

**With `max_num_batched_tokens` — the chunk size IS it**: with chunking on, a "chunk" is the budget granted to that request per step. Tuning `max_num_batched_tokens` tunes the chunk size.

**Startup validation against `max_model_len`** ([scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)):

```
chunking off: max_num_batched_tokens < max_model_len → startup error
chunking on:  constraint lifted (long sequences digest in chunks)
```

This is why long-context deployments almost always enable it: **the prerequisite for running long contexts on a small budget**.

**Preemption linkage**: chunking makes per-step KV growth of long requests smaller (one chunk written per step), smoothing pool pressure; `vllm:num_preemptions` fluctuates less than without chunking.

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Mixed long/short traffic (typical online serving) | **Keep on** (default) |
| TTFT-first with known prompt lengths | Can disable, but must ensure `max_num_batched_tokens ≥ max_model_len` (else startup error), and accept decode jitter |
| CPP dynamic chunking (Ascend PP) | Chunking is the prerequisite; pair with [`profiling_chunk_config`](../flags/profiling-chunk-config.md) for dynamic sizing |

## Ascend context & official usage

- Default on vLLM main: auto-on for supporting models. Official tutorials pass `--enable-chunked-prefill` explicitly for large-model long-context (Qwen3.5-397B family), paired with large `max_num_batched_tokens` (16384+) for chunk sizing.
- Ascend's **CPP (dynamic chunked pipeline parallelism)** builds on chunking: the chunk size equals `max_num_batched_tokens`; tuning space [8192, 16384, 24576, 32768] ([official CPP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enable-chunked-prefill --max-num-batched-tokens 16384
```

## Related args

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — the actual chunk size
- [`--max-model-len`](max-model-len.md) — startup constraint when chunking is off
- [`profiling_chunk_config`](../flags/profiling-chunk-config.md) — Ascend dynamic chunking config
