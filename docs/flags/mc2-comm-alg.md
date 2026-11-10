---
title: mc2_comm_alg
---

# `mc2_comm_alg`

> dispatch/combine 算子的通信算法选择（v0.30.0 新增），用于取代已弃用的 [`enable_mc2_hierarchy_comm`](enable-mc2-hierarchy-comm.md)。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `""` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | MoE 模型；A2 / A3 |

## 取值

| 值 | 含义 | 芯片支持 |
|---|---|---|
| `""` | 默认算法 | 全部 |
| `"fullmesh"` | 全互联算法 | 全部 |
| `"hierarchy"` | 层次化算法（跨节点 ROCE） | 仅 A2 / A3 |
| `"fullmesh_v2"` | 全互联算法 v2 | 目前仅 A3 |

## 用法

```bash
# 跨节点 MoE 通信走层次化算法
vllm serve Qwen/Qwen3-8B --additional-config='{"mc2_comm_alg": "hierarchy"}'
```

## 与旧开关的关系

| 旧写法（deprecated） | 新写法 |
|---|---|
| `{"enable_mc2_hierarchy_comm": true}` | `{"mc2_comm_alg": "hierarchy"}` |

源码中设置 `mc2_comm_alg = "hierarchy"` 会自动等效旧的 hierarchy 行为；两者同时设置时以 `mc2_comm_alg` 为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见混部/PD 分离说明；已知芯片约束："hierarchy" 仅 A2/A3，"fullmesh_v2" 当前仅 A3。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_mc2_hierarchy_comm](enable-mc2-hierarchy-comm.md) — 已弃用的旧开关
- [enable_fused_mc2](enable-fused-mc2.md) — 融合 MC2 路径
- [mega_moe_max_tokens](mega-moe-max-tokens.md) — 融合路径 token 容量
