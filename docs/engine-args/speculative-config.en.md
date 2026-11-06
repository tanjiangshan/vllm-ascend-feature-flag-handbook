---
title: speculative-config
---

# `--speculative-config`

> Speculative decoding configuration (JSON): a draft model predicts multiple tokens; the target model verifies them in one pass — trading compute for TPOT.

| Property | Value |
|---|---|
| Type | `dict[str, Any]` (JSON) |
| Default | `None` (disabled) |
| Category | Speculative Decoding |

## Official definition

> Speculative decoding configuration.

(vLLM source: `SpeculativeConfig`, [config/speculative.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/speculative.py))

## How it works

**The principle**: a decode step produces 1 token from the target model. Speculative decoding lets a lightweight draft model guess `num_speculative_tokens` tokens first; the target model **verifies them in parallel** — accepted tokens all land in one step. With a high acceptance rate, one target step does the work of several, and TPOT drops by a multiple.

**The costs, accounted honestly**:

- The draft model itself consumes memory and compute (one extra forward per step);
- Missed guesses are pure waste — **low acceptance makes it slower**;
- Scheduling gets complex: each step schedules "draft forward + target verification".

**Key JSON fields** (evidenced from official tutorials):

| Field | Role |
|---|---|
| `method` | draft method; Ascend tutorials use **dspark** (DeepSpark) |
| `num_speculative_tokens` | guesses per step (tutorials commonly 5–7) |
| `model` | draft model path (same as target for self-speculation) |
| `draft_tensor_parallel_size` | draft-side parallelism (may be smaller than the target's) |
| `draft_sample_method` | draft sampling (e.g. `greedy`) |
| `enforce_eager` | skip graph capture on the draft side (`true` in the Kimi-K3 recipe) |

## Parameter interplay

**Scheduler-level linkage (source-level)**: speculation multiplies per-step token counts by `1 + num_speculative_tokens`. The scheduler's `max_num_scheduled_tokens` "is usually equal to `max_num_batched_tokens`, but can be smaller in cases when the model might append tokens into the batch (such as speculative decoding)" ([scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py) field docstring).

**Graph-capture linkage**: capture-size enumeration must cover `1 + n` shapes — the fine-grained TP formula `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))` contains it ([Fine_grained_TP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)).

**PCP compatibility** ([Ascend context parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)): MLA + PCP supports MTP drafts only; GQA + PCP supports Eagle3 only.

**Ascend companion flags**:

| Flag | Role |
|---|---|
| [`dynamic_spec_config`](../flags/dynamic-spec-config.md) | dynamically tune speculation by acceptance rate |
| [`enable_flashcomm1`](../flags/enable-flashcomm1.md) | MRv1 speculation communication optimization |
| [`rejection_sampler_config`](../flags/rejection-sampler-config.md) | verification sampling config for RL rollouts |

## Ascend context & official usage

- Recommended method in official tutorials: **dspark** (DeepSpark).
  - [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html): `--speculative-config '{"num_speculative_tokens":5,"method":"dspark"}'`
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): dspark + `draft_tensor_parallel_size:8` + `draft_sample_method:"greedy"` + `num_speculative_tokens:7`, with `enforce_eager:true` on the draft side
- Often combined with [`--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'`](compilation-config.md).

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --speculative-config '{"method":"dspark","num_speculative_tokens":5}'
```

## Related args

- [`--compilation-config`](compilation-config.md) — capture sizes must cover speculative shapes
- [`--max-num-seqs`](max-num-seqs.md) — the other input to the capture-size formula
- [`dynamic_spec_config`](../flags/dynamic-spec-config.md) — Ascend dynamic speculation
