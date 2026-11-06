---
title: enable_dsa_cp
---

# `enable_dsa_cp`

> DSA 注意力的上下文并行开关。⚠️ 已在 main 分支移除，由 PCP 取代。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ❌ removed（main 已移除） |
| 支持版本 | v0.30.0 |

## 历史用法（v0.30.0）

```bash
vllm serve <dsa-model> \
  --additional-config='{"enable_dsa_cp": true}'
```

- 与 PCP（`prefill_context_parallel_size > 1`）互斥，同时开启会在启动时报错。
- main 分支已删除该键：v0.30.0 的报错信息本身就写着 "Use PCP instead: remove enable_dsa_cp from additional_config"——升级 main 后请直接改用 PCP。

## 相关开关

- [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) — PCP 权重分片
- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — 稀疏注意力 C8 布局
- [`sfa_dcp_force_tmajor_restore`](sfa-dcp-force-tmajor-restore.md) — SFA DCP 布局恢复
