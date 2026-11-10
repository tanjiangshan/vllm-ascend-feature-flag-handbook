---
title: enable_transpose_kv_cache_by_block
---

# `enable_transpose_kv_cache_by_block`

> 融合算子路径下按块转置 KV cache。
> 📚 所属专题：[3. KV Cache 量化与内存格式](../feature-topics.md#t-kvfmt)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` |

## 说明

默认开启。该开关控制融合 attention 算子中 KV cache 的按块转置布局，属于算子级性能优化。一般**无需显式设置**；在排查 attention 算子精度或性能问题时，可作为对照变量临时关闭。

## 迁移

| 迁移前 | 迁移后 |
|---|---|
| `export VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK=1` | `{"enable_transpose_kv_cache_by_block": true}`（默认即 true，通常无需设置） |

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
