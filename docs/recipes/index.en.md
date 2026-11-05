---
title: Deployment recipes
---

# Deployment recipes (official recommended commands)

> All commands are quoted verbatim from vLLM-Ascend official docs (main branch), each with a link to the source. **Official tutorials evolve with releases — treat the linked source as authoritative**; this site regenerates the blocks on each sync.

## By model family / scenario

| Group | Contents |
|---|---|
| [DeepSeek family](deepseek.md) | V4-Flash / V4-Pro / V4.1-Flash (dspark speculation, PCP, ascend quantization) |
| [Kimi family](kimi.md) | K2.6 / K3 / K3.1-Pro (dspark + FULL_DECODE_ONLY, NetLoader) |
| [GLM family](glm.md) | GLM5 / GLM5.2 / GLM5.3-Flash (w4a4c8-mxfp4 950 quantization, PCP+DCP) |
| [Qwen family](qwen.md) | 9 sets: Qwen3 Dense / MoE / VL / extra-large (single-node MP to multi-node Ray) |
| [MiniMax family](minimax.md) | M3 / M3.1-Flash |
| [Other models](others.md) | Cohere / Dots3 / Gemma4 / Hy4 / SigLIP2 / Step-5 |
| [Feature scenarios](features.md) | PD disaggregation (Mooncake) / Ray multi-node / suffix speculative decoding |

## How to use

1. Open a group page, expand a model card, copy the full command;
2. Replace `$MODEL_PATH`, `$PORT` etc. with your values (the source docs include the corresponding env-var setup);
3. For `--additional-config` keys see the [feature flags overview](../flags/index.md); for engine args see the [engine args overview](../engine-args/index.md).

## Verification

- Commands are quoted verbatim from official docs code blocks (only line-wrap normalized);
- Each card's "Source" link points to the corresponding docs.vllm.ai tutorial page;
- `data/recipes.json` is extracted from official docs by a script — never edit commands by hand.
