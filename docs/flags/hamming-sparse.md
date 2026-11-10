---
title: hamming_sparse
---

# `hamming_sparse`

> Hamming 稀疏注意力配置。⚠️ 已从源码移除（v0.30.0 起）。
> 📚 所属专题：[3. KV Cache 量化与内存格式](../feature-topics.md#t-kvfmt)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->

## 相关开关

- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — 现用稀疏注意力布局开关
- [`sparse_kv_offload_config`](sparse-kv-offload-config.md) — 稀疏 KV 卸载（现用）
