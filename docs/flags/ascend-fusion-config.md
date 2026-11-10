---
title: ascend_fusion_config
---

# `ascend_fusion_config`

> Ascend 融合算子配置，控制是否使用 GmmSwigluQuant 融合算子。
> 📚 所属专题：[4. 图与编译](../feature-topics.md#t-graph)

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |
| 适用 | 全部 |

## 用法

```bash
vllm serve <model> \
  --additional-config='{"ascend_fusion_config": {"fusion_ops_gmmswigluquant": true}}'
```

## 子键

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `fusion_ops_gmmswigluquant` | `bool` | `true` | 是否启用 GmmSwigluQuant 融合算子（量化权重下使用） |

## 注意事项

- pydantic `extra="forbid"`：写错子键名会直接启动报错，不会静默忽略。
- 对非量化模型该算子可能不生效，显式设为 `false` 可在调试时关闭融合路径。

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

- [`ascend_compilation_config`](ascend-compilation-config.md) — Ascend 编译配置
- [`combine_quant_mode`](combine-quant-mode.md) — Combine 通信量化模式（另一处融合算子开关）
