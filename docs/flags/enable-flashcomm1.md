---
title: enable_flashcomm1
---

# `enable_flashcomm1`

> 启用 SP MoE 的 FlashComm1 通信优化。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_ENABLE_FLASHCOMM1` |
| 适用 | MoE 模型，Model Runner V1 + 序列并行 |

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_flashcomm1": true}'
```

## 限制

- **仅 Model Runner V1 支持**，且需要序列并行；启用后会自动启用 FlashComm；
- **Model Runner V2 下设置为 `true` 会直接报配置错误**——MRv2 请改用 PCP（见官方上下文并行文档）；
- DSA-CP 配置已解耦：依赖 FC1 隐式启用 DSA-CP 的用户，现需同时显式设置 DSA-CP 相关配置（见 release notes 的解耦说明）。

## 迁移

| 迁移前 | 迁移后 |
|---|---|
| `export VLLM_ASCEND_ENABLE_FLASHCOMM1=1` | `{"enable_flashcomm1": true}` |

## 相关开关

- [enable_fused_mc2](enable-fused-mc2.md) — MoE 融合路径（常与通信优化配合调优）
- [mc2_comm_alg](mc2-comm-alg.md) — dispatch/combine 通信算法
