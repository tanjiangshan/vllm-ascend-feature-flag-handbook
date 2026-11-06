---
title: kv-cache-dtype
---

# `--kv-cache-dtype`

> KV cache 存储量化类型——直接决定每 token KV 的显存占用，是"用精度换并发"的第一手段。

| 属性 | 值 |
|---|---|
| 类型 | `str`（CacheDType） |
| 默认值 | `"auto"`（跟随模型 dtype） |
| 分类 | 调度与内存 |

## 官方定义

> Data type for kv cache storage. If "auto", will use model data type. CUDA 11.8+ supports fp8 (=fp8_e4m3) and fp8_e5m2. ROCm (AMD GPU) supports fp8 (=fp8_e4m3). Intel Gaudi (HPU) supports fp8 (using fp8_inc). Some models (namely DeepSeekV3.2) default to fp8, set to bfloat16 to use bfloat16 instead...

（vLLM 源码：`CacheConfig.cache_dtype`，[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)）

## 机制详解

**量化对象是 KV cache，不是权重**：两者独立。权重量化由 [`--quantization`](quantization.md) 控制；本参数控制 attention 过程中 K/V 张量的存储格式。fp8 KV 相对 bf16 每 token 省一半显存，等效于把 KV 池容量翻倍。

**官方定义里的三个要点**（源码 docstring 直译）：

1. `auto` = 跟随模型权重 dtype；
2. **部分模型默认就是 fp8**（源码点名 DeepSeekV3.2）——这类模型想退回 bf16 要显式设 `bfloat16`；
3. 显式 `fp16`/`bfloat16` **必须与模型 dtype 一致**，否则报错；
4. 平台后端可通过 `register_kv_cache_dtype` 注册自定义 KV dtype——**Ascend 的 fp8/int8 KV 支持就走这个机制**。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | KV 量化 = 等效扩大池容量；两者都是扩容手段，可叠加 |
| [`--block-size`](block-size.md) | 官方教程常组合配置（fp8 + block 32） |
| [`--max-num-seqs`](max-num-seqs.md) | 池子大了，同样并发下抢占更少 |
| 权重 NZ（[`weight_nz_mode`](../flags/weight-nz-mode.md)） | 别混淆：那是权重格式，本参数是 KV cache |

**显存账**：KV 池能装的 token 数 ≈ 池容量 ÷（2 × 层数 × KV 头数 × 头维度 × 每元素字节数）。`kv-cache-dtype fp8` 把"每元素字节数"从 2 降到 1，容量直接 ×2。

## 调优思路

| 场景 | 建议 |
|---|---|
| MoE 大模型长上下文（官方教程主流） | fp8（参考 DeepSeek-V4-Pro 配方），关注精度回归 |
| 精度敏感 | auto / bfloat16，靠其他手段腾显存 |
| Mamba/SSM 类模型 | 对应参数是 `--mamba-ssm-cache-dtype`，默认 auto |

## Ascend 语境与官方用法

- 官方教程显式取值：
  - **fp8**——[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)：`--kv-cache-dtype fp8`，并配 `--attention_config.indexer_kv_dtype fp8`
  - **int8** / **mxfp8**——其他量化模型教程
- 注意精度与显存的权衡是显式的：fp8 KV 省一半显存，但需按业务验证精度。

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## 相关参数

- [`--quantization`](quantization.md) — 权重量化（与本参数独立）
- [`--block-size`](block-size.md) — 官方教程常组合配置
- [`--mamba-ssm-cache-dtype`](index.md) — Mamba 类模型的对应参数
