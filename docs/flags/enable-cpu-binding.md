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
