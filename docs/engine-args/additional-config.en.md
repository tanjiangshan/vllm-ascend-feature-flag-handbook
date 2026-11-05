---
title: additional-config
---

# `--additional-config`

> Platform extension config (JSON dict). **The sole entry point for all 51 vLLM-Ascend feature flags.**

| Property | Value |
|---|---|
| Type | `dict` |
| Default | `{}` |
| Category | Server |

## Official definition

Additional config for specified platform. Different platforms may support different configs. Make sure the configs are valid for the platform you are using. (vLLM source: `VllmConfig.additional_config`, `Field(default_factory=dict)`)

## Ascend context

- This parameter is the reason this handbook exists: all 51 vLLM-Ascend feature flags (MoE fusion, RL mode, scheduler extensions, Runtime Guard, etc.) are passed through it.
- Full list with defaults, version support and detail pages: **[Feature flags overview](../flags/index.md)**.
- Nearly every official `vllm serve` command carries it, e.g.:
  - `{"ascend_compilation_config": {...}}` (Qwen3 family)
  - `{"enable_cpu_binding": true, "enable_flashcomm1": true}` ([Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html))

## Usage

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config '{"enable_fused_mc2": 1, "weight_nz_mode": 1}'
```

## Related

- [Feature flags overview](../flags/index.md) — deep reference for the 51 flags
- [Migration table](../migration.md) — env var → additional-config migration
