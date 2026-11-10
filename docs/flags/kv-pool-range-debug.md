---
title: kv_pool_range_debug
---

# `kv_pool_range_debug`

> KV pool 逐层范围传输审计日志。调试 KV cache 管理问题的工具开关。
> 📚 所属专题：[6. KV 复用与池化](../feature-topics.md#t-kvp)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 旧环境变量 | `VLLM_ASCEND_KVPOOL_RANGE_DEBUG`（严格二进制 `"0"`/`"1"`） |

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"kv_pool_range_debug": true}'
```

## 行为

开启后，为 KV pool 的整键操作、逐层范围和提交操作输出 JSON 审计事件，用于追踪 KV block 的分配与传输行为。

!!! warning "仅限调试"
    逐层日志有明显开销，正常运行请保持禁用。旧环境变量为严格二进制格式：取值不是 `"0"`/`"1"` 会直接抛 `ValueError`。

## 迁移

| 迁移前 | 迁移后 |
|---|---|
| `export VLLM_ASCEND_KVPOOL_RANGE_DEBUG=1` | `{"kv_pool_range_debug": true}` |

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->
