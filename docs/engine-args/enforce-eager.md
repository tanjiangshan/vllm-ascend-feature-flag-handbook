---
title: enforce-eager
---

# `--enforce-eager`

> 强制 eager 执行：跳过 torch.compile 与 CUDA Graph 捕获——用性能换确定性的排障手段。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `False` |
| 分类 | 编译与图 |

## 官方定义

> Always use eager-mode PyTorch. If False, will use torch.compile and use fast CUDA Graphs when possible.

（vLLM 源码：`ModelConfig.enforce_eager`，[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）

## 机制详解

**图捕获为什么快**：vLLM 生产路径会把模型计算编译/捕获成 CUDA Graph——相同形状的 kernel 序列整图重放，省去每步的 CPU 调度开销和 kernel launch 开销。decode 步尤其受益（每步计算量小，调度占比高）。

**eager 模式放弃什么**：每次前向都走 PyTorch 动态调度。好处是行为完全透明、出错可直接定位；代价是 TPOT 明显变差（官方教程中 eager 模式通常配合降并发使用）。

**什么时候该开**：它不是性能参数，是**排障与救急开关**：

1. **首部署调试**——精度异常、输出乱码、启动卡住时，用它排除图捕获/编译因素，缩小排查面；
2. **显存救急**——图捕获本身占显存，超大模型权重紧张时用它把显存让给权重和 KV；
3. **特性组合不支持图**时兜底（配合具体特性文档判断）。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--compilation-config`](compilation-config.md) | 本参数是图策略的"总开关反面"：eager 开 = 一切图配置失效 |
| Ascend [`ascend_compilation_config`](../flags/ascend-compilation-config.md) | vllm-ascend `platform.py` 按本参数 + 该开关共同决定图模式（`get_compilation_mode`） |
| Ascend [`xlite_graph_config`](../flags/xlite-graph-config.md) | Ascend 另一条图路径，与本参数互斥判断 |
| [`--speculative-config`](speculative-config.md) | 草稿侧常用 `enforce_eager:true`（官方 Kimi-K3 配方），避免给草稿模型做图捕获 |

**类比**：图捕获像"把整条流水线录成回放带"——回放快但录带要空间、且中途改工序就得重录；eager 是"每步现场操作"，慢但什么都能看。

## Ascend 语境与官方用法

- 官方教程两种场景显式开启：
  1. **调试**——排查精度/启动问题时；
  2. **超大模型显存紧张**——如 [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) 显式 `--enforce-eager`，把显存留给权重与 KV。
- **生产默认关闭**（False）以获得图捕获性能；开启前确认收益大于 TPOT 损失。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enforce-eager   # 调试用
```

## 相关参数

- [`--compilation-config`](compilation-config.md) — 图捕获策略（本参数开启后失效）
- [`ascend_compilation_config`](../flags/ascend-compilation-config.md) / [`xlite_graph_config`](../flags/xlite-graph-config.md) — Ascend 侧图配置
