---
title: sfa_dcp_force_tmajor_restore
---

# `sfa_dcp_force_tmajor_restore`

> SFA 注意力在 DCP（Decode Context Parallel）下强制 T-major 布局恢复。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | SFA 模型 + DCP |

## 用法

```bash
vllm serve <sfa-model> \
  --additional-config='{"sfa_dcp_force_tmajor_restore": true}'
```

## 注意事项

- 仅调试/兼容用途，正常部署**无需设置**。
- 强制 SFA 注意力在 DCP 恢复时采用 T-major 布局；默认走自动选择路径。
- 与 [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) 等 SFA 布局开关属于不同层面的配置。

## 相关开关

- [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) — SFA C8 缓存布局
- [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) — PCP 权重分片
