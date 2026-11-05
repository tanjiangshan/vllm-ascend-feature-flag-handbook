---
title: mega_moe_max_tokens
---

# `mega_moe_max_tokens`

> 融合 MC2/MegaMoe 路径中 dispatch 后每个 rank 的 token 容量参考值。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `65536` |
| 状态 | ✅ active |
| 适用 | MoE 模型 + [`enable_fused_mc2`](enable-fused-mc2.md) 融合路径 |

## 作用

该值同时作为：

- `dispatch_ffn_combine` 算子的 `max_output_size`；
- CANN MegaMoe 缓冲区的 `max_recv_token_num`。

## 风险

!!! warning "超容量精度下降"
    若某个 rank 的实际 MoE 负载超过该值，**可能出现精度下降**。绝对安全上限为：

    ```
    num_max_tokens_per_rank * ep_world_size * min(num_topk, expert_per_rank)
    ```

    但直接使用安全上限会消耗非常大的设备内存，应**按实际 expert 负载分布调整**。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_fused_mc2": 2, "mega_moe_max_tokens": 32768}'
```

## 相关开关

- [enable_fused_mc2](enable-fused-mc2.md) — 融合路径总开关
- [enable_prefill_mc2](enable-prefill-mc2.md) — prefill 批次的 MC2 容量策略
