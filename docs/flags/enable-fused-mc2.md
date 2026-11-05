---
title: enable_fused_mc2
---

# `enable_fused_mc2`

> 融合 MC2（MoE dispatch/combine）路径选择。MoE 推理性能的关键开关之一。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `0` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_FUSED_MC2`（整数语义不变） |
| 适用 | MoE 模型；A2 / A3 / A5 |

## 取值

| 值 | 含义 |
|---|---|
| `0` | 禁用融合路径（默认） |
| `1` | 使用 dispatch-FFN-combine 融合算子 |
| `2` | 在模型与并行配置支持时，选择 CANN MegaMoe 融合算子 |

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_fused_mc2": 1}'
```

## 注意事项

- **A5 + MegaMoe（值 2）的前置条件**：SiTU 模型需要暴露 `activation` 和 `activation_params` 两个参数的 CANN MegaMoe 包装器，这两个参数在初始化时从 MoE 配置绑定。
- **负载上限**：融合路径中每个 rank 的 token 容量由 [`mega_moe_max_tokens`](mega-moe-max-tokens.md)（默认 65536）控制，超过可能出现精度下降，需按实际 expert 负载分布调整。
- **量化组合**：与 [`combine_quant_mode`](combine-quant-mode.md) 搭配可设置融合算子的通信量化模式。

## 相关开关

- [`mega_moe_max_tokens`](mega-moe-max-tokens.md) — 融合路径 token 容量上限
- [`combine_quant_mode`](combine-quant-mode.md) — 融合 combine 算子的通信量化
- [`mc2_comm_alg`](mc2-comm-alg.md) — dispatch/combine 的通信算法选择
