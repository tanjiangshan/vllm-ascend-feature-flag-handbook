---
title: enable_sparse_li_c8
---

# `enable_sparse_li_c8`

> 为稀疏注意力（Lightning Indexer）启用 C8 KV cache 布局。⚠️ v0.30.0 起改为派生量，`additional-config` 传本键不再生效。
> 📚 所属专题：[3. KV Cache 量化与内存格式](../feature-topics.md#t-kvfmt)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ removed（v0.30.0 起被派生覆盖） |
| 支持版本 | v0.23.0 |

## 启用方式对照

| 版本 | 写法 |
|---|---|
| v0.23.0 | `--additional-config '{"enable_sparse_li_c8": true}'` |
| v0.30.0 / main | `--attention_config.indexer_kv_dtype int8`（或 `fp8`） |

v0.30.0 起 `derive_and_validate` 无条件覆盖：

```python
enable_sparse_li_c8 = attention_config.indexer_kv_dtype in ["fp8", "int8"] and use_sparse
```

即：只要 `indexer_kv_dtype` 是 fp8/int8 且模型本身是稀疏注意力架构，C8 布局自动启用——不再需要（也不能）用 `additional-config` 手动开。

## 联动与互斥

- **与 `enable_sparse_li_c4` 互斥**：`indexer_kv_dtype = "mxfp4"` 时派生 `enable_sparse_li_c4`，与 C8 路径互斥（源码有防御性 `ValueError`）。一个 `indexer_kv_dtype` 只能取一个值，天然二选一。
- **P/D 两侧 dtype 必须一致**：官方教程强调 `--kv-cache-dtype` 与 `--attention_config.indexer_kv_dtype` 在 P 和 D 节点要配成同样的值，否则传输的 KV 不能直接复用。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ✅ D 节点 |

GLM5.2 PD 配方中配在 D 节点（kv_consumer）；GLM5 优化表按吞吐场景区分：高吞吐/PD 场景开启、低延迟场景关闭。v0.30.0 起由 --attention_config.indexer_kv_dtype 派生。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html)
<!-- DEPLOY_END -->

## 相关参数

- [`--attention-config`](../engine-args/index.md) — `indexer_kv_dtype` 的宿主参数（v0.30.0 起 C8 的实际开关）
- [`--kv-cache-dtype`](../engine-args/kv-cache-dtype.md) — 全模型 KV 存储 dtype（SFA 模型 C8 由它派生）
- `enable_sparse_li_c4` — mxfp4 路径（派生量）
