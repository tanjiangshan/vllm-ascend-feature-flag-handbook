---
title: enable_shared_expert_dp
---

# `enable_shared_expert_dp`

> 共享专家权重在 TP rank 间复制、以数据并行方式运行。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 适用 | 含共享专家的 MoE 模型 |

## 作用

启用后，共享专家（shared expert）权重会在各 TP rank 上复制一份，并以数据并行（DP）方式执行，避免共享专家计算成为 TP 通信的串行瓶颈。

- **收益**：共享专家计算吞吐提升；
- **代价**：每 rank 多存一份共享专家权重，**显存消耗增加**；
- 与上游 vLLM 的 MoE 序列并行**相互独立**：两者可单独启用，也可同时启用。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_shared_expert_dp": true}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 双端 |

官方 PD 配方 P/D 两侧均出现；DeepSeek-V4-Pro 说明其作用为把 shared experts 放到 DP ranks。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)
<!-- DEPLOY_END -->

## 相关开关

- [multistream_overlap_shared_expert](multistream-overlap-shared-expert.md) — 共享专家多流重叠
- [multistream_overlap_gate](multistream-overlap-gate.md) — 门控多流重叠
- [dynamic_eplb](dynamic-eplb.md) — 专家负载均衡
