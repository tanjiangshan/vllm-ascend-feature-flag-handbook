---
title: quantization
---

# `--quantization`

> 权重量化方法。Ascend 模型仓库有专门的量化格式命名。

| 属性 | 值 |
|---|---|
| 类型 | `str`（QuantizationMethods） |
| 默认值 | `None`（从模型 config 的 `quantization_config` 推断） |
| 分类 | 模型与加载 |

## 官方定义

Method used to quantize the weights. If `None`, we first check the `quantization_config` attribute in the model config file.（vLLM 源码 `ModelConfig.quantization`）

## Ascend 语境与官方用法

- 官方教程显式取值：**ascend**（GLM5.2/DeepSeek-V4 系，Ascend 专用量化格式）、**deepseek_v4_fp8**、**mxfp8**。
- Ascend 模型仓库的量化命名规律（以 [GLM5.2 教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html)为例）：`GLM-5.2-w4a4c8-mxfp4`（950 系列，W4A4 MXFP4 混合精度）；A3 与 950 的量化格式**不通用**，下载时必须对应硬件。
- 量化模型需配套注意 KV cache dtype（[`--kv-cache-dtype`](kv-cache-dtype.md)）与权重 NZ（[`weight_nz_mode`](../flags/weight-nz-mode.md)，默认 1）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --quantization ascend
```

## 相关参数

- [`--dtype`](index.md) — 非量化路径的 dtype 选择
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV cache 量化
