---
title: max-model-len
---

# `--max-model-len`

> 模型最大上下文长度（prompt + output），超长请求会被直接拒绝。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（从模型 config 自动推断） |
| 分类 | 调度与内存 |

## 官方定义

Model context length (prompt and output). If unspecified, will be automatically derived from the model config. When passing via `--max-model-len`, supports k/m unit suffixes.（vLLM 源码 `ModelConfig`）

## Ascend 语境与官方用法

- 官方教程几乎全部**显式设置**，因为它直接决定 KV cache 显存压力：
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) / [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html) / [Kimi-K3.1-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html)：`1048576`（1M 长上下文）
  - [GLM5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) / [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：`131072`
  - 常见还有 `133120`、`135168`、`40000` 等按模型裁剪的值
- 支持 `k`/`m` 后缀（如 `--max-model-len 128k`）。
- 与 PCP/DCP 配合时，超长 prefill 会被进一步切分到多卡（见 [`prefill-context-parallel-size`](prefill-context-parallel-size.md)）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-model-len 131072
```

## 相关参数

- [`--block-size`](block-size.md) — KV cache 分块粒度
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) — 长上下文 prefill 加速
