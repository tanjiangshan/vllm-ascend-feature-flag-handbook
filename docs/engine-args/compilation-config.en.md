---
title: compilation-config
---

# `--compilation-config` (`-cc`)

> torch.compile and CUDA Graph capture configuration — the core production-performance knob, controlling which steps are captured and at which sizes.

| Property | Value |
|---|---|
| Type | `CompilationConfig` (JSON, or `-cc.key=value` dotted overrides) |
| Default | `CompilationConfig()` (sub-fields carry their own defaults, e.g. `cudagraph_mode`) |
| Category | Compilation & Graphs |

## Official definition

> `torch.compile` and cudagraph capture configuration for the model. As a shorthand, one can append compilation arguments via `-cc.parameter=argument`.

(vLLM source: `EngineArgs.compilation_config`, [arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py))

## How it works

**What it governs**: two subsystems — torch.compile (compiling the model into better kernel sequences) and CUDA Graph (whole-graph replay). Key sub-fields:

| Sub-field | Role |
|---|---|
| `cudagraph_mode` | Capture scope: `FULL` (prefill+decode), `FULL_DECODE_ONLY` (decode only), `PIECEWISE`, etc. |
| `cudagraph_capture_sizes` | Explicit list of batch sizes to capture |
| `max_cudagraph_capture_size` | Upper bound on capture sizes |

**Why decode steps need graphs most**: each decode step is a single forward (1 token per sequence), where kernel-launch and CPU scheduling dominate; replaying the whole step as one graph maximizes TPOT gains. Prefill steps are compute-heavy with varying shapes — little capture benefit, frequent misses. This is why official tutorials favor `FULL_DECODE_ONLY`.

**Two ways to pass it** (confirmed in the source docstring):

```bash
--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'   # full JSON
-cc.cudagraph_mode=FULL_DECODE_ONLY                            # dotted shorthand
```

## Parameter interplay

**Mutually exclusive with `--enforce-eager`**: eager on = this entire config is inert (see [`enforce-eager`](enforce-eager.md)).

**Capture-size formula vs scheduling args** (Ascend fine-grained TP, [Fine_grained_TP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)):

```
the max capture size must cover min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))
```

Otherwise oproj/mlp fine-grained TP is auto-disabled with a warning at startup. On the vLLM side, `max_cudagraph_capture_size` is also truncated by the Ascend platform layer based on available memory (vllm-ascend `platform.py`).

**Speculative decoding linkage**: with `num_speculative_tokens > 0`, decode steps carry `1 + n` tokens per sequence — the capture-size enumeration must cover those shapes (same formula).

## Tuning guidance

| Scenario | Suggestion |
|---|---|
| Production default (official mainstream) | `{"cudagraph_mode":"FULL_DECODE_ONLY"}` — decode captured, prefill free-form |
| Fixed batch shapes | Enumerate `cudagraph_capture_sizes` explicitly (official Qwen3-Dense recipe), skipping auto-probing |
| Tight memory | Shrink the capture-size list / lower `max_cudagraph_capture_size`; last resort `--enforce-eager` |

## Ascend context & official usage

- High-frequency values in official tutorials:
  - `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'` ([Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html), DeepSeek-V4 family)
  - `--compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,...]}'` (Qwen3-Dense etc.)
- Mind the layering vs Ascend-side graph switches (`enable_npugraph_ex` in [`ascend_compilation_config`](../flags/ascend-compilation-config.md), [`xlite_graph_config`](../flags/xlite-graph-config.md)): this arg is the vLLM layer; those are the Ascend platform layer; the final graph mode is arbitrated by platform code.

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
# or dotted override
vllm serve Qwen/Qwen3-8B -cc.cudagraph_mode=FULL_DECODE_ONLY
```

## Related args

- [`--enforce-eager`](enforce-eager.md) — the mutually exclusive master switch
- [`--max-num-seqs`](max-num-seqs.md) — input to the capture-size formula
- [`--speculative-config`](speculative-config.md) — affects decode-step shapes
