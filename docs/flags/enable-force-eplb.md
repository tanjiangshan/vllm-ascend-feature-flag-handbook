---
title: enable_force_eplb
---

# `enable_force_eplb`

> 强制确定性轮询专家路由，用于测量 EPLB 性能上限。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（仅限分析用途） |
| 适用 | MoE 模型 |

!!! danger "切勿用于生产"
    本开关会**替换真实的 MoE 路由输出**，模型结果与精度**完全无效**。它仅用于测量 EPLB 的性能上限（理想负载均衡下的吞吐），是性能分析工具，不是功能开关。

## 互斥关系

- 不可与 `eplb_config.dynamic_eplb` 同时启用（启动会报错）。

## 用法（仅性能分析场景）

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_force_eplb": true}'
```

测量得到的吞吐可视为 EPLB 优化的目标上限，用于评估 [`dynamic_eplb`](dynamic-eplb.md) 的实际收益。

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

- [`dynamic_eplb`](dynamic-eplb.md) — 真正可用的动态负载均衡
