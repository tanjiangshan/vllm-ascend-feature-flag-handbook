---
title: enforce-eager
---

# `--enforce-eager`

> Force eager execution: skip torch.compile and CUDA Graph capture — trading performance for debuggability.

| Property | Value |
|---|---|
| Type | `bool` |
| Default | `False` |
| Category | Compilation & Graphs |

## Official definition

> Always use eager-mode PyTorch. If False, will use torch.compile and use fast CUDA Graphs when possible.

(vLLM source: `ModelConfig.enforce_eager`, [model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py))

## How it works

**Why graph capture is fast**: the production path compiles/captures model computation into CUDA Graphs — a fixed kernel sequence replayed whole, eliminating per-step CPU scheduling and kernel-launch overhead. Decode steps benefit most (small compute per step, high scheduling share).

**What eager gives up**: every forward goes through PyTorch dynamic dispatch. Behavior is fully transparent and errors directly traceable — at the cost of markedly worse TPOT (eager deployments typically pair with lower concurrency).

**When to enable it**: it is not a performance knob but a **debugging / emergency switch**:

1. **First-deployment debugging** — on accuracy anomalies, garbled outputs, or startup hangs, use it to rule out graph-capture/compile factors and narrow the search;
2. **Memory emergency** — capture itself consumes memory; on huge models, trade it for weight/KV headroom;
3. **Fallback** when a feature combination doesn't support graphs (judge per feature docs).

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--compilation-config`](compilation-config.md) | the "master-switch opposite": eager on = all graph config inert |
| Ascend [`ascend_compilation_config`](../flags/ascend-compilation-config.md) | vllm-ascend `platform.py` derives the graph mode from this arg plus that flag (`get_compilation_mode`) |
| Ascend [`xlite_graph_config`](../flags/xlite-graph-config.md) | the other Ascend graph path, mutually exclusive with eager |
| [`--speculative-config`](speculative-config.md) | draft side often uses `enforce_eager:true` (official Kimi-K3 recipe) to skip graph capture for the draft model |

**Analogy**: graph capture is "recording the whole assembly line on tape" — playback is fast, but recording takes space and any mid-process change requires a re-record; eager is "operating live every step" — slower, but everything is visible.

## Ascend context & official usage

- Two scenarios where official tutorials enable it explicitly:
  1. **Debugging** — accuracy/startup investigations;
  2. **Tight memory on huge models** — e.g. [Qwen3.5-397B-A17B](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html) passes `--enforce-eager` to leave memory for weights and KV.
- **Keep off in production** (default False) for graph-capture performance; before enabling, confirm the benefit outweighs the TPOT loss.

## Usage

```bash
vllm serve Qwen/Qwen3-8B --enforce-eager   # debugging
```

## Related args

- [`--compilation-config`](compilation-config.md) — graph capture policy (inert when this arg is on)
- [`ascend_compilation_config`](../flags/ascend-compilation-config.md) / [`xlite_graph_config`](../flags/xlite-graph-config.md) — Ascend-side graph configs
