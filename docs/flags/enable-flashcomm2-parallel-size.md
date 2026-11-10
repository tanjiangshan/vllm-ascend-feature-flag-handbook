---
title: enable_flashcomm2_parallel_size
---

# `enable_flashcomm2_parallel_size`

> FlashComm2 并行规模。**已在 v0.30.0 移除**。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
