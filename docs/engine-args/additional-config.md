---
title: additional-config
---

# `--additional-config`

> 平台扩展配置（JSON 字典）——**vLLM-Ascend 全部 64 个特性开关的唯一入口**，本站存在的理由。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 分类 | 服务端 |

## 官方定义

> Additional config for specified platform. Different platforms may support different configs. Make sure the configs are valid for the platform you are using. Contents must be hashable.

（vLLM 源码：`VllmConfig.additional_config`，`Field(default_factory=dict)`，[config/vllm.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/vllm.py)）

## 机制详解

**分层设计**：vLLM 主干的 CLI 参数只有引擎通用项；平台（CUDA/ROCm/NPU）的专有配置走这条"透传通道"——vLLM 不解析内容，原样交给平台插件校验。vLLM-Ascend 插件在这里消费**全部 64 个特性开关**（MoE 融合、RL 模式、调度扩展、Runtime Guard 等）。

**键的来源**：合法的键名在 vllm-ascend 源码 `vllm_ascend/ascend_config.py` 与 `vllm_ascend/envs.py` 定义，本站[特性开关总览](../flags/index.md)逐键核验过——**找不到出处的一律不收**。

**注意"hashable"约束**（源码 docstring 原文）：内容必须可哈希（参与配置缓存键），即 JSON 值用基本类型/不可变结构。

**迁移背景**：PR #9064 起，vLLM-Ascend 的环境变量开关统一迁移到 `--additional-config`；过渡期两者并存，环境变量未来移除。对照表见[迁移对照表](../migration.md)。

## 用法分层

```bash
# 单键
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_fused_mc2": 1}'

# 组合（官方教程常态）
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_cpu_binding":true,"enable_flashcomm1":true}'

# 嵌套（编译配置）
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"ascend_compilation_config":{"enable_npugraph_ex":true,"enable_static_kernel":false}}'
```

## 参数联动

| 联动对象 | 关系 |
|---|---|
| 64 个特性开关 | 全部经本参数传入，见[特性开关总览](../flags/index.md) |
| [`--compilation-config`](compilation-config.md) | vLLM 层图配置；Ascend 层的 `ascend_compilation_config` 走本参数，两者分工见该页 |
| [`--enforce-eager`](enforce-eager.md) | 平台层图模式的裁决输入之一 |
| [`--quantization`](quantization.md) | `weight_nz_mode` 等量化布局开关走本参数 |

## Ascend 语境

- 官方教程几乎每条 `vllm serve` 命令都带本参数，高频组合如：
  - `{"ascend_compilation_config": {...}}`（Qwen3 系）
  - `{"enable_cpu_binding": true, "enable_flashcomm1": true}`（[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)）
- 每个开关的默认值、状态、版本支持、风险标注见[特性开关总览](../flags/index.md)；详情页之间互链成环。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config '{"enable_fused_mc2": 1, "weight_nz_mode": 1}'
```

## 相关

- [特性开关总览](../flags/index.md) — 64 个开关的深度参考（默认值/版本/风险）
- [迁移对照表](../migration.md) — 环境变量 → additional-config 迁移
- [版本支持矩阵](../version-matrix.md) — 每个开关在 v0.23.0 / v0.30.0 / main 的支持情况
