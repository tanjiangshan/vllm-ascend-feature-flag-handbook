---
title: enforce-eager
---

# `--enforce-eager`

> Force eager execution: skip torch.compile and CUDA Graph capture.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `False` |
| Category | Compilation & Graphs |

## Official definition

Always use eager-mode PyTorch. If False, will use torch.compile and use fast CUDA Graphs when possible. (vLLM source: `ModelConfig.enforce_eager`)

## Ascend context & official usage

- Official tutorials enable it explicitly in two scenarios:
  1. **First deployment / debugging** — rule out graph-capture factors when investigating accuracy or startup hangs;
  2. **Tight HBM on huge models** — e.g. [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) passes `--enforce-eager` to leave memory for weights and KV.
- For production, keep it **off** (default False) to get graph-capture performance.
- Ascend interplay: vllm-ascend `platform.py` derives the graph mode from this flag together with `ascend_compilation_config` (`get_compilation_mode`); `xlite_graph_config` is a separate graph path.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enforce-eager   # debugging
```

## Related args

- [`--compilation-config`](compilation-config.md) — graph capture policy
- [`ascend_compilation_config`](../flags/ascend-compilation-config.md) / [`xlite_graph_config`](../flags/xlite-graph-config.md) — Ascend-side graph configs
