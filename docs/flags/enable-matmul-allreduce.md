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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
