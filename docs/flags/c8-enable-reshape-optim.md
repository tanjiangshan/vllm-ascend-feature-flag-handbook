---
title: c8_enable_reshape_optim
---

# `c8_enable_reshape_optim`

> LI-C8 的 reshape 优化。⚠️ 已从源码移除（v0.30.0 起）。
> 📚 所属专题：[3. KV Cache 量化与内存格式](../feature-topics.md#t-kvfmt)

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

- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — LI-C8 稀疏缓存（现用）
- [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) — SFA-C8 稀疏缓存
