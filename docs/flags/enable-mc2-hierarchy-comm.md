---
title: enable_mc2_hierarchy_comm
---

# `enable_mc2_hierarchy_comm`

> 跨节点 MoE 通信（ROCE）开关。**已弃用**，请改用 [`mc2_comm_alg`](mc2-comm-alg.md)。

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
