---
title: Quick Start
---

# Quick Start: `--additional-config`

vLLM-Ascend feature flags are passed through vLLM's `--additional-config` argument as a JSON object.

!!! warning "Transition period"
    Since PR #9064, environment variables are migrating to `--additional-config`. Both work during the transition, but **use `--additional-config` for new deployments** — env vars will be removed in a future release. See the [migration table](migration.md).

## Online serving (`vllm serve`)

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_fused_mc2": 1, "weight_nz_mode": 2}'
```

## Offline inference (Python API)

```python
from vllm import LLM

llm = LLM(
    model="Qwen/Qwen3-8B",
    additional_config={
        "enable_fused_mc2": 1,
        "weight_nz_mode": 2,
    },
)
```

## Nested configs

Some flags are dict-typed, e.g. scheduler and EPLB configs:

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{
    "scheduler_config": {"enable_balance_scheduling": true},
    "eplb_config": {"dynamic_eplb": true}
  }'
```

!!! note "Dynamic EPLB requirement"
    Besides `eplb_config.dynamic_eplb: true`, the env var `DYNAMIC_EPLB=true` must also be set as a safety guard, or startup fails an assertion. See [`dynamic_eplb`](flags/dynamic-eplb.md).

## Common engine args: graph capture mode

`--additional-config` is the star of this handbook, but in real deployments it is most often paired with the vLLM engine arg `--compilation-config` for graph capture mode. The canonical recipe for a PD-disaggregated decode node:

```bash
vllm serve <model> \
  --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'
```

- Semantics: full graphs for decode batches only; prefill and mixed batches run ungraphed — protects TPOT on the D node. This is the mainstream recipe in official PD tutorials.
- Upstream default when unset: `FULL_AND_PIECEWISE` — full graphs for decode, piecewise graphs for prefill and mixed batches.
- Deep dive: [`--compilation-config` detail page](engine-args/compilation-config.md) (values, default resolution, auto capture sizes, official recipe index).

## Common pitfalls

| Error | Cause | Fix |
|---|---|---|
| `must be either '0' or '1'` | A strict-binary flag received an unexpected string | Use JSON `true`/`false` for bool flags |
| Flag has no effect | Misspelled key or wrong nesting | Check the key and nesting against the [overview](flags/index.md) |
| Startup config conflict | Mutually exclusive flags both set (e.g. `enable_force_eplb` + `eplb_config.dynamic_eplb`) | See the `conflicts` field on each detail page |
| `enable_flashcomm1` errors on MRv2 | FlashComm1 only supports Model Runner V1 | Use PCP on MRv2; see version notes |

## Next steps

- [Feature flags overview](flags/index.md): the full quick-reference table
- [Engine args overview](engine-args/index.md): top-level vLLM engine args (incl. `--compilation-config`)
- [Migration table](migration.md): env var → config key mapping
- [Environment variables](env-vars.md): standalone env vars that remain active
