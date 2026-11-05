---
title: finegrained_tp_config
---

# `finegrained_tp_config`

> 细粒度张量并行（Fine-Grained Tensor Parallelism）配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |

## 说明

将模型按模块（如 MLP、attention、embedding、LM Head）设置不同的 TP 并行粒度，替代全局统一的 TP size。相关字段（如 `embedding_tensor_parallel_size`、`mlp_tensor_parallel_size`、`oproj_tensor_parallel_size` 等）在 v0.23 起逐步收归到本配置下。

## 兼容性

- embedding / LM Head 的细粒度 TP 与 [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) **不兼容**（PCP size > 1 时二选一）。

具体字段清单以对应版本的官方文档为准。
