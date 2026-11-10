---
title: mlapo_keep_prefill_weights
---

# `mlapo_keep_prefill_weights`

> MLAPO 场景下，D 节点是否保留 prefill 权重。
> 📚 所属专题：[5. PD 分离与并行](../feature-topics.md#t-pd)

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（v0.30.0 新增） |
| 依赖 | [`enable_mlapo`](enable-mlapo.md) |

## 背景

MLAPO 默认在 kv_consumer（仅 decode 的 D 节点）上释放 prefill 权重以节省显存。但 D 节点存在正常的本地 prefill 路径（recompute / fallback / preempt），**权重释放后这些路径会崩溃**（[issue #11882](https://github.com/vllm-project/vllm-ascend/issues/11882)）。

## 作用

启用后，D 节点保留 prefill 权重在 NPU 上：

- **收益**：本地 prefill 路径稳定，不会崩溃；
- **代价**：D 节点显存占用增加。

## 使用建议

PD 分离 + MLAPO 部署，且 D 节点观察到过 prefill fallback / preempt 时，**建议开启**。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_mlapo": true, "mlapo_keep_prefill_weights": true}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | — 不适用 |
| PD 分离 | ✅ D 节点 |

官方配置文档：在 kv_consumer（decode-only D）节点上保留 MLAPO prefill 权重——D 节点的本地 prefill 路径（recompute/fallback/preempt）在权重释放后会崩溃（issue #11882）；以显存换稳定。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)
<!-- DEPLOY_END -->

## 相关开关

- [enable_mlapo](enable-mlapo.md) — MLAPO 总开关
- [recompute_scheduler_enable](recompute-scheduler-enable.md) — D 节点重计算调度
