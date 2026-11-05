---
title: 环境变量迁移对照表
---

# 环境变量 → `--additional-config` 迁移对照表

自 [PR #9064](https://github.com/vllm-project/vllm-ascend/pull/9064)（2026-05）起，vLLM-Ascend 将环境变量统一迁移至 `--additional-config`。

- **当前**：过渡期内环境变量与 `--additional-config` 均受支持；
- **建议**：新部署使用 `--additional-config`，并尽快迁移现有配置；
- **未来**：环境变量将在未来版本移除（移除计划见 [issue #10381](https://github.com/vllm-project/vllm-ascend/issues/10381)）。

## 迁移速查表

| 环境变量 | 配置键 | 类型转换 |
|---|---|---|
| `VLLM_ASCEND_BALANCE_SCHEDULING` | `scheduler_config.enable_balance_scheduling` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_ENABLE_FLASHCOMM1` | `enable_flashcomm1` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` | `enable_matmul_allreduce` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` | `enable_flashcomm2_parallel_size` | 整数（不变） |
| `MSMONITOR_USE_DAEMON` | `msmonitor_use_daemon` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_ENABLE_MLAPO` | `enable_mlapo` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_ENABLE_NZ` | `weight_nz_mode` | 整数（不变，**字段名已更改**） |
| `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` | `enable_context_parallel` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_ENABLE_FUSED_MC2` | `enable_fused_mc2` | 整数（不变） |
| `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` | `enable_transpose_kv_cache_by_block` | `"1"` → `true`，`"0"` → `false` |
| `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` | `kvpool_range_debug` | `"1"` → `true`，`"0"` → `false` |

## 迁移示例

**迁移前（环境变量）：**

```bash
export VLLM_ASCEND_ENABLE_MLAPO=1
vllm serve Qwen/Qwen3-8B
```

**迁移后（`--additional-config`）：**

```bash
vllm serve Qwen/Qwen3-8B --additional-config='{"enable_mlapo": true}'
```

**含嵌套键的迁移（以均衡调度为例）：**

```bash
# 迁移前
export VLLM_ASCEND_BALANCE_SCHEDULING=1

# 迁移后
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"scheduler_config": {"enable_balance_scheduling": true}}'
```

## 注意事项

1. **`weight_nz_mode` 字段名已更改**：旧环境变量名是 `VLLM_ASCEND_ENABLE_NZ`，新键名为 `weight_nz_mode`，且语义从"是否启用"扩展为三档模式（见 [`weight_nz_mode`](flags/weight-nz-mode.md)）。
2. **嵌套键注意层级**：`enable_balance_scheduling`、`recompute_scheduler_enable` 等迁移后位于 `scheduler_config` 之下。
3. **优先级**：过渡期若同一字段两种格式都提供，以 `scheduler_config` 中的值为准。
4. **迁移期顶部旧键仍可用**：`enable_balance_scheduling`、`recompute_scheduler_enable`、`short_request_first_config`、`profiling_chunk_config` 作为顶层键仍被兼容，但均已标记弃用。
5. **部分迁移目标键后来被移除**：`VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE`、`VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` 等迁移后不久即在 v0.30.0 移除，升级前请核对[版本支持矩阵](version-matrix.md)。
