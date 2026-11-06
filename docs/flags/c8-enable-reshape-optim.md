---
title: c8_enable_reshape_optim
---

# `c8_enable_reshape_optim`

> LI-C8 的 reshape 优化。⚠️ 已从源码移除（v0.30.0 起）。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ removed |
| 移除版本 | v0.30.0 |

## 历史用法（v0.23.0）

```bash
vllm serve <model> \
  --additional-config='{"enable_sparse_li_c8": true, "c8_enable_reshape_optim": true}'
```

- 仅在 [`enable_sparse_li_c8`](enable-sparse-li-c8.md) 开启时生效，用于 C8 布局的 reshape 优化。
- v0.30.0 起源码已无读取点，设置无效。

## 相关开关

- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — LI-C8 稀疏缓存（现用）
- [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) — SFA-C8 稀疏缓存
