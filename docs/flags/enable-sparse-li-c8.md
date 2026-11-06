---
title: enable_sparse_li_c8
---

# `enable_sparse_li_c8`

> 为稀疏注意力（Lightning Indexer）启用 C8 KV cache 布局。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | GLM-5 系列、DeepSeek 稀疏注意力模型 |

## 用法

```bash
vllm serve <glm-5> \
  --additional-config='{"enable_sparse_li_c8": true}'
```

## 注意事项

- **与 `enable_sparse_li_c4` 互斥**：后者由 `attention_config.indexer_kv_dtype = "mxfp4"` 自动派生，源码明确 `if self.enable_sparse_li_c8 and self.enable_sparse_li_c4: raise ValueError(...)`，用户不要同时开启。
- C8 布局改变 KV cache 内存格式，量化稀疏注意力下可降显存占用。
- 官方 GLM5.2 教程实测开启。

## 相关开关

- [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) — SFA 模型的 C8 布局
- [`c8_enable_reshape_optim`](c8-enable-reshape-optim.md) — C8 reshape 优化（已移除）
- [`enable_kv_nz`](enable-kv-nz.md) — KV cache NZ 布局（另一独立布局开关）
