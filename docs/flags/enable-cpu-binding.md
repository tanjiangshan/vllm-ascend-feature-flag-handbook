---
title: enable_cpu_binding
---

# `enable_cpu_binding`

> ARM 服务器上的昇腾原生 CPU 绑定。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `true` |
| 状态 | ✅ active |
| 适用 | ARM 架构服务器 |

## 说明

默认开启。在 ARM 服务器上将 vLLM 工作线程绑定到昇腾 NPU 就近的 CPU 核，减少跨 NUMA 访问，提升 host 侧算子调度性能。

如遇 CPU 亲和性相关的调度问题（如与外部进程管理器冲突），可显式关闭排查：

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_cpu_binding": false}'
```

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ✅ 可开 |
| PD 分离 | ✅ 双端 |

官方 PD 分离教程 P/D 两侧普遍开启（Qwen3.8-Flash-Next、MiniMax-M3、GLM5.2 等配方）。

[出处](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.8-Flash-Next.html)
<!-- DEPLOY_END -->
