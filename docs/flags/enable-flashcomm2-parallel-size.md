---
title: enable_flashcomm2_parallel_size
---

# `enable_flashcomm2_parallel_size`

> FlashComm2 并行规模。**已在 v0.30.0 移除**。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `0` |
| 状态 | ❌ **removed**（v0.30.0 移除） |
| 旧环境变量 | `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` |

## 生命周期

- **v0.23.0**：配置键 + 环境变量回退均存在（PR #9064 迁移对象之一）；
- **v0.30.0 起**：源码与文档中均已移除。

## 升级指引

升级到 v0.30.0+ 时，请从配置中删除该键及对应环境变量。FlashComm 系列优化在 v0.30.0 的演进以 [`enable_flashcomm1`](enable-flashcomm1.md) 与 PCP 方案为准。
