---
title: speculative-config
---

# `--speculative-config`

> 投机解码配置（JSON）：草稿模型先猜多个 token，主模型一次验证——用算力换 TPOT。

| 属性 | 值 |
|---|---|
| 类型 | `dict[str, Any]`（JSON） |
| 默认值 | `None`（不启用） |
| 分类 | 投机解码 |

## 官方定义

> Speculative decoding configuration.

（vLLM 源码：`SpeculativeConfig`，[config/speculative.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/speculative.py)）

## 机制详解

**原理**：decode 每步主模型只产 1 个 token。投机解码让轻量草稿模型先猜 `num_speculative_tokens` 个，主模型**并行验证**——猜对的部分一步全收。 acceptance rate 高时，一个主模型步当多个步用，TPOT 成倍下降。

**代价必须算清**：

- 草稿模型本身吃显存、吃算力（每步多一次草稿前向）；
- 猜不中的步纯浪费——**acceptance 低时反而变慢**；
- 调度变复杂：每步要排"草稿前向 + 主模型验证"两段。

**关键 JSON 字段**（官方教程实证）：

| 字段 | 作用 |
|---|---|
| `method` | 草稿方法，Ascend 教程用 **dspark**（DeepSpark） |
| `num_speculative_tokens` | 每步猜几个（教程常见 5–7） |
| `model` | 草稿模型路径（自投机时同主模型） |
| `draft_tensor_parallel_size` | 草稿侧并行度（可小于主模型） |
| `draft_sample_method` | 草稿采样方式（如 `greedy`） |
| `enforce_eager` | 草稿侧是否跳过图捕获（Kimi-K3 配方为 `true`） |

## 参数联动

**与调度的联动（源码级）**：投机解码让步内 token 数变成 `1 + num_speculative_tokens` 的倍数。源码中调度器的 `max_num_scheduled_tokens` "通常等于 `max_num_batched_tokens`，但在模型会往 batch 里追加 token 的情况下（如投机解码）可以更小"（[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py) 字段说明）。

**与图捕获的联动**：捕获尺寸枚举需覆盖 `1 + n` 形状——细粒度 TP 的公式 `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))` 里就有它（[Fine_grained_TP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)）。

**与 PCP 的兼容性**（[Ascend 上下文并行指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)）：MLA + PCP 仅支持 MTP 草稿；GQA + PCP 仅支持 Eagle3。

**Ascend 配套开关**：

| 开关 | 作用 |
|---|---|
| [`dynamic_spec_config`](../flags/dynamic-spec-config.md) | 按接受率动态调投机参数 |
| [`enable_flashcomm1`](../flags/enable-flashcomm1.md) | MRv1 投机通信优化 |
| [`rejection_sampler_config`](../flags/rejection-sampler-config.md) | RL rollout 的验收采样配置 |

## Ascend 语境与官方用法

- 官方教程的 Ascend 推荐方法：**dspark**（DeepSpark）。
  - [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)：`--speculative-config '{"num_speculative_tokens":5,"method":"dspark"}'`
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：dspark + `draft_tensor_parallel_size:8` + `draft_sample_method:"greedy"` + `num_speculative_tokens:7`，草稿侧 `enforce_eager:true`
- 常与 [`--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'`](compilation-config.md) 组合。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --speculative-config '{"method":"dspark","num_speculative_tokens":5}'
```

## 相关参数

- [`--compilation-config`](compilation-config.md) — 捕获尺寸需覆盖投机形状
- [`--max-num-seqs`](max-num-seqs.md) — 捕获尺寸公式的另一个输入
- [`dynamic_spec_config`](../flags/dynamic-spec-config.md) — Ascend 动态投机
