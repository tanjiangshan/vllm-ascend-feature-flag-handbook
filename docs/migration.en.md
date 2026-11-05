---
title: Environment Variable Migration Table
---

# Environment Variables → `--additional-config` Migration Table

Since [PR #9064](https://github.com/vllm-project/vllm-ascend/pull/9064) (2026-05), vLLM-Ascend is migrating environment variables to `--additional-config`.

- **Now**: both env vars and `--additional-config` are supported during the transition;
- **Recommendation**: use `--additional-config` for new deployments and migrate existing configs;
- **Future**: env vars will be removed in a future release (tracking: [issue #10381](https://github.com/vllm-project/vllm-ascend/issues/10381)).

## Quick reference

| Env var | Config key | Type conversion |
|---|---|---|
| `VLLM_ASCEND_BALANCE_SCHEDULING` | `scheduler_config.enable_balance_scheduling` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_ENABLE_FLASHCOMM1` | `enable_flashcomm1` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` | `enable_matmul_allreduce` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` | `enable_flashcomm2_parallel_size` | integer (unchanged) |
| `MSMONITOR_USE_DAEMON` | `msmonitor_use_daemon` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_ENABLE_MLAPO` | `enable_mlapo` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_ENABLE_NZ` | `weight_nz_mode` | integer (unchanged, **key renamed**) |
| `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` | `enable_context_parallel` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_ENABLE_FUSED_MC2` | `enable_fused_mc2` | integer (unchanged) |
| `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` | `enable_transpose_kv_cache_by_block` | `"1"` → `true`, `"0"` → `false` |
| `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` | `kvpool_range_debug` | `"1"` → `true`, `"0"` → `false` |

## Example

**Before (env var):**

```bash
export VLLM_ASCEND_ENABLE_MLAPO=1
vllm serve Qwen/Qwen3-8B
```

**After (`--additional-config`):**

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_mlapo": true}'
```

**Nested key migration (balance scheduling):**

```bash
# Before
export VLLM_ASCEND_BALANCE_SCHEDULING=1

# After
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"enable_balance_scheduling": true}}'
```

## Notes

1. **`weight_nz_mode` was renamed**: the old env var is `VLLM_ASCEND_ENABLE_NZ`; the new key is `weight_nz_mode`, and its semantics expanded from on/off to a three-mode switch (see [`weight_nz_mode`](flags/weight-nz-mode.md)).
2. **Mind the nesting**: keys like `enable_balance_scheduling` and `recompute_scheduler_enable` now live under `scheduler_config`.
3. **Precedence**: if the same field is provided in both formats during the transition, the value inside `scheduler_config` wins.
4. **Legacy top-level keys still parse**: `enable_balance_scheduling`, `recompute_scheduler_enable`, `short_request_first_config` and `profiling_chunk_config` remain accepted as top-level keys, but are all deprecated.
5. **Some migration targets were later removed**: `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE`, `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` and others were removed in v0.30.0 shortly after migration — check the [version support matrix](version-matrix.md) before upgrading.
