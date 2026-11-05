---
title: enable-chunked-prefill
---

# `--enable-chunked-prefill` / `--no-enable-chunked-prefill`

> Chunked prefill: long prompts are split into chunks scheduled against remaining `max_num_batched_tokens`, so long requests don't starve decode.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `None` (vLLM main `SchedulerConfig.enable_chunked_prefill = True` — enabled by default) |
| Category | Scheduling & Memory |

## Official definition

If True, prefill requests can be chunked based on the remaining `max_num_batched_tokens`. (vLLM source: `SchedulerConfig`)

## Ascend context & official usage

- Enabled by default on vLLM main; auto-disabled for encoder-decoder models (vLLM source `scheduler.py`).
- Official tutorials pass `--enable-chunked-prefill` explicitly for large-model long-context (e.g. Qwen3.5-397B family), paired with [`--max-num-batched-tokens`](max-num-batched-tokens.md) for chunk sizing.
- **CPP (dynamic chunked pipeline parallelism) interplay**: the chunk size equals `max_num_batched_tokens`; tuning space [8192, 16384, 24576, 32768] ([CPP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enable-chunked-prefill --max-num-batched-tokens 16384
```

## Related args

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — actual chunk size
- [`--long-prefill-token-threshold`](index.md) — long-request threshold
