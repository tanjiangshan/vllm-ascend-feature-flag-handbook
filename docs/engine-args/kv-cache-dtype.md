---
title: kv-cache-dtype
---

# `--kv-cache-dtype`

> KV cache 存储量化类型，直接决定 KV cache 显存占用。

| 属性 | 值 |
|---|---|
| 类型 | `str`（CacheDType） |
| 默认值 | `"auto"`（跟随模型 dtype） |
| 分类 | 调度与内存 |

## 官方定义

Data type for kv cache storage. If "auto", will use model data type... Some models (namely DeepSeekV3.2) default to fp8.（vLLM 源码 `CacheConfig.cache_dtype`）

## Ascend 语境与官方用法

- 官方教程显式取值：**fp8**（[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)：`--kv-cache-dtype fp8`，并配 `--attention_config.indexer_kv_dtype fp8`）、**int8**、**mxfp8**。
- 平台后端可注册自定义 KV cache dtype（`register_kv_cache_dtype`），Ascend 的 fp8/int8 支持即走此机制。
- 显式 fp16/bfloat16 必须与模型 dtype 一致，否则报错。
- 注意与权重 NZ（[`weight_nz_mode`](../flags/weight-nz-mode.md)）区分：后者是权重格式，本参数是 KV cache。

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## 相关参数

- [`--block-size`](block-size.md) — 官方教程常组合配置
- [`--mamba-ssm-cache-dtype`](index.md) — Mamba 类模型的对应参数
