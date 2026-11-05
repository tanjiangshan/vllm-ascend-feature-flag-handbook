---
title: quantization
---

# `--quantization`

> Weight quantization method. Ascend model repos use dedicated quantization format naming.

| Property | Value |
|---|---|
| Type | `str` (QuantizationMethods) |
| Default | `None` (inferred from the model config's `quantization_config`) |
| Category | Model & Loading |

## Official definition

Method used to quantize the weights. If `None`, we first check the `quantization_config` attribute in the model config file. (vLLM source: `ModelConfig.quantization`)

## Ascend context & official usage

- Explicit values in official tutorials: **ascend** (GLM5.2 / DeepSeek-V4 family — Ascend-specific format), **deepseek_v4_fp8**, **mxfp8**.
- Ascend repo naming convention (from the [GLM5.2 tutorial](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html)): `GLM-5.2-w4a4c8-mxfp4` (950 series, W4A4 MXFP4 mixed precision). **A3 and 950 quantization formats are not interchangeable** — match the checkpoint to your hardware when downloading.
- Quantized models: also mind KV cache dtype ([`--kv-cache-dtype`](kv-cache-dtype.md)) and weight NZ ([`weight_nz_mode`](../flags/weight-nz-mode.md), default 1).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --quantization ascend
```

## Related args

- [`--dtype`](index.md) — dtype choice on the non-quantized path
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV cache quantization
