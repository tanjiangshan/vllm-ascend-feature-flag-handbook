---
title: prefill-context-parallel-size
---

# `--prefill-context-parallel-size`

> Prefill Context Parallel (PCP): splits a long request's prefill tokens across ranks to cut TTFT.

| Property | Value |
|---|---|
| Type | `int` |
| Default | `1` |
| Category | Parallelism |

## Official definition

> Prefill Context Parallel (PCP) splits the prefill tokens of a long prefill request across additional ranks. Each rank computes a different part of the sequence, reducing time to first token (TTFT).

(vLLM-Ascend [official context parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html); upstream concept: vLLM [Context Parallel Deployment](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/))

## How it works

**Difference from TP**: TP slices "each layer's matrices" (every token passes through a slice on every device); PCP slices "one sequence" (different devices compute different **segments** of the same sequence, with cross-device exchange at attention layers). TP reduces per-layer compute; PCP reduces the **latency** of a single prefill — a long request that one device would compute serially is now split N-ways.

**Division of labor with DCP**: PCP accelerates prefill; `--decode-context-parallel-size` (DCP) shards KV by decode groups, reducing duplicate KV storage and lifting decode throughput. The two can stack and share the same devices.

**Current status**: **PCP is experimental on vLLM-Ascend** (the official guide's own words).

## Parameter interplay

**Official compatibility matrix** ([Ascend context parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html); A2/A3 MLA fully compatible):

| Combination | Compatibility |
|---|---|
| Basic PCP on MLA / GQA | ✅ |
| Prefix caching / chunked prefill / PD disaggregation (MooncakeConnectorV1/V2) + PCP | ✅ fully compatible |
| Graph mode + PCP | Partial (FULL mode unsupported) |
| Speculative decoding + PCP | Partial: MLA → MTP only, GQA → Eagle3 only |
| Sequence parallelism (SP) + PCP | ✅ (this is DSA-PCP, the MRv2-recommended path) |

**Source hard constraint** (DCP side, [model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)):

```
DCP > 1 on a non-MLA (GQA/MQA) model: tensor_parallel_size must exceed the total KV head count,
dcp_size ≤ TP // num_kv_heads, and Q-heads-per-KV-head % dcp_size == 0
```

**Expert sharding**: PCP is the second factor of the MoE expert sharding product TP × **PCP** × DP — enabling PCP also changes per-rank expert counts.

## Ascend context & official usage

- Tutorial values: **1 / 2 / 8**, often stacked with `--decode-context-parallel-size`.
- **DSA-PCP** (PCP + sequence parallelism) is the recommended long-context path on Ascend MRv2, replacing the legacy env-var switch `enable_context_parallel`.
- While experimental, re-verify the compatibility table after each vllm-ascend upgrade.

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --prefill-context-parallel-size 2 --tensor-parallel-size 4
```

## Related args

- [`--decode-context-parallel-size`](index.md) — decode-phase KV sharding
- [`--cp-kv-cache-interleave-size`](index.md) — KV interleave granularity in CP
- [`--tensor-parallel-size`](tensor-parallel-size.md) — upper bound for DCP
- [`--data-parallel-size`](data-parallel-size.md) — the third expert-sharding factor
