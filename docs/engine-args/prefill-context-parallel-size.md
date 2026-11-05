---
title: prefill-context-parallel-size
---

# `--prefill-context-parallel-size`

> Prefill 上下文并行（PCP）：把长请求的 prefill token 切到多卡并行计算，降低 TTFT。

| 属性 | 值 |
|---|---|
| 类型 | `int` |
| 默认值 | `1` |
| 分类 | 并行策略 |

## 官方定义

Number of groups to split prefill context into... 长 prefill 请求跨 rank 切分，各 rank 计算序列的不同部分。详见 vLLM [Context Parallel Deployment](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/)。

## Ascend 语境与官方用法

- **PCP 在 vLLM-Ascend 上为 experimental**（[官方上下文并行指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)），官方兼容性矩阵：
  - MLA / GQA 后端均支持基本 PCP；
  - 前缀缓存、分块 prefill、PD 分离（MooncakeConnectorV1/V2）全兼容；
  - 图模式部分兼容（FULL 模式不支持）、投机解码部分兼容（MLA 仅 MTP / GQA 仅 Eagle3）。
- 官方教程取值 **1 / 2 / 8**，常与 `--decode-context-parallel-size` 叠加（A2/A3 MLA 全兼容）。
- 与序列并行（SP）组合时即为 **DSA-PCP** 方案（MRv2 推荐路径，替代旧 `enable_context_parallel`）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --prefill-context-parallel-size 2 --tensor-parallel-size 4
```

## 相关参数

- [`--decode-context-parallel-size`](index.md) — decode 阶段 KV 分片
- [`--cp-kv-cache-interleave-size`](index.md) — CP 的 KV 交错粒度
- [`--tensor-parallel-size`](tensor-parallel-size.md)
