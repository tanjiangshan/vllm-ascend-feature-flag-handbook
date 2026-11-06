---
title: hamming_sparse
---

# `hamming_sparse`

> Hamming 稀疏注意力配置。⚠️ 已从源码移除（v0.30.0 起）。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{"enabled": false, "sparse_json_location": ""}` |
| 状态 | ❌ removed |
| 移除版本 | v0.30.0 |

## 历史用法（v0.23.0）

```bash
vllm serve <model> \
  --additional-config='{"hamming_sparse": {"enabled": true, "sparse_json_location": "/path/to/sparse.json"}}'
```

- `sparse_json_location` 必须是真实存在的 JSON 文件，否则启动报错 `Hamming sparse config json file doesn't exist.`。
- 该开关在 v0.23.0 用于启用 Hamming 稀疏注意力；v0.30.0 起源码已无读取点，等同于未设置。

## 相关开关

- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — 现用稀疏注意力布局开关
- [`sparse_kv_offload_config`](sparse-kv-offload-config.md) — 稀疏 KV 卸载（现用）
