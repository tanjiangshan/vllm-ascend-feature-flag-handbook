---
title: enable_sparse_sfa_c8
---

# `enable_sparse_sfa_c8`

> 为 SFA（Sparse Flash Attention）稀疏注意力启用 C8 KV cache 布局。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | GLM-5 / GLM-5.2 等 SFA 模型 |

## 用法

```bash
vllm serve <glm-5> \
  --additional-config='{"enable_sparse_sfa_c8": true}'
```

## 注意事项

- 仅对 SFA 稀疏注意力模型生效；GQA/MHA 或混合注意力模型开启无效果。
- 官方 GLM5 / GLM5.2 教程实测开启。

## 相关开关

- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — Lightning Indexer 的 C8 布局
- [`sfa_dcp_force_tmajor_restore`](sfa-dcp-force-tmajor-restore.md) — SFA DCP 布局恢复
