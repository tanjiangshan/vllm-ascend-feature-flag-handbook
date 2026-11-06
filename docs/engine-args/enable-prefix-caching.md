---
title: enable-prefix-caching
---

# `--enable-prefix-caching` / `--no-enable-prefix-caching`

> 前缀缓存：复用相同前缀的 KV block，多轮对话/共享 system prompt 场景的 TTFT 利器。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `None`（按模型/后端自动判断，见下） |
| 分类 | 调度与内存 |

## 官方定义

> Whether to enable prefix caching.

（vLLM 源码：`CacheConfig.enable_prefix_caching`，[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)）

## 机制详解

**原理**：请求 1 的 prompt 和请求 2 的 prompt 共享一段前缀（比如相同的 system prompt 或多轮对话历史）时，这段前缀的 KV block 完全相同。开启后，调度器对块内容做哈希，相同内容的块直接复用——请求 2 跳过整段前缀的 prefill 计算，TTFT 直接砍掉这部分。

**默认值的自动解析**（CLI 不传时，`EngineArgs` 按模型能力自动判断，[arg_utils.py `_set_default_chunked_prefill_and_prefix_caching_args`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)）：

```
None → model_config.is_prefix_caching_supported（模型/后端支持则自动开启）
```

也就是说 main 上"不设"通常等于"开"——除非模型或后端明确不支持。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--block-size`](block-size.md) | 命中粒度 = 块边界；`prefix_match_unit` 须整除块大小（源码硬校验） |
| [`--kv-transfer-config`](kv-transfer-config.md) | **PD 分离时显式关闭**（见下） |
| Ascend KV 布局开关（[`enable_kv_nz`](../flags/enable-kv-nz.md)） | 影响前缀缓存的底层块布局 |

**与 PD 分离的冲突**（重要）：官方 [PD 分离（Mooncake）教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html)中，prefill 和 decode 节点都显式传 **`--no-enable-prefix-caching`**。原因：PD 架构下 KV 在节点间传输，前缀复用语义已由 KV 传输层接管，再开本地前缀缓存会造成语义重复/冲突。记住口诀：**走 PD 关本地前缀缓存**。

## 调优思路

| 场景 | 建议 |
|---|---|
| 多轮对话 / 共享 system prompt | **开启**（默认自动开启一般已够），TTFT 收益显著 |
| PD 分离部署 | **关闭**（`--no-enable-prefix-caching`，官方教程做法） |
| 单轮短 prompt、无共享前缀 | 收益为零，开不开无所谓 |

## Ascend 语境与官方用法

- PD 分离教程（Mooncake 单节点/多节点）：prefill、decode 节点均 `--no-enable-prefix-caching`。
- 常规在线服务：依赖自动解析即可（默认开）。

## 用法

```bash
# 常规服务（显式开）
vllm serve Qwen/Qwen3-8B --enable-prefix-caching

# PD 分离节点（按官方教程关）
vllm serve Qwen/Qwen3-8B --no-enable-prefix-caching --kv-transfer-config '{...}'
```

## 相关参数

- [`--block-size`](block-size.md) — 命中粒度
- [`--kv-transfer-config`](kv-transfer-config.md) — PD 分离时二者联动
