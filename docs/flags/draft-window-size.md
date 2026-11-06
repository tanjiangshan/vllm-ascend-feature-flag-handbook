---
title: draft_window_size
---

# `draft_window_size`

> 投机解码的草稿 KV 滑窗：仅将草稿模型注意力限制在最近 N 个 token，目标模型仍用全上下文，输出质量不变。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `None`（不启用滑窗） |
| 状态 | ✅ active |
| 适用 | 投机解码（eagle3 / dflash / dspark）长上下文场景 |

## 用法

```bash
vllm serve <model> \
  --speculative-config '{"method": "dspark", "model": "path/to/draft", "num_speculative_tokens": 7, "enforce_eager": true}' \
  --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}' \
  --additional-config '{"draft_window_size": 2048}'
```

## 机制

- 草稿模型注意力被限制在最近 `draft_window_size` 个 token；超出部分不可见。
- 目标模型仍 attend 全上下文，**最终输出质量不受影响**——牺牲的是草稿的远距离注意力视野。
- 适用场景：上下文远超草稿训练长度时，草稿注意力"越界"导致接受率崩塌、投机变成开销。

## 注意事项

- 仅对 eagle3 / dflash / dspark 投机方法生效；其他方法忽略。
- `None` 表示不启用滑窗（默认行为）。
- 设得过小可能降低接受率；建议按草稿模型的有效训练上下文长度取整。

## 相关开关

- [`rejection_sampler_config`](rejection-sampler-config.md) — 拒绝采样器（投机的另一半）
- [`dynamic_spec_config`](dynamic-spec-config.md) — 动态投机解码配置
