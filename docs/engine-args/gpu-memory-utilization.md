---
title: gpu-memory-utilization
---

# `--gpu-memory-utilization`

> 模型执行器可占用的设备显存比例（0–1），NPU 上同样生效。

| 属性 | 值 |
|---|---|
| 类型 | `float` |
| 默认值 | `None` → 解析为 **1.0**（可扩展 KV cache）或 **0.92**（否则）（vLLM main 源码 `resolved_gpu_memory_utilization`） |
| 分类 | 调度与内存 |

## 官方定义

The fraction of GPU memory to be used for the model executor... On non-GPU installs, this value controls the corresponding device memory utilization.（vLLM 源码 `CacheConfig`）

## Ascend 语境与官方用法

- 官方教程几乎全部显式设置，实测范围 **0.80–0.90**：
  - 0.80：[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)
  - 0.85：[GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html)、[Qwen3.5-27B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html)
  - 0.90：大量 A2/A3 教程
- 这是 **单实例** 限制；同卡多实例部署时按比例分配。
- KV cache 可用量 ≈ 总显存 × 该值 − 权重 − 激活，直接决定最大并发和上下文长度。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --gpu-memory-utilization 0.9
```

## 相关参数

- [`--kv-cache-memory-bytes`](index.md) — 按字节直接限制 KV cache
- [`--max-num-seqs`](max-num-seqs.md) — 并发上限受此值间接约束
