---
title: enable-prefix-caching
---

# `--enable-prefix-caching` / `--no-enable-prefix-caching`

> 前缀缓存：复用相同前缀的 KV block，降低长 prompt 场景的 TTFT。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `None`（按模型/后端自动判断） |
| 分类 | 调度与内存 |

## 官方定义

Whether to enable prefix caching.（vLLM 源码 `CacheConfig.enable_prefix_caching`）

## Ascend 语境与官方用法

- 官方 [PD 分离（Mooncake）教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html)中，prefill 和 decode 节点都显式传 **`--no-enable-prefix-caching`**——PD 场景下前缀缓存语义由 KV 传输层接管，不要重复开启。
- 常规在线服务（多轮对话、共享 system prompt）建议开启。
- Ascend 专属：KV cache 池化/布局开关（如 [`enable_kv_nz`](../flags/enable-kv-nz.md)）会影响前缀缓存的底层布局。

## 用法

```bash
# 常规服务
vllm serve Qwen/Qwen3-8B --enable-prefix-caching
# PD 分离节点（按官方教程）
vllm serve Qwen/Qwen3-8B --no-enable-prefix-caching --kv-transfer-config '{...}'
```

## 相关参数

- [`--block-size`](block-size.md) — 前缀缓存命中粒度
- [`--kv-transfer-config`](kv-transfer-config.md) — PD 分离时二者联动
