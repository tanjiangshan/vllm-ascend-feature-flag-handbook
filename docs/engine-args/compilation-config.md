---
title: compilation-config
---

# `--compilation-config`（`-cc`）

> torch.compile 与 CUDA Graph 捕获配置——生产性能的核心旋钮，控制"哪些步录图、录哪些尺寸"。

| 属性 | 值 |
|---|---|
| 类型 | `CompilationConfig`（JSON 或 `-cc.key=value` 点号覆盖） |
| 默认值 | `CompilationConfig()`（各子项自带默认值，如 `cudagraph_mode`） |
| 分类 | 编译与图 |

## 官方定义

> `torch.compile` and cudagraph capture configuration for the model. As a shorthand, one can append compilation arguments via `-cc.parameter=argument`.

（vLLM 源码：`EngineArgs.compilation_config`，[arg_utils.py](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py)）

## 机制详解

**它管什么**：两大子系统——torch.compile（把模型编译成更优的 kernel 序列）和 CUDA Graph（整图重放）。核心子项：

| 子项 | 作用 |
|---|---|
| `cudagraph_mode` | 录图范围，共 5 个取值（见下表） |
| `cudagraph_capture_sizes` | 显式枚举要捕获的 batch 尺寸列表 |
| `max_cudagraph_capture_size` | 捕获尺寸上界 |

`cudagraph_mode` 完整取值（vLLM 源码 [`CUDAGraphMode`](https://github.com/vllm-project/vllm/blob/main/vllm/config/compilation.py) 枚举）：

| 取值 | 语义 |
|---|---|
| `NONE` | 不录图（`--enforce-eager` 会强制落为此值） |
| `PIECEWISE` | 只录分段图，图不兼容算子（如部分 attention）留在图外 |
| `FULL` | 所有 batch 整图录制（部分后端不支持） |
| `FULL_DECODE_ONLY` | 仅 decode batch 录整图，prefill / 混合批不录 |
| `FULL_AND_PIECEWISE` | decode 录整图，prefill 与混合批录分段图——**v1 引擎默认值** |

**decode 步为什么最需要图**：每步只做一次前向（每序列 1 个 token），kernel launch 和 CPU 调度占比最高；录图后整步回放，TPOT 收益最大。prefill 步计算量大、形状多变，录图收益小还容易 miss——这是官方教程偏爱 `FULL_DECODE_ONLY` 的原因。

**两种传法**（源码 docstring 原文确认）：

```bash
--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'   # 整 JSON
-cc.cudagraph_mode=FULL_DECODE_ONLY                            # 点号简写
```

## 参数联动

**与 `--enforce-eager` 互斥**：eager 开 = 本参数全部失效（见 [`enforce-eager`](enforce-eager.md)）。

**与调度参数的捕获尺寸公式**（Ascend 细粒度 TP，[Fine_grained_TP 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/Fine_grained_TP.html)）：

```
最大捕获尺寸必须覆盖 min(max_num_batched_tokens, max_num_seqs × (1 + num_speculative_tokens))
```

否则 oproj/mlp 细粒度 TP 启动时自动禁用并告警。vLLM 侧 `max_cudagraph_capture_size` 也会被 Ascend 平台层按可用显存截断（vllm-ascend `platform.py`）。

**与投机解码的联动**：`num_speculative_tokens > 0` 时 decode 步的 token 数变成 `1 + n` 的倍数，捕获尺寸枚举需覆盖这些形状（同上公式）。

## 调优思路

| 场景 | 建议 |
|---|---|
| 生产默认（官方教程主流） | `{"cudagraph_mode":"FULL_DECODE_ONLY"}`——decode 录图、prefill 自由 |
| batch 形状固定 | 显式枚举 `cudagraph_capture_sizes`（官方 Qwen3-Dense 配方），省自动探测 |
| 显存紧张 | 缩小捕获尺寸枚举 / 降 `max_cudagraph_capture_size`；再不行上 `--enforce-eager` |

## Ascend 语境与官方用法

- 官方教程高频取值：
  - `--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'`（[Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)、DeepSeek-V4 系）
  - `--compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,...]}'`（Qwen3-Dense 等）
- 注意与 Ascend 侧图开关（[`ascend_compilation_config`](../flags/ascend-compilation-config.md) 的 `enable_npugraph_ex`、[`xlite_graph_config`](../flags/xlite-graph-config.md)）的层次：本参数是 vLLM 层，那些是 Ascend 平台层，最终图模式由 platform 代码裁决。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
# 或点号覆盖
vllm serve Qwen/Qwen3-8B -cc.cudagraph_mode=FULL_DECODE_ONLY
```

## 相关参数

- [`--enforce-eager`](enforce-eager.md) — 互斥的总开关
- [`--max-num-seqs`](max-num-seqs.md) — 捕获尺寸公式的输入
- [`--speculative-config`](speculative-config.md) — 影响 decode 步的形状
