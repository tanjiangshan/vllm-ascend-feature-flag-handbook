---
title: speculative-config
---

# `--speculative-config`

> 投机解码配置（JSON），用草稿模型预测多个 token 加速 decode。

| 属性 | 值 |
|---|---|
| 类型 | `dict[str, Any]`（JSON） |
| 默认值 | `None`（不启用） |
| 分类 | 投机解码 |

## 官方定义

Speculative decoding configuration.（vLLM 源码 `SpeculativeConfig`）

## Ascend 语境与官方用法

- 官方教程的 Ascend 推荐方法：**dspark**（DeepSpark）。
  - [DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)：`--speculative-config '{"num_speculative_tokens":5,"method":"dspark"}'`
  - [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：dspark + `draft_tensor_parallel_size:8` + `draft_sample_method:"greedy"`，草稿侧 `enforce_eager:true`，`num_speculative_tokens:7`
- 兼容性（[上下文并行指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)）：MLA + PCP 仅支持 MTP；GQA + PCP 仅支持 Eagle3。
- Ascend 侧专属开关联动：[`dynamic_spec_config`](../flags/dynamic-spec-config.md)（动态投机）、[`enable_flashcomm1`](../flags/enable-flashcomm1.md)（MRv1 通信优化）、[`rejection_sampler_config`](../flags/rejection-sampler-config.md)（RL 验收）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --speculative-config '{"method":"dspark","num_speculative_tokens":5}'
```

## 相关参数

- [`--compilation-config`](compilation-config.md) — 常与 `FULL_DECODE_ONLY` 组合
- [`--max-num-seqs`](max-num-seqs.md) — cudagraph 覆盖公式含 `num_speculative_tokens`
