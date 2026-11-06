---
title: enable_sparse_sfa_c8
---

# `enable_sparse_sfa_c8`

> 为 SFA（Sparse Flash Attention）稀疏注意力启用 C8 KV cache 布局。⚠️ v0.30.0 起改为派生量，`additional-config` 传本键不再生效。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ removed（v0.30.0 起被派生覆盖） |
| 支持版本 | v0.23.0 |

## 启用方式对照

| 版本 | 写法 |
|---|---|
| v0.23.0 | `--additional-config '{"enable_sparse_sfa_c8": true}'` |
| v0.30.0 / main | `--kv-cache-dtype int8`（或 `fp8`） |

v0.30.0 起 `derive_and_validate` 无条件覆盖：

```python
enable_sparse_sfa_c8 = cache_config.cache_dtype in ["fp8", "int8"] and use_sparse_sfa
```

即：SFA 稀疏注意力模型只要 `--kv-cache-dtype` 是 fp8/int8，SFA-C8 布局自动启用。

## 联动

- 官方 GLM5 / GLM5.2 教程实测写法：`--kv-cache-dtype fp8 --attention_config.indexer_kv_dtype fp8` 成对出现——SFA 模型的 KV dtype 跟 `--kv-cache-dtype`，Lightning Indexer 稀疏层的 KV dtype 跟 `indexer_kv_dtype`。
- P/D 两侧取值必须一致，否则 KV 传输后不能直接复用。

## 相关参数

- [`--kv-cache-dtype`](../engine-args/kv-cache-dtype.md) — SFA-C8 的实际开关（v0.30.0 起）
- [`--attention-config`](../engine-args/index.md) — `indexer_kv_dtype` 宿主
- `enable_sparse_sfa_turboquant` — `cache_dtype = turboquant_4bit_nc` 时派生
