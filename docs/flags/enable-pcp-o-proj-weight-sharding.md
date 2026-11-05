---
title: enable_pcp_o_proj_weight_sharding
---

# `enable_pcp_o_proj_weight_sharding`

> PCP 组内 O 投影权重分片（v0.30.0 新增）。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | PCP（Prefill Context Parallel）注意力路径 |

## 作用

控制 PCP 是否在组内对 O 投影权重分片：

- **SFA-PCP**：分片 `o_proj`；
- **DSA-PCP**：分片两阶段 O 投影（`wo_a` / `wo_b`）。

## 行为细节

- 若权重方法或 PCP 分区不支持分片，该选项会**给出警告并自动禁用**，不会启动失败；
- 可在服务启动时显式设为 `false` 关闭分片；
- **其他注意力后端不使用此选项**。

## 相关开关

- [enable_pcp_embedding_lmhead_weight_sharding](enable-pcp-embedding-lmhead-weight-sharding.md) — embedding / LM Head 的 PCP 分片
