---
title: additional-config
---

# `--additional-config`

> Platform extension config (JSON dict) — **the sole entry point for all 63 vLLM-Ascend feature flags**: the reason this handbook exists.

| Property | Value |
|---|---|
| Type | `dict` |
| Default | `{}` |
| Category | Server |

## Official definition

> Additional config for specified platform. Different platforms may support different configs. Make sure the configs are valid for the platform you are using. Contents must be hashable.

(vLLM source: `VllmConfig.additional_config`, `Field(default_factory=dict)`, [config/vllm.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/vllm.py))

## How it works

**Layered design**: the vLLM core CLI only has engine-generic args; platform-specific configs (CUDA/ROCm/NPU) go through this pass-through channel — vLLM does not parse the contents; the platform plugin validates and consumes them. The vLLM-Ascend plugin consumes **all 63 feature flags** here (MoE fusion, RL mode, scheduler extensions, Runtime Guard, etc.).

**Where the keys come from**: valid keys are defined in vllm-ascend source (`vllm_ascend/ascend_config.py` and `vllm_ascend/envs.py`) and verified key-by-key on this site — **anything without a provenance is not listed** (see the [feature flags overview](../flags/index.md)).

**Mind the "hashable" constraint** (source docstring): contents must be hashable (they participate in the config cache key) — use primitive/immutable JSON values.

**Migration background**: since PR #9064, vLLM-Ascend env-var switches migrated to `--additional-config`; both work during the transition, and env vars will be removed in a future release. See the [migration table](../migration.md).

## Usage patterns

```bash
# single key
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_fused_mc2": 1}'

# combined (the norm in official tutorials)
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_cpu_binding":true,"enable_flashcomm1":true}'

# nested (compilation config)
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"ascend_compilation_config":{"enable_npugraph_ex":true,"enable_static_kernel":false}}'
```

## Parameter interplay

| Related arg | Relationship |
|---|---|
| The 63 feature flags | all passed through this arg — see the [feature flags overview](../flags/index.md) |
| [`--compilation-config`](compilation-config.md) | the vLLM-layer graph config; Ascend-layer `ascend_compilation_config` goes through this arg — see that page for the split |
| [`--enforce-eager`](enforce-eager.md) | one of the inputs to the platform-layer graph-mode arbitration |
| [`--quantization`](quantization.md) | layout switches like `weight_nz_mode` go through this arg |

## Ascend context

- Nearly every official `vllm serve` command carries this arg; frequent combinations:
  - `{"ascend_compilation_config": {...}}` (Qwen3 family)
  - `{"enable_cpu_binding": true, "enable_flashcomm1": true}` ([Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html))
- Defaults, status, version support, and risk notes for every flag: [feature flags overview](../flags/index.md); detail pages interlink for navigation.

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config '{"enable_fused_mc2": 1, "weight_nz_mode": 1}'
```

## Related

- [Feature flags overview](../flags/index.md) — deep reference for the 63 flags (defaults/versions/risks)
- [Migration table](../migration.md) — env var → additional-config migration
- [Version support matrix](../version-matrix.md) — per-flag support on v0.23.0 / v0.30.0 / main
