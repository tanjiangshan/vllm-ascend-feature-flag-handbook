---
title: combine_quant_mode
---

# `combine_quant_mode`

> 融合 combine 算子的通信量化模式（v0.30.0 新增）。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `0` |
| 状态 | ✅ active（v0.30.0 新增） |
| 适用 | [`enable_fused_mc2`](enable-fused-mc2.md) 融合路径 |

## 作用

作为 `comm_quant_mode` 参数传给 `torch_npu.npu_moe_distribute_combine_v2` 算子，控制融合 combine 阶段的通信量化方式。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_fused_mc2": 1, "combine_quant_mode": 2}'
```

!!! note "有效值范围"
    有效取值范围以算子文档为准，不同 CANN 版本支持情况可能不同。

## 相关开关

- [enable_fused_mc2](enable-fused-mc2.md) — 融合 MC2 总开关
- [mc2_comm_alg](mc2-comm-alg.md) — 通信算法选择
