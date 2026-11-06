---
title: quantization
---

# `--quantization`

> 权重量化方法——决定权重占显存多少、用什么 kernel 计算。Ascend 模型仓库有专用量化格式命名。

| 属性 | 值 |
|---|---|
| 类型 | `str`（QuantizationMethods） |
| 默认值 | `None`（从模型 config 推断） |
| 分类 | 模型与加载 |

## 官方定义

> Method used to quantize the weights. If `None`, we first check the `quantization_config` attribute in the model config file. If that is `None`, we assume the model weights are not quantized and use `dtype` to determine the data type of the weights.

（vLLM 源码：`ModelConfig.quantization`，[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）

## 机制详解

**推断链**（源码 docstring 直译）：

```
显式设置 → 用显式值
None     → 模型 config 的 quantization_config 有值 → 用它
           也没有 → 权重未量化，dtype 决定权重类型
```

即大部分场景**不用手动设**——模型仓库自带量化信息时自动识别。需要显式设置的两个场景：模型 config 缺量化信息但你用的是量化 checkpoint；或强制走某条量化 kernel 路径。

**它决定的不只是显存**：不同量化方法对应不同的权重 kernel（计算路径），精度、速度、支持硬件各不相同。Ascend 上可用的方法与芯片代际强相关——以模型教程为准。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--dtype`](index.md) | 未量化路径的权重 dtype；量化路径下由量化方法接管 |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | 权重量化 ≠ KV 量化，两者独立但常组合（DeepSeek-V4-Pro：ascend 权重 + fp8 KV） |
| Ascend [`weight_nz_mode`](../flags/weight-nz-mode.md) | 权重 NZ 格式模式，量化权重的配套布局开关 |
| Ascend [`ascend_compilation_config`](../flags/ascend-compilation-config.md) | 部分量化格式对图模式有要求 |

**显存账**：权重量化直接改"分子"——`KV 池 ≈ 总显存 × 占比 − 权重`。W8A8 权重相对 bf16 省一半，省下的全归 KV 池，等效扩容。

## Ascend 语境与官方用法

- 官方教程显式取值：
  - **ascend**——[GLM5.2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) / DeepSeek-V4 系（Ascend 专用量化格式）
  - **deepseek_v4_fp8**、**mxfp8**——对应各自的量化 checkpoint
- Ascend 模型仓库量化命名规律（以 GLM5.2 教程为例）：`GLM-5.2-w4a4c8-mxfp4`（950 系列，W4A4 MXFP4 混合精度）。**A3 与 950 系列的量化格式不通用**，下载 checkpoint 时必须对应硬件。
- 量化模型需配套关注 KV dtype 与权重 NZ（上表）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --quantization ascend
```

## 相关参数

- [`--dtype`](index.md) — 非量化路径的 dtype 选择
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV 量化（与本参数独立）
- [`weight_nz_mode`](../flags/weight-nz-mode.md) — Ascend 权重 NZ 格式
