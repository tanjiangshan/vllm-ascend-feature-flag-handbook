---
title: enable_matmul_allreduce
---

# `enable_matmul_allreduce`

> Matmul + AllReduce 融合优化。**已在 v0.30.0 移除**。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ **removed**（v0.30.0 移除） |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` |

## 生命周期

- **v0.23.0**：以环境变量形式存在（`VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE`）；
- **v0.30.0 起**：源码与文档中均已移除，无直接替代开关。

## 升级指引

升级到 v0.30.0+ 时，请从部署配置中删除该环境变量，否则可能触发未知配置告警。相关的 TP 通信优化可关注 `ascend_fusion_config`（融合算子配置）的后续演进。
