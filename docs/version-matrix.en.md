---
title: Version Support Matrix
---

# Version Support Matrix

> This matrix is auto-generated from the `version_support` field in `data/flags/*.yaml` by `scripts/generate_tables.py`. Do not edit the table area by hand.

Shows whether each flag exists in three vLLM-Ascend versions:

| Column | Meaning |
|---|---|
| **v0.23.0** | An earlier stable release |
| **v0.30.0** | The current stable release (most additions) |
| **main** | Development branch, i.e. the next release (unpublished, subject to change) |

Legend: :white_check_mark: = supported; — = not present (never introduced, or already removed)

## How to read

- `v0.23.0 — / v0.30.0 ✅ / main ✅`: added in v0.30.0; deploying on an older release raises an unknown-config-key error;
- `v0.23.0 ✅ / v0.30.0 — / main —`: removed; the config stops working after upgrade (see the Note column for the replacement);
- All ✅: available everywhere, the common case.

<!-- MATRIX_START -->
| Config key | v0.23.0 | v0.30.0 | main | Note |
|---|---|---|---|---|
| [`ascend_compilation_config`](flags/ascend-compilation-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_fusion_config`](flags/ascend-fusion-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_log_path`](flags/ascend-log-path.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_warmup_config`](flags/ascend-warmup-config.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`batch_job_sched_config`](flags/batch-job-sched-config.md) | — | :white_check_mark: | :white_check_mark: | top-level key deprecated since v0.30.0 (still works with a warning); canonical form scheduler_config.batch_job_sched_config |
| [`c8_enable_reshape_optim`](flags/c8-enable-reshape-optim.md) | :white_check_mark: | — | — |  |
| [`combine_quant_mode`](flags/combine-quant-mode.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`draft_window_size`](flags/draft-window-size.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`dump_config`](flags/dump-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dump_config_path`](flags/dump-config-path.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dynamic_eplb`](flags/dynamic-eplb.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dynamic_spec_config`](flags/dynamic-spec-config.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`dyntra_lb_config`](flags/dyntra-lb-config.md) | — | :white_check_mark: | :white_check_mark: | top-level key no longer parsed since v0.30.0 (extra=forbid raises an unknown-key error); must use the nested form scheduler_config.dyntra_lb_config |
| [`enable_balance_scheduling`](flags/enable-balance-scheduling.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | top-level key deprecated |
| [`enable_context_parallel`](flags/enable-context-parallel.md) | — | — | — | Env var only up to v0.18; superseded by enable_dsa_cp |
| [`enable_cpu_binding`](flags/enable-cpu-binding.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_flashcomm1`](flags/enable-flashcomm1.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_flashcomm2_parallel_size`](flags/enable-flashcomm2-parallel-size.md) | :white_check_mark: | — | — | Config key + env fallback in v0.23.0; removed in v0.30.0 |
| [`enable_force_eplb`](flags/enable-force-eplb.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`enable_fused_mc2`](flags/enable-fused-mc2.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_kv_nz`](flags/enable-kv-nz.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_kvpp`](flags/enable-kvpp.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`enable_matmul_allreduce`](flags/enable-matmul-allreduce.md) | :white_check_mark: | — | — | Env var only in v0.23.0; removed in v0.30.0 |
| [`enable_mc2_hierarchy_comm`](flags/enable-mc2-hierarchy-comm.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_mlapo`](flags/enable-mlapo.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_pcp_embedding_lmhead_weight_sharding`](flags/enable-pcp-embedding-lmhead-weight-sharding.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`enable_pcp_o_proj_weight_sharding`](flags/enable-pcp-o-proj-weight-sharding.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`enable_prefill_mc2`](flags/enable-prefill-mc2.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_shared_expert_dp`](flags/enable-shared-expert-dp.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_sparse_li_c8`](flags/enable-sparse-li-c8.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_sparse_sfa_c8`](flags/enable-sparse-sfa-c8.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_transpose_kv_cache_by_block`](flags/enable-transpose-kv-cache-by-block.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`eplb_config`](flags/eplb-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`finegrained_tp_config`](flags/finegrained-tp-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`hamming_sparse`](flags/hamming-sparse.md) | :white_check_mark: | — | — |  |
| [`kv_pool_range_debug`](flags/kv-pool-range-debug.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`mc2_comm_alg`](flags/mc2-comm-alg.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`mega_moe_max_tokens`](flags/mega-moe-max-tokens.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`mix_placement`](flags/mix-placement.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`mlapo_keep_prefill_weights`](flags/mlapo-keep-prefill-weights.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`msmonitor_use_daemon`](flags/msmonitor-use-daemon.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`multistream_dsv4_dsa_overlap`](flags/multistream-dsv4-dsa-overlap.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`multistream_engram_overlap`](flags/multistream-engram-overlap.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`multistream_overlap_gate`](flags/multistream-overlap-gate.md) | :white_check_mark: | — | — | Removed since v0.30.0 |
| [`multistream_overlap_shared_expert`](flags/multistream-overlap-shared-expert.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`pa_shape_list`](flags/pa-shape-list.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`profiling_chunk_config`](flags/profiling-chunk-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | top-level key deprecated since v0.30.0 (still works with a warning); canonical form scheduler_config.profiling_chunk_config |
| [`recompute_scheduler_enable`](flags/recompute-scheduler-enable.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | top-level key deprecated since v0.30.0 (still works with a warning); canonical form scheduler_config.recompute_scheduler_enable |
| [`refresh`](flags/refresh.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`rejection_sampler_config`](flags/rejection-sampler-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`rl_config`](flags/rl-config.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`runtime_config`](flags/runtime-config.md) | — | — | :white_check_mark: | New on main; ships in the next release |
| [`runtime_config_hot_reload`](flags/runtime-config-hot-reload.md) | — | — | :white_check_mark: | New on main; ships in the next release |
| [`runtime_config_path`](flags/runtime-config-path.md) | — | — | :white_check_mark: | New on main; ships in the next release |
| [`runtime_dump_dir`](flags/runtime-dump-dir.md) | — | — | — | Part of Runtime Guard; new on main |
| [`runtime_report_dir`](flags/runtime-report-dir.md) | — | — | — | Part of Runtime Guard; new on main |
| [`scheduler_config`](flags/scheduler-config.md) | — | :white_check_mark: | :white_check_mark: | New in v0.30.0 |
| [`sfa_dcp_force_tmajor_restore`](flags/sfa-dcp-force-tmajor-restore.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`short_request_first_config`](flags/short-request-first-config.md) | — | :white_check_mark: | :white_check_mark: | top-level key deprecated since v0.30.0 (still works with a warning); canonical form scheduler_config.short_request_first_config |
| [`sparse_kv_offload_config`](flags/sparse-kv-offload-config.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`weight_nz_mode`](flags/weight-nz-mode.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`weight_prefetch_config`](flags/weight-prefetch-config.md) | :white_check_mark: | — | — | Removed since v0.30.0 |
| [`xlite_graph_config`](flags/xlite-graph-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
<!-- MATRIX_END -->

## How this data is verified

`version_support` is verified by diffing `vllm_ascend/envs.py` (env vars) and `vllm_ascend/ascend_config.py` (config keys) at each tag; flags that moved into sub-config classes are cross-checked against the official configuration docs. If you find a discrepancy, edit `data/flags/<key>.yaml` directly and open a PR.
