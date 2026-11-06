---
title: 版本支持矩阵
---

# 版本支持矩阵

> 本页矩阵由 `scripts/generate_tables.py` 从 `data/flags/*.yaml` 的 `version_support` 字段自动生成，请勿手改表格区域。

展示每个开关在三个 vLLM-Ascend 版本中的支持情况：

| 列 | 含义 |
|---|---|
| **v0.23.0** | 较早的稳定 release |
| **v0.30.0** | 当前的稳定 release（新增最多） |
| **main** | 开发分支，代表下一版本（未发布，随时可能变动） |

图例：:white_check_mark: = 该版本支持；— = 该版本不存在（未引入或已移除）

## 阅读示例

- `v0.23.0 — / v0.30.0 ✅ / main ✅`：v0.30.0 新增开关，用旧版本部署会报未知配置键；
- `v0.23.0 ✅ / v0.30.0 — / main —`：已被移除的开关，升级后原配置会失效（通常有替代开关，见备注）；
- 全 ✅：三个版本均可用，最常见。

<!-- MATRIX_START -->
| 配置键 | v0.23.0 | v0.30.0 | main | 备注 |
|---|---|---|---|---|
| [`ascend_compilation_config`](flags/ascend-compilation-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_fusion_config`](flags/ascend-fusion-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_log_path`](flags/ascend-log-path.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`ascend_warmup_config`](flags/ascend-warmup-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`batch_job_sched_config`](flags/batch-job-sched-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 起顶层键废弃（仍可用，发 deprecation 警告），规范写法 scheduler_config.batch_job_sched_config |
| [`c8_enable_reshape_optim`](flags/c8-enable-reshape-optim.md) | :white_check_mark: | — | — |  |
| [`combine_quant_mode`](flags/combine-quant-mode.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`draft_window_size`](flags/draft-window-size.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`dump_config`](flags/dump-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dump_config_path`](flags/dump-config-path.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dynamic_eplb`](flags/dynamic-eplb.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`dynamic_spec_config`](flags/dynamic-spec-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`dyntra_lb_config`](flags/dyntra-lb-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 起顶层键不再解析（extra=forbid 会报未知键错误），必须写 scheduler_config.dyntra_lb_config 嵌套形式 |
| [`enable_balance_scheduling`](flags/enable-balance-scheduling.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | 顶层键废弃 |
| [`enable_context_parallel`](flags/enable-context-parallel.md) | — | — | — | v0.18 及更早通过环境变量支持；后被 enable_dsa_cp 取代 |
| [`enable_cpu_binding`](flags/enable-cpu-binding.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_dsa_cp`](flags/enable-dsa-cp.md) | — | :white_check_mark: | — |  |
| [`enable_flashcomm1`](flags/enable-flashcomm1.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_flashcomm2_parallel_size`](flags/enable-flashcomm2-parallel-size.md) | :white_check_mark: | — | — | v0.23.0 为配置键 + 环境变量回退；v0.30.0 已移除 |
| [`enable_force_eplb`](flags/enable-force-eplb.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`enable_fused_mc2`](flags/enable-fused-mc2.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_kv_nz`](flags/enable-kv-nz.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_kvpp`](flags/enable-kvpp.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`enable_matmul_allreduce`](flags/enable-matmul-allreduce.md) | :white_check_mark: | — | — | v0.23.0 仅环境变量；v0.30.0 已移除 |
| [`enable_mc2_hierarchy_comm`](flags/enable-mc2-hierarchy-comm.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_mlapo`](flags/enable-mlapo.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_pcp_embedding_lmhead_weight_sharding`](flags/enable-pcp-embedding-lmhead-weight-sharding.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`enable_pcp_o_proj_weight_sharding`](flags/enable-pcp-o-proj-weight-sharding.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`enable_prefill_mc2`](flags/enable-prefill-mc2.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_shared_expert_dp`](flags/enable-shared-expert-dp.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`enable_sparse_li_c8`](flags/enable-sparse-li-c8.md) | :white_check_mark: | — | — | v0.30.0 起由 --attention_config.indexer_kv_dtype fp8/int8 派生 |
| [`enable_sparse_sfa_c8`](flags/enable-sparse-sfa-c8.md) | :white_check_mark: | — | — | v0.30.0 起由 --kv-cache-dtype fp8/int8 派生 |
| [`enable_transpose_kv_cache_by_block`](flags/enable-transpose-kv-cache-by-block.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`eplb_config`](flags/eplb-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`finegrained_tp_config`](flags/finegrained-tp-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`hamming_sparse`](flags/hamming-sparse.md) | :white_check_mark: | — | — |  |
| [`kv_pool_range_debug`](flags/kv-pool-range-debug.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`mc2_comm_alg`](flags/mc2-comm-alg.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`mega_moe_max_tokens`](flags/mega-moe-max-tokens.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`mix_placement`](flags/mix-placement.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`mlapo_keep_prefill_weights`](flags/mlapo-keep-prefill-weights.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`msmonitor_use_daemon`](flags/msmonitor-use-daemon.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`multistream_dsv4_dsa_overlap`](flags/multistream-dsv4-dsa-overlap.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`multistream_engram_overlap`](flags/multistream-engram-overlap.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`multistream_overlap_gate`](flags/multistream-overlap-gate.md) | :white_check_mark: | — | — | v0.30.0 起已移除 |
| [`multistream_overlap_shared_expert`](flags/multistream-overlap-shared-expert.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`pa_shape_list`](flags/pa-shape-list.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`profiling_chunk_config`](flags/profiling-chunk-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | v0.30.0 起顶层键废弃（仍可用，发 deprecation 警告），规范写法 scheduler_config.profiling_chunk_config |
| [`recompute_scheduler_enable`](flags/recompute-scheduler-enable.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: | v0.30.0 起顶层键废弃（仍可用，发 deprecation 警告），规范写法 scheduler_config.recompute_scheduler_enable |
| [`refresh`](flags/refresh.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`rejection_sampler_config`](flags/rejection-sampler-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`rl_config`](flags/rl-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`runtime_config`](flags/runtime-config.md) | — | — | :white_check_mark: | main 分支新增，下一版本发布 |
| [`runtime_config_hot_reload`](flags/runtime-config-hot-reload.md) | — | — | :white_check_mark: | main 分支新增，下一版本发布 |
| [`runtime_config_path`](flags/runtime-config-path.md) | — | — | :white_check_mark: | main 分支新增，下一版本发布 |
| [`runtime_dump_dir`](flags/runtime-dump-dir.md) | — | — | — | Runtime Guard 特性的一部分，main 分支新增 |
| [`runtime_report_dir`](flags/runtime-report-dir.md) | — | — | — | Runtime Guard 特性的一部分，main 分支新增 |
| [`scheduler_config`](flags/scheduler-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 新增 |
| [`sfa_dcp_force_tmajor_restore`](flags/sfa-dcp-force-tmajor-restore.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`short_request_first_config`](flags/short-request-first-config.md) | — | :white_check_mark: | :white_check_mark: | v0.30.0 起顶层键废弃（仍可用，发 deprecation 警告），规范写法 scheduler_config.short_request_first_config |
| [`sparse_kv_offload_config`](flags/sparse-kv-offload-config.md) | — | :white_check_mark: | :white_check_mark: |  |
| [`weight_nz_mode`](flags/weight-nz-mode.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
| [`weight_prefetch_config`](flags/weight-prefetch-config.md) | :white_check_mark: | — | — | v0.30.0 起已移除 |
| [`xlite_graph_config`](flags/xlite-graph-config.md) | :white_check_mark: | :white_check_mark: | :white_check_mark: |  |
<!-- MATRIX_END -->

## 数据核验方式

`version_support` 的核验来源是对应 tag 上 `vllm_ascend/envs.py`（环境变量）与 `vllm_ascend/ascend_config.py`（配置键）的逐一比对，个别在源码中拆分到子配置类的开关以官方配置文档交叉确认。发现与实际情况不符时，请直接修改 `data/flags/<key>.yaml` 并提 PR。
