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
| `HCCL_SO_PATH` | path | unset (`libhccl.so`) | HCCL library path used by the pyhccl communicator backend. Only needed when explicitly using the pyhccl backend |

## Deployment form

> Colocated = PD on the same instance or multiple instances sharing NPUs; PD-disaggregated = P/D nodes split via KV transfer. None of the three runtime env vars has **documented deployment-form restrictions** — set them uniformly per node; "no official guidance" ≠ cannot enable.

| Env var | Colocated | PD-disaggregated |
|---|---|---|
| `VLLM_ASCEND_ENABLE_BATCH_MEMCPY` | no official guidance | no official guidance |
| `DYNAMIC_EPLB` | no official guidance | no official guidance |
| `EXPERT_MAP_RECORD` | no official guidance | no official guidance |

For per-flag deployment conclusions (with official sources), see the "部署形态" section of each [feature flag page](flags/index.md).

## Build-time environment variables

These affect **source builds** only, not runtime behavior. Full list: [official build docs](https://docs.vllm.ai/projects/ascend/en/latest/installation/ascend.html).

| Env var | Default | Description |
|---|---|---|
| `COMPILE_CUSTOM_KERNELS` | `1` | Whether to compile custom kernels. Set `0` when running unit tests without an NPU |
| `MAX_JOBS` | CPU core count | Build parallelism |
| `SOC_VERSION` | auto-detect | Chip version, auto-queried via `npu-smi` during build |
| `ASCEND_HOME_PATH` | `/usr/local/Ascend/ascend-toolkit/latest` | CANN toolkit path |
| `VERBOSE` | `"0"` | Verbose logs during compilation; set `1` for more build output |
| `CMAKE_BUILD_TYPE` | `Release` | CMake build type: `Release` / `Debug` / `RelWithDebugInfo` |
| `C_COMPILER` | system default | C compiler path (when building custom kernels from source) |
| `CXX_COMPILER` | system default | C++ compiler path (same as above) |
| `VLLM_VERSION` | unset | Version override for source-installed vLLM: a locally source-built vLLM often reports a version different from PyPI; set this so vllm-ascend's dependency resolution pins the correct one (developer scenario) |

## Recommendations

- **Prefer `--additional-config` for deployment**: except the "Runtime environment variables" above, new configs should use config keys. See [Quick start](quick-start.md).
- **Do not mix both forms for one flag**: when a flag is set both as an env var and as a config key, behavior follows the source implementation (config key usually wins), and mixing makes troubleshooting harder.
