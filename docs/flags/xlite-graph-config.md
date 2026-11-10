---
title: xlite_graph_config
---

# `xlite_graph_config`

> Xlite 图模式配置。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |

## 说明

Xlite 图模式的参数入口，控制模型在 Xlite 图执行路径下的行为。属于进阶优化项，一般在与官方调优指南对应的场景下使用。

具体子字段以对应版本的官方文档为准。

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 双端 |

官方 graph_mode 指南：默认（full_mode=false）token 预算按 decode 步 sizing，prefill 与大批次回退 ACLGraph——偏 D 侧重 decode；full_mode=true 时预算按 max_num_batched_tokens，prefill/decode 都走 xlite（建议 --enforce-eager）。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/graph_mode.html)
<!-- DEPLOY_END -->
