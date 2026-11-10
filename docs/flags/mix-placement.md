---
title: mix_placement
---

# `mix_placement`

> 混合放置模式（DP×TP 平面上的专家/权重放置策略），计入 RFork 权重传输的兼容性指纹。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | MoE 模型 + RFork 权重传输场景 |

## 用法

```bash
vllm serve <model> \
  --additional-config='{"mix_placement": true}'
```

## 注意事项

- **必须收发两端一致**：`mix_placement` 是 RFork 兼容性指纹的组成部分，发送端与接收端配置不一致会导致指纹不匹配、权重传输失败。
- 影响 MoE 专家在 DP×TP 平面上的放置布局，与 [`finegrained_tp_config`](finegrained-tp-config.md)、[`enable_shared_expert_dp`](enable-shared-expert-dp.md) 等分片策略相关。
- 正常在线推理无需显式设置；仅在使用 RFork 热迁移/重放权重时需要关注。

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

- [`finegrained_tp_config`](finegrained-tp-config.md) — 细粒度张量并行
- [`enable_shared_expert_dp`](enable-shared-expert-dp.md) — 共享专家数据并行
