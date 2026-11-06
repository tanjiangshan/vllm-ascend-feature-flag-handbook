---
title: block-size
---

# `--block-size`

> KV cache 的物理块大小（token 数）——前缀缓存的命中粒度、碎片率都受它影响。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（"use default"，由引擎按注意力后端页大小解析，源码注释：[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)） |
| 分类 | 调度与内存 |

## 官方定义

> Size of a contiguous cache block in number of tokens.

（vLLM 源码：`CacheConfig.block_size`，`Field(default=None, gt=0)`，注释 "Accepts None (meaning 'use default'). After construction, always int."，[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)）

## 机制详解

**块是 KV cache 的分配单位**：vLLM 不按 token 逐段分配 KV，而是按固定大小的块（block）整段申请/释放。请求来了按块数要显存，结束按块归还。

**两个直接后果**：

1. **碎片**：一条长度 L 的序列占 `ceil(L / block_size)` 个块，最后一个块平均浪费一半——块越大，内部碎片越大；
2. **前缀缓存粒度**：前缀缓存以块为命中单位。块越大，命中粒度越粗（共享边界必须对齐到块），但管理开销越小。

源码中 `prefix_match_unit`（前缀命中的最细 token 边界）有整除校验："prefix-cacheable KV cache group block sizes must be divisible by prefix_match_unit"（[kv_cache_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/v1/core/kv_cache_utils.py)）——块大小与命中粒度的耦合在源码里就是硬约束。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--enable-prefix-caching`](enable-prefix-caching.md) | 命中粒度 = 块边界；细粒度命中需两者配合 |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | KV 量化改变每 token 字节数，与块大小共同决定单块显存 |
| Ascend KV 布局开关（[`enable_kv_nz`](../flags/enable-kv-nz.md)、KVPP） | 布局特性对块大小/对齐另有要求，以特性文档为准 |

经验判断：块小 → 碎片少、命中细，但元数据开销大；块大 → 管理省，但碎片和命中粒度粗。默认值（引擎按后端页大小解析）对大多数场景已合适，**官方教程显式改它都有明确原因**（见下）。

## Ascend 语境与官方用法

- 官方教程显式取值及语境：
  - **32**——[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)，配合 `--kv-cache-dtype fp8`（fp8 KV 的块布局）
  - **128** / **1536**——KVPP 等 KV 池化特性场景
- 不要照搬异构值：128/1536 属于特定特性组合，常规部署用解析默认值即可。

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --block-size 32 --kv-cache-dtype fp8
```

## 相关参数

- [`--kv-cache-dtype`](kv-cache-dtype.md) — 官方教程常与之组合
- [`--enable-prefix-caching`](enable-prefix-caching.md) — 命中粒度依赖块边界
