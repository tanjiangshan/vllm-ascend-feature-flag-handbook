---
title: max-model-len
---

# `--max-model-len`

> Maximum model context length (prompt + output). Requests beyond it are rejected.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `None` (auto-derived from model config) |
| Category | Scheduling & Memory |

## Official definition

Model context length (prompt and output). If unspecified, will be automatically derived from the model config. Supports k/m unit suffixes. (vLLM source: `ModelConfig`)

## Ascend context & official usage

- Nearly all official tutorials set it explicitly, since it directly drives KV cache memory pressure:
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) / [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html) / [Kimi-K3.1-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html): `1048576` (1M context)
  - [GLM5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) / [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html): `131072`
  - Also `133120`, `135168`, `40000`, etc. depending on the model
- With PCP/DCP, long prefills are further split across ranks (see [`prefill-context-parallel-size`](prefill-context-parallel-size.md)).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --max-model-len 131072
```

## Related args

- [`--block-size`](block-size.md)
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md)
