---
title: additional-config
---

# `--additional-config`

> 平台扩展配置（JSON 字典）。**vLLM-Ascend 全部 51 个特性开关的唯一入口。**

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 分类 | 服务端 |

## 官方定义

Additional config for specified platform. Different platforms may support different configs. Make sure the configs are valid for the platform you are using.（vLLM 源码 `VllmConfig.additional_config`，`Field(default_factory=dict)`）

## Ascend 语境

- 这是本站存在的理由：vLLM-Ascend 的 51 个特性开关（MoE 融合、RL 模式、调度扩展、Runtime Guard 等）全部通过本参数传入。
- 完整清单、默认值、版本支持与详情页见 **[特性开关总览](../flags/index.md)**。
- 官方教程几乎每条 `vllm serve` 命令都带本参数，例如：
  - `{"ascend_compilation_config": {...}}`（Qwen3 系）
  - `{"enable_cpu_binding": true, "enable_flashcomm1": true}`（[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)）

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config '{"enable_fused_mc2": 1, "weight_nz_mode": 1}'
```

## 相关

- [特性开关总览](../flags/index.md) — 51 个开关的深度参考
- [迁移对照表](../migration.md) — 环境变量 → additional-config 迁移
