---
title: max-num-seqs
---

# `--max-num-seqs`

> Maximum number of sequences processed in a single iteration — the concurrency cap.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto, inferred from memory) |
| Category | Scheduling & Memory |

## Official definition

Maximum number of sequences to be processed in a single iteration. (vLLM source: `EngineArgs` / `SchedulerConfig`)

## Ascend context & official usage

- Observed values in official tutorials span **12 / 16 / 32 / 64 / 128**, depending on HBM size, model scale, and TTFT/TPOT targets.
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): 12
  - [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html): 64 (with `--max-num-batched-tokens 20480`)
  - [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / Qwen3.5-27B: 128
- **Fine-grained TP interplay** ([Fine_grained_TP guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)): the largest cudagraph capture size must cover `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))`, otherwise oproj/mlp fine-grained TP is auto-disabled with a warning.
- Affects balancing granularity when dynamic EPLB / balance scheduling is on.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-num-seqs 32
```

## Related args

- [`--max-num-batched-tokens`](max-num-batched-tokens.md)
- [`--gpu-memory-utilization`](gpu-memory-utilization.md)
