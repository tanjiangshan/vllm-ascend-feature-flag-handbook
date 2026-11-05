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

Splits prefill tokens of a long request across additional ranks; each rank computes a different part of the sequence. See vLLM [Context Parallel Deployment](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/).

## Ascend context & official usage

- **PCP is experimental on vLLM-Ascend** ([official context parallel guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/context_parallel.html)). Compatibility matrix:
  - MLA / GQA backends both support basic PCP;
  - Prefix caching, chunked prefill, PD disaggregation (MooncakeConnectorV1/V2) fully compatible;
  - Graph mode partially compatible (FULL mode unsupported); speculative decoding partially compatible (MLA: MTP only; GQA: Eagle3 only).
- Tutorial values: **1 / 2 / 8**, often stacked with `--decode-context-parallel-size` (A2/A3 MLA fully compatible).
- Combined with sequence parallelism (SP) it becomes the **DSA-PCP** scheme (recommended path on MRv2, replacing legacy `enable_context_parallel`).

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --prefill-context-parallel-size 2 --tensor-parallel-size 4
```

## Related args

- [`--decode-context-parallel-size`](index.md)
- [`--cp-kv-cache-interleave-size`](index.md)
- [`--tensor-parallel-size`](tensor-parallel-size.md)
