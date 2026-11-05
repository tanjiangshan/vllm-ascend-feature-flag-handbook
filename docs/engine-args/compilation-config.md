---
title: compilation-config
---

# `--compilation-config`（`-cc`）

> torch.compile 与 CUDA Graph 捕获配置，生产性能的关键参数。

| 属性 | 值 |
|---|---|
| 类型 | `CompilationConfig`（JSON / 点号覆盖） |
| 默认值 | `CompilationConfig()`（各子项有默认值，如 `cudagraph_mode`） |
| 分类 | 编译与图 |

## 官方定义

`torch.compile` and cudagraph capture configuration for the model. As a shorthand, one can append compilation arguments via `-cc.parameter=argument`.（vLLM 源码 `EngineArgs.compilation_config`）

## Ascend 语境与官方用法

- 官方教程高频取值：
  - `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'`（[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)、DeepSeek-V4 系）——只对 decode 步捕获图，prefill 保持 eager，首 token 更稳；
  - `--compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,...]}'`（Qwen3-Dense 等）——显式枚举捕获尺寸。
- **细粒度 TP 联动**：最大捕获尺寸必须覆盖 `min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))`，否则相关优化自动禁用（[Fine_grained_TP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)）。
- Ascend 侧适配：vllm-ascend `platform.py` 会按显存缩减 `max_cudagraph_capture_size` 并处理 `use_inductor_graph_partition` 等选项。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
# 或点号覆盖
vllm serve Qwen/Qwen3-8B -cc.cudagraph_mode=FULL_DECODE_ONLY
```

## 相关参数

- [`--enforce-eager`](enforce-eager.md) — 本参数的"总开关反面"
- [`--max-num-seqs`](max-num-seqs.md) — 捕获尺寸上界公式输入
