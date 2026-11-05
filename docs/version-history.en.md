---
title: Version History
---

# Version History

Tracks flag introductions, default changes, deprecations and removals. The per-flag data lives in `data/flags/*.yaml` (`status` / `version_support` / `version_note`); this page summarizes version-level events.

> Verified by diffing `vllm_ascend/envs.py` and `vllm_ascend/ascend_config.py` at each release tag. See the [version support matrix](version-matrix.md).

## v0.23.0 (earlier stable release)

- Many flags existed only as env vars or top-level keys (e.g. `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE`, `enable_flashcomm2_parallel_size`);
- The `scheduler_config` canonical nesting did not exist yet; scheduler flags were top-level keys or env vars.

## v0.30.0 (current stable release, biggest delta)

**14 flags added**:

- Scheduler family: `scheduler_config` (canonical nesting), `short_request_first_config`, `batch_job_sched_config`, `dyntra_lb_config`
- MoE communication: `mc2_comm_alg` (replaces `enable_mc2_hierarchy_comm`), `combine_quant_mode`
- RL: `rl_config`, rejection-sampling capabilities
- Others: `ascend_warmup_config`, `dynamic_spec_config`, `enable_force_eplb`, `enable_pcp_o_proj_weight_sharding`, `enable_pcp_embedding_lmhead_weight_sharding`, `kv_pool_range_debug`, `mlapo_keep_prefill_weights`

**4 flags removed**:

| Removed flag | Note |
|---|---|
| `enable_matmul_allreduce` | Env var only in v0.23.0; no direct replacement |
| `enable_flashcomm2_parallel_size` | FlashComm2 config; no direct replacement |
| `multistream_overlap_gate` | Gate multi-stream overlap; see `multistream_overlap_shared_expert` for shared-expert overlap |
| `weight_prefetch_config` | Weight prefetch; see `ascend_warmup_config` |

**Superseded**:

- `enable_context_parallel` (env var up to v0.18) → `enable_dsa_cp` / PCP.

## main (development branch, next release)

- Adds Runtime Guard boot config: `runtime_config`, `runtime_config_path`, `runtime_config_hot_reload`;
- Env-var cleanup continues: PR #9064 transition env vars are largely gone from `envs.py` on main (see the [version support matrix](version-matrix.md)).

## Historical events

| Date | Event |
|---|---|
| 2026-05 | [PR #9064](https://github.com/vllm-project/vllm-ascend/pull/9064) started migrating 10+ env vars to `--additional-config` (dual support during transition) |
| After | `scheduler_config` became the canonical nesting for scheduler options; `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` migrated to `kv_pool_range_debug` |
| Planned | Per [issue #10381](https://github.com/vllm-project/vllm-ascend/issues/10381), transition env vars will be fully removed (largely done on main) |

## How to update this page

1. Update `status` / `version_support` / `version_note` in `data/flags/<key>.yaml`;
2. Add a version-level row above with a source (tag diff or PR number);
3. If a default or semantics changed, add a "Change history" section to the flag's detail page.
