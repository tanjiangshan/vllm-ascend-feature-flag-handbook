---
title: enable_mc2_hierarchy_comm
---

# `enable_mc2_hierarchy_comm`

> 跨节点 MoE 通信（ROCE）开关。**已弃用**，请改用 [`mc2_comm_alg`](mc2-comm-alg.md)。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ⚠️ **deprecated**（将由 `mc2_comm_alg = "hierarchy"` 取代） |
| 适用 | A2 / A3 |

## 迁移

| 旧写法 | 新写法 |
|---|---|
| `{"enable_mc2_hierarchy_comm": true}` | `{"mc2_comm_alg": "hierarchy"}` |

## 说明

该开关启用 dispatch/combine 算子的节点间 ROCE 通信。v0.30.0 起由 [`mc2_comm_alg`](mc2-comm-alg.md) 的 `"hierarchy"` 取值统一接管，本开关保留仅为过渡期兼容，未来版本将移除。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见混部/PD 分离说明；已知约束：以 ROCE 做 dispatch/combine 跨节点通信，将被 mc2_comm_alg="hierarchy" 取代。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)
<!-- DEPLOY_END -->
