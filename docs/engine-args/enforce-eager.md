---
title: enforce-eager
---

# `--enforce-eager`

> 强制 eager 执行模式：跳过 torch.compile 与 CUDA Graph 捕获。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `False` |
| 分类 | 编译与图 |

## 官方定义

Always use eager-mode PyTorch. If False, will use torch.compile and use fast CUDA Graphs when possible.（vLLM 源码 `ModelConfig.enforce_eager`）

## Ascend 语境与官方用法

- 官方教程中两种场景会显式开启：
  1. **首部署/调试**（排查精度、启动卡住等问题时排除图捕获因素）；
  2. **超大模型显存紧张**（如 [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) 显式 `--enforce-eager`，把显存留给权重与 KV）。
- 生产环境建议**关闭**（默认 False）以获得图捕获性能。
- Ascend 侧联动：vllm-ascend `platform.py` 会根据本参数与 `ascend_compilation_config` 共同决定图模式（`get_compilation_mode`）；`xlite_graph_config` 是另一条图路径。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --enforce-eager   # 调试用
```

## 相关参数

- [`--compilation-config`](compilation-config.md) — 图捕获策略
- [`ascend_compilation_config`](../flags/ascend-compilation-config.md) / [`xlite_graph_config`](../flags/xlite-graph-config.md) — Ascend 侧图配置
