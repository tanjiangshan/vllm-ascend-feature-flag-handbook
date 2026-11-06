---
title: quantization
---

# `--quantization`

> Weight quantization method — determines weight memory footprint and the compute kernel. Ascend repos use dedicated quantization format naming.

| Property | Value |
|---|---|
| Type | `str` (QuantizationMethods) |
| Default | `None` (inferred from the model config) |
| Category | Model & Loading |

## Official definition

> Method used to quantize the weights. If `None`, we first check the `quantization_config` attribute in the model config file. If that is `None`, we assume the model weights are not quantized and use `dtype` to determine the data type of the weights.

(vLLM source: `ModelConfig.quantization`, [model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py))

## How it works

**The inference chain** (per the source docstring):

```
explicitly set → use the explicit value
None           → if the model config's quantization_config exists → use it
                 else → weights are not quantized; dtype decides the weight type
```

So in most cases **you don't set it manually** — a quantized checkpoint carries its own metadata and is auto-detected. Set it explicitly in two cases: the model config lacks quantization info but you're using a quantized checkpoint; or you want to force a specific quantization kernel path.

**It's not only about memory**: each method maps to a different weight kernel (compute path), with different precision, speed, and hardware support. Available methods on Ascend are strongly tied to the chip generation — follow the model's tutorial.

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--dtype`](index.md) | weight dtype on the non-quantized path; the quantization method takes over otherwise |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | weight quantization ≠ KV quantization — independent, but commonly combined (DeepSeek-V4-Pro: ascend weights + fp8 KV) |
| Ascend [`weight_nz_mode`](../flags/weight-nz-mode.md) | weight NZ format mode, the layout companion for quantized weights |
| Ascend [`ascend_compilation_config`](../flags/ascend-compilation-config.md) | some quantization formats impose graph-mode requirements |

**The memory math**: weight quantization changes the numerator directly — `KV pool ≈ total memory × utilization − weights`. W8A8 halves weights vs bf16, and everything saved goes to the KV pool.

## Ascend context & official usage

- Explicit values in official tutorials:
  - **ascend** — [GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / DeepSeek-V4 family (Ascend-specific format)
  - **deepseek_v4_fp8**, **mxfp8** — matched to their respective quantized checkpoints
- Ascend repo naming convention (GLM5.2 tutorial): `GLM-5.2-w4a4c8-mxfp4` (950 series, W4A4 MXFP4 mixed precision). **A3 and 950 quantization formats are not interchangeable** — match the checkpoint to your hardware.
- Quantized models should also mind KV dtype and weight NZ (table above).

## Usage

```bash
vllm serve Qwen/Qwen3-8B --quantization ascend
```

## Related args

- [`--dtype`](index.md) — dtype choice on the non-quantized path
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV quantization (independent of this arg)
- [`weight_nz_mode`](../flags/weight-nz-mode.md) — Ascend weight NZ format
