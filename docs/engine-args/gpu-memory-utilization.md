---
title: gpu-memory-utilization
---

# `--gpu-memory-utilization`

> 模型执行器可占用的设备显存比例（0–1）——**KV cache 池总容量的来源**。

| 属性 | 值 |
|---|---|
| 类型 | `float`（0–1） |
| 默认值 | `None` → 解析为 **1.0**（可扩展 KV cache）或 **0.92**（否则）（vLLM main 源码 `resolved_gpu_memory_utilization`） |
| 分类 | 调度与内存 |

## 官方定义

> The fraction of GPU memory to be used for the model executor, which can range from 0 to 1. For example, a value of 0.5 would imply 50% GPU memory utilization. This is a per-instance limit, and only applies to the current vLLM instance... On non-GPU installs, this value controls the corresponding device memory utilization.

（vLLM 源码：`CacheConfig.gpu_memory_utilization`，[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)）

两个要点：

1. **单实例限制**：只约束当前 vLLM 实例。同卡多实例部署时按各自比例分配，互不影响；
2. **NPU 同样生效**："On non-GPU installs, this value controls the corresponding device memory utilization"——Ascend NPU 上控制的就是 NPU 显存（HBM）。

## 机制详解

**默认值的精确语义**（[`resolved_gpu_memory_utilization`](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)，property）：

```
显式设置  → 用显式值
未设置    → enable_extensible_kv_cache ? 1.0 : DEFAULT_GPU_MEMORY_UTILIZATION(0.92)
```

即 main 分支上"不设"不等于一个固定数：启用可扩展 KV cache（按实测内存定池）时给 1.0，传统路径给 0.92（`DEFAULT_GPU_MEMORY_UTILIZATION` 常量）。

**显存都去哪了**：这个比例覆盖模型执行器的全部占用——模型权重、KV cache、激活。vLLM 启动时先加载权重并 profiling，**剩余部分划给 KV cache 池**。因此：

```
KV 池可用量 ≈ 设备总显存 × 本参数 − 模型权重 − 激活/工作区预留
```

权重越大（或量化后越小），同样的比例下 KV 池差异巨大——这就是为什么量化权重的官方教程敢把比例开到 0.9 甚至更高。

## 参数联动

**与有效并发的关系**（承接 [`--max-num-seqs`](max-num-seqs.md) 页的公式）：

```
实际并发 ≈ min(max_num_seqs, KV 池容量 ÷ 平均上下文长度)
                  ↑
        本参数决定这一项
```

想提高并发但 `max_num_seqs` 已到顶？只有两条路：调大本参数（池子更大），或缩小单请求占用（`max_model_len`、`kv-cache-dtype` 量化）。

**与抢占的关系**：池子被占满即触发 preemption（`vllm:num_preemptions` 上升）。池子大小的第一旋钮就是它——但注意别顶到 1.0 导致运行时 OOM：非可扩展 KV 路径的默认 0.92 就是给运行时波动留的余量。

**更精细的替代**：若不想按比例、想按字节精确控制 KV cache，用 `kv_cache_memory_bytes`（比比例更精细的硬上限）。

## 调优思路

| 场景 | 建议 |
|---|---|
| 独占单卡生产部署 | 0.85–0.90 起步（官方教程实测区间），观察无 OOM 后再微调 |
| 同卡多实例 | 各实例按比例瓜分，总和 ≤ 1 减去系统预留 |
| 权重已量化 | 权重占比小，可适当上调给 KV 池腾地方 |
| OOM/启动 profiling 失败 | 先降本参数；或换量化权重、缩小 `max_model_len` |

## Ascend 语境与官方用法

- 官方教程几乎全部显式设置，实测范围 **0.80–0.90**：
  - 0.80：[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)
  - 0.85：[GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html)、[Qwen3.5-27B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html)
  - 0.90：大量 A2/A3 教程（如 [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html)）
- Ascend 量化模型（W8A8 等）权重占比小，是官方教程敢用 0.9 的原因之一——但具体以启动 profiling 输出为准。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --gpu-memory-utilization 0.9
```

## 相关参数

- [`--kv-cache-memory-bytes`](index.md) — 按字节精确限制 KV cache
- [`--max-num-seqs`](max-num-seqs.md) — 并发上限，受本参数间接约束
- [`--kv-cache-dtype`](kv-cache-dtype.md) — KV 量化，等效扩大池容量
