---
title: weight_nz_mode
---

# `weight_nz_mode`

> 权重 NZ（FractalNZ）格式模式。量化模型推理性能的重要开关。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_NZ`（注意：**键名已更改**） |

## 取值

| 值 | 含义 |
|---|---|
| `0` | 禁用 NZ |
| `1` | 仅对量化权重启用 NZ（默认） |
| `2` | 在支持的情况下，对 BF16/FP16 权重也启用 NZ |

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"weight_nz_mode": 2}'
```

## 注意事项

- **迁移时键名不同**：旧环境变量名为 `VLLM_ASCEND_ENABLE_NZ`，迁移后键名为 `weight_nz_mode`，且语义从"是否启用"扩展为三档模式。
- **RL 模式强制覆盖**：启用 [`rl_config`](rl-config.md) 时，NZ 会被强制设为 `0`（RL 模式的固定行为优先于顶层 `weight_nz_mode`）。
- NZ 对矩阵乘类算子的性能影响显著，调整该开关后建议对比首 token 延迟与吞吐。

## 相关开关

- [`enable_kv_nz`](enable-kv-nz.md) — KV cache 的 NZ 布局（注意与权重 NZ 是不同开关）
- [`rl_config`](rl-config.md) — RL 模式会强制 `weight_nz_mode=0`
