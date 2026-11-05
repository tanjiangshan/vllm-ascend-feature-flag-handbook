---
title: block-size
---

# `--block-size`

> KV cache 的物理块大小（token 数），前缀缓存的命中粒度也取决于它。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（自动；vLLM 典型解析为 16，按注意力后端页大小决定） |
| 分类 | 调度与内存 |

## 官方定义

Size of a contiguous cache block in number of tokens.（vLLM 源码 `CacheConfig.block_size`，`Field(default=None, gt=0)`）

## Ascend 语境与官方用法

- 官方教程中的显式取值：**32**（[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)，配 fp8 KV cache）、**128**、**1536**（KVPP 等特性场景）。
- block_size 影响：
  - 前缀缓存命中边界（`hash_block_size` 要求整除 block_size）；
  - KV cache 内部/外部碎片比例。
- 与 [`enable_kv_nz`](../flags/enable-kv-nz.md)、KVPP 等 Ascend KV 布局特性组合时，以特性文档给出的取值为准。

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --block-size 32 --kv-cache-dtype fp8
```

## 相关参数

- [`--kv-cache-dtype`](kv-cache-dtype.md) — 常与之一起配置
- [`--enable-prefix-caching`](enable-prefix-caching.md) — 命中粒度依赖 block 边界
