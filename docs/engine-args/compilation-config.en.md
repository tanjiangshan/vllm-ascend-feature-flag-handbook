---
title: compilation-config
---

# `--compilation-config` (`-cc`)

> torch.compile and CUDA Graph capture configuration — the key production-performance parameter.

| Property | Value |
|---|---|
| Type | `CompilationConfig` (JSON / dotted overrides) |
| Default | `CompilationConfig()` (sub-fields have their own defaults, e.g. `cudagraph_mode`) |
| Category | Compilation & Graphs |

## Official definition

`torch.compile` and cudagraph capture configuration for the model. As a shorthand, one can append compilation arguments via `-cc.parameter=argument`. (vLLM source: `EngineArgs.compilation_config`)

## Ascend context & official usage

- High-frequency values in official tutorials:
  - `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` ([Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html), DeepSeek-V4 family) — capture graphs for decode steps only; prefill stays eager for stabler TTFT;
  - `--compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,...]}'` (Qwen3-Dense etc.) — explicit capture-size enumeration.
- **Fine-grained TP interplay**: the max capture size must cover `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))`, otherwise related optimizations are auto-disabled ([Fine_grained_TP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)).
- Ascend adaptation: vllm-ascend `platform.py` shrinks `max_cudagraph_capture_size` based on available memory and handles options like `use_inductor_graph_partition`.

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
# or dotted override
vllm serve Qwen/Qwen3-8B -cc.cudagraph_mode=FULL_DECODE_ONLY
```

## Related args

- [`--enforce-eager`](enforce-eager.md) — the opposite "master switch"
- [`--max-num-seqs`](max-num-seqs.md) — input to the capture-size bound formula
