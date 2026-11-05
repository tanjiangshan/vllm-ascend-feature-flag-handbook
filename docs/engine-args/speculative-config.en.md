---
title: speculative-config
---

# `--speculative-config`

> Speculative decoding configuration (JSON): a draft model predicts multiple tokens to accelerate decode.

| Property | Value |
|---|---|
| Type | `dict[str, Any]` (JSON) |
| Default | `None` (disabled) |
| Category | Speculative Decoding |

## Official definition

Speculative decoding configuration. (vLLM source: `SpeculativeConfig`)

## Ascend context & official usage

- Recommended method on Ascend in official tutorials: **dspark** (DeepSpark).
  - [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html): `--speculative-config '{"num_speculative_tokens":5,"method":"dspark"}'`
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): dspark + `draft_tensor_parallel_size:8` + `draft_sample_method:"greedy"`, with `enforce_eager:true` on the draft side and `num_speculative_tokens:7`
- Compatibility ([context parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)): MLA + PCP supports MTP only; GQA + PCP supports Eagle3 only.
- Ascend companion flags: [`dynamic_spec_config`](../flags/dynamic-spec-config.md) (dynamic speculation), [`enable_flashcomm1`](../flags/enable-flashcomm1.md) (MRv1 comm optimization), [`rejection_sampler_config`](../flags/rejection-sampler-config.md) (RL verification).

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --speculative-config '{"method":"dspark","num_speculative_tokens":5}'
```

## Related args

- [`--compilation-config`](compilation-config.md) — often combined with `FULL_DECODE_ONLY`
- [`--max-num-seqs`](max-num-seqs.md) — the cudagraph bound formula includes `num_speculative_tokens`
