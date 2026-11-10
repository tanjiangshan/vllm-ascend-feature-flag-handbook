---
title: enable_dsa_cp
---

# `enable_dsa_cp`

> DSA 注意力的上下文并行开关。⚠️ 已在 main 分支移除，由 PCP 取代。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | — 不适用 |
| PD 分离 | — 不适用 |

v0.30.0 专属开关，main 已移除（启动报错提示改用 PCP），无部署形态意义。

出处：`vllm_ascend/ascend_config.py @ main`
<!-- DEPLOY_END -->

## 相关开关

- [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) — PCP 权重分片
- [`enable_sparse_li_c8`](enable-sparse-li-c8.md) — 稀疏注意力 C8 布局
- [`sfa_dcp_force_tmajor_restore`](sfa-dcp-force-tmajor-restore.md) — SFA DCP 布局恢复
