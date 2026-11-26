---
title: async-scheduling
---

# `--async-scheduling`

> 异步调度：把下一步的 CPU 调度与输出处理，和当前步的 GPU 执行重叠，消除"GPU 等 CPU"的空泡。

| 属性 | 值 |
|---|---|
| 类型 | `bool`（`--async-scheduling` / `--no-async-scheduling`） |
| 默认值 | `None`（自动） |
| 分类 | 调度与内存 |

## 官方定义

> If set to False, disable async scheduling. Async scheduling helps to avoid gaps in GPU utilization, leading to better latency and throughput.

（vLLM 源码：`SchedulerConfig.async_scheduling`，[scheduler.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）

## 机制详解

**解决什么问题**：同步调度下每步是串行的——GPU 算完 → 结果回传 → CPU 处理输出、调度器选下一批 → 再启动下一步。这段主机工作期间 GPU 空转，batch 越小（decode 步）空泡占比越高。异步调度让 `AsyncScheduler` 提前把下一（几）步的调度决策与输入准备好，与当前步的 GPU 计算并行。

**在途步深**：`--async-scheduling-depth`（默认 `2`，最小 `2`）控制同时在途的步数——GPU 上 1 步 + 提前调度 `depth-1` 步；默认 2 即重叠 1 步的主机工作。主机往返比 GPU 单步更慢时（跨节点低并发 decode、投机解码）才需要加深；未开启异步调度时该值被忽略。

**默认 `None` 的自动解析**（vLLM `VllmConfig` 后处理）：

| 条件 | 结果 |
|---|---|
| 普通模型 + executor 支持 + 非 ROCm DeepEP HT DBO | 自动开启 |
| pooling 模型（embedding/rerank） | 自动关闭（当前实现会拖慢 pooling） |
| 分布式 executor 后端不支持 | 自动关闭 + 警告 |
| ROCm DeepEP high-throughput DBO | 自动关闭（该组合可能破坏 DP+EP 生成精度） |

显式传 `--async-scheduling` 时，遇到上述不兼容组合会**启动直接报错**（hard fail），而不是静默降级——这正是官方教程普遍显式写它的原因之一：把风险暴露在启动期。

**附带效果**：异步调度开启且 DP>1、模型为 MoE 时，vLLM 自动设置 `disable_nccl_for_dp_synchronization=True`（DP 同步改走 CPU group）。

## 参数联动

- `--async-scheduling-depth`：在途步数，默认 2；仅异步调度开启时生效。
- `--max-num-seqs` / `--max-num-batched-tokens`：决定每步批大小，直接影响主机调度耗时与重叠收益。
- `--speculative-config`：低并发 + 投机解码时主机往返占比高，是源码注释点名的"可加深步深"场景。

## 调优思路

| 场景 | 建议 |
|---|---|
| 默认部署 | 不传即可——`None` 自动开启；官方 PD 教程也普遍显式写 `--async-scheduling`（16 个教程页面、124 处） |
| 需要确定性对比 / 排查调度器问题 | `--no-async-scheduling` 做基线 |
| 跨节点低并发 decode、投机解码 | 默认步深不够时再调 `--async-scheduling-depth` |
| pooling / rerank 模型 | 保持自动关闭，不要显式开启 |

## Ascend 语境与官方用法

- 官方 Ascend 教程高频出现：Qwen3.8-Flash-Next、Qwen3.5-397B-A17B、GLM5/5.2/5.3、MiniMax-M3、DeepSeek-V4 系、Hy4 等（16 页 124 处），PD 分离 P/D 两侧配方均见。
- 常与 `--max-num-seqs`、`--max-num-batched-tokens`、`--no-disable-hybrid-kv-cache-manager`、`--model-loader-extra-config '{"enable_multithread_load":true,...}'` 同现。

## 用法

```bash
vllm serve <model> --async-scheduling
# 关闭（排查/基线对比）
vllm serve <model> --no-async-scheduling
```

## 相关参数

- [`--speculative-config`](speculative-config.md) — 低并发投机场景的主机往返
- [`--max-num-seqs`](max-num-seqs.md) — 每步批大小
- 相关专题：[负载均衡与调度](../feature-topics.md#t-scheduling)
