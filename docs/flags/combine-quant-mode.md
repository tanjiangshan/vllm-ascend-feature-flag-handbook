---
title: combine_quant_mode
---

# `combine_quant_mode`

> 融合 combine 算子的通信量化模式（v0.30.0 新增）。
> 📚 所属专题：[1. MoE 通信与计算重叠](../feature-topics.md#t-moe)

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `0` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | [`enable_fused_mc2`](enable-fused-mc2.md) 融合路径 |

## 作用

作为 `comm_quant_mode` 参数传给 `torch_npu.npu_moe_distribute_combine_v2` 算子，控制融合 combine 阶段的通信量化方式。

## 取值

源码类型 `Literal[0, 2, 3, 4]`，默认 `0`：

| 值 | 语义 | 依据 |
|---|---|---|
| `0` | 禁用强制量化，沿用模型自身 quant_type | 源码注释 + 官方配置文档 |
| `4` | MXFP float8_e4m3 通信量化 | 源码注释 + DeepSeek-V4 官方配方（D 节点） |
| `2` / `3` | 源码 Literal 允许，**官方文档未说明语义**（原文指向算子文档） | 官方配置文档 |

!!! note "有效值范围"
    有效取值范围以算子文档为准，不同 CANN 版本支持情况可能不同。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_fused_mc2": 1, "combine_quant_mode": 2}'
```

!!! note "有效值范围"
    有效取值范围以算子文档为准，不同 CANN 版本支持情况可能不同。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ✅ D 节点 |

DeepSeek-V4-Pro/Flash 教程原文：combine_quant_mode: 4「forces the MoE MC2 combine stage on Decode nodes to use FP8 … communication quantization」；官方配方中该键配在 D 节点。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_fused_mc2](enable-fused-mc2.md) — 融合 MC2 总开关
- [mc2_comm_alg](mc2-comm-alg.md) — 通信算法选择
