---
title: Environment Variables
---

# Environment Variables

Besides the 10+ flags being migrated (see [migration table](migration.md)), the following environment variables remain **active standalone entry points** with no announced migration plan.

## Runtime environment variables

| Env var | Type | Default | Description |
|---|---|---|---|
| `VLLM_ASCEND_ENABLE_BATCH_MEMCPY` | `"1"` / `"0"` / unset | unset (auto) | Controls the `aclrtMemcpyBatchAsync` compile path for KV cache offloading. `"1"` force-enables, `"0"` force-disables, unset auto-detects from CANN headers. **Note**: no `--additional-config` key exists; env var only. |
| `DYNAMIC_EPLB` | `"true"` / `"false"` | `"false"` | Safety guard for dynamic EPLB. Only takes effect when `dynamic_eplb: true` (or record mode) is also set in config. See [`dynamic_eplb`](flags/dynamic-eplb.md) |
| `EXPERT_MAP_RECORD` | bool | unset | EPLB record mode: records the expert map and saves it to `expert_map_record_path` |

## Build-time environment variables

These affect **source builds** only, not runtime behavior. Full list: [official build docs](https://docs.vllm.ai/projects/ascend/en/latest/installation/ascend.html).

| Env var | Default | Description |
|---|---|---|
| `COMPILE_CUSTOM_KERNELS` | `1` | Whether to compile custom kernels. Set `0` when running unit tests without an NPU |
| `MAX_JOBS` | CPU core count | Build parallelism |
| `SOC_VERSION` | auto-detect | Chip version, auto-queried via `npu-smi` during build |
| `ASCEND_HOME_PATH` | `/usr/local/Ascend/ascend-toolkit/latest` | CANN toolkit path |

## Recommendations

- **Prefer `--additional-config` for deployment**: except the "Runtime environment variables" above, new configs should use config keys. See [Quick start](quick-start.md).
- **Do not mix both forms for one flag**: when a flag is set both as an env var and as a config key, behavior follows the source implementation (config key usually wins), and mixing makes troubleshooting harder.
