---
title: 特性开关总览
---

# 特性开关总览

> 本页表格由 [`scripts/generate_tables.py`](https://github.com/tanjiangshan/vllm-ascend-feature-flag-handbook/blob/main/scripts/generate_tables.py) 从 `data/flags/*.yaml` 自动生成，请勿手改表格区域。

状态图例：:white_check_mark: active（生效中）｜:warning: deprecated（已弃用，即将移除）｜:x: removed（已移除）｜:construction: planned（规划中）

## 中文速查表

<!-- TABLE_ZH_START -->
| 配置键 | 类型 | 默认值 | 状态 | 旧环境变量 | v0.23 / v0.30 / main | 适用芯片 | 说明 |
|---|---|---|---|---|---|---|---|
| [`ascend_compilation_config`](ascend-compilation-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Ascend 编译配置。 |
| [`ascend_warmup_config`](ascend-warmup-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 与权重加载重叠的启动预热配置。 |
| [`batch_job_sched_config`](batch-job-sched-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 面向 batch-job-aware 调度器的配置。 |
| [`combine_quant_mode`](combine-quant-mode.md) | `int` | `0` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 融合 combine 算子的通信量化模式，作为 comm_quant_mode 传给 npu_moe_distribute_combine_v2。有效范围见算子文档。 |
| [`dump_config`](dump-config.md) | `dict` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 内联 msprobe dump 配置，vLLM-Ascend 会物化为临时 JSON 文件传给调试器。 |
| [`dump_config_path`](dump-config-path.md) | `str` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | msprobe dump 的配置文件路径（兼容旧版选项）。 |
| [`dynamic_eplb`](dynamic-eplb.md) | `bool` | `false` | :white_check_mark: active | `DYNAMIC_EPLB` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | 启用动态专家并行负载均衡（Dynamic EPLB）。属于 eplb_config 子配置；旧版需配合环境变量 DYNAMIC_EPLB=true。 |
| [`dynamic_spec_config`](dynamic-spec-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 动态投机解码（Dynamic Speculative Decoding）配置。 |
| [`dyntra_lb_config`](dyntra-lb-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | PD 分离解码节点 DyntraLB 负载均衡配置。 |
| [`enable_balance_scheduling`](enable-balance-scheduling.md) | `bool` | `false` | :warning: deprecated | `VLLM_ASCEND_BALANCE_SCHEDULING` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用均衡调度。已弃用，请改用 scheduler_config.enable_balance_scheduling。 |
| [`enable_context_parallel`](enable-context-parallel.md) | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` | — — — | All | 启用上下文并行（Context Parallel）。 |
| [`enable_cpu_binding`](enable-cpu-binding.md) | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 在 ARM 服务器上启用昇腾原生 CPU 绑定。设为 false 可禁用。 |
| [`enable_flashcomm1`](enable-flashcomm1.md) | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FLASHCOMM1` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 SP MoE 的 FlashComm1 通信优化。仅 Model Runner V1 支持且需序列并行；MRv2 下启用会报配置错误，请改用 PCP。 |
| [`enable_flashcomm2_parallel_size`](enable-flashcomm2-parallel-size.md) | `int` | `0` | :x: removed | `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` | :white_check_mark: — — | All | FlashComm2 并行规模，0 表示禁用。 |
| [`enable_force_eplb`](enable-force-eplb.md) | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 强制使用确定性轮询专家路由，仅用于性能分析。会替换真实 MoE 路由，导致模型结果与精度无效，切勿用于生产。 |
| [`enable_fused_mc2`](enable-fused-mc2.md) | `int` | `0` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FUSED_MC2` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3, A5 | 融合 MC2（MoE dispatch/combine）配置。A5 上 MegaMoe 需 SiTU 模型暴露 CANN MegaMoe 包装器。 |
| [`enable_kv_nz`](enable-kv-nz.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 KV cache 的 NZ 布局，仅对使用 MLA 的模型（如 DeepSeek）生效。 |
| [`enable_matmul_allreduce`](enable-matmul-allreduce.md) | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` | :white_check_mark: — — | All | 启用 Matmul 与 AllReduce 融合优化。 |
| [`enable_mc2_hierarchy_comm`](enable-mc2-hierarchy-comm.md) | `bool` | `false` | :warning: deprecated | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | 通过 ROCE 启用 dispatch/combine 算子的节点间通信。已弃用，将由 mc2_comm_alg="hierarchy" 取代。 |
| [`enable_mlapo`](enable-mlapo.md) | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_MLAPO` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 MLAPO（模型逐层自适应并行优化）。 |
| [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | PCP size > 1 时，在每个 TP 分片内对 embedding 与 LM Head 权重跨 PCP rank 分片。与 batch-sharded sampling 及这两个模块的细粒度 TP 不兼容。 |
| [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | PCP 是否在组内对 O 投影权重分片（SFA-PCP 的 o_proj 与 DSA-PCP 两阶段 wo_a/wo_b）。不支持的权重方法/PCP 分区会警告并自动禁用；其他注意力后端不使用此选项。 |
| [`enable_prefill_mc2`](enable-prefill-mc2.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为 prefill 批次预留 mc2_token_capacity（用 max_num_batched_tokens 计算）。临时开关，未来 MC2 完备后默认启用并移除。 |
| [`enable_shared_expert_dp`](enable-shared-expert-dp.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 在 TP rank 间复制共享专家权重并以数据并行运行。提升性能但消耗更多内存，与上游 MoE 序列并行相互独立。 |
| [`enable_transpose_kv_cache_by_block`](enable-transpose-kv-cache-by-block.md) | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 是否启用按块转置 KV cache（融合算子路径）。 |
| [`eplb_config`](eplb-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | EPLB（专家并行负载均衡）配置。dynamic_eplb 启用动态均衡；expert_map_record_path 录制映射；expert_map_path 加载静态映射。 |
| [`finegrained_tp_config`](finegrained-tp-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 细粒度张量并行配置。 |
| [`kv_pool_range_debug`](kv-pool-range-debug.md) | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` | — :white_check_mark: :white_check_mark: | All | 为 KV pool 的整键操作、逐层范围和提交操作输出 JSON 审计日志。仅在调试时开启，正常运行保持禁用以避免日志开销。 |
| [`mc2_comm_alg`](mc2-comm-alg.md) | `str` | `""` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | A2, A3 | dispatch/combine 算子的通信算法选择，将取代 enable_mc2_hierarchy_comm。 |
| [`mega_moe_max_tokens`](mega-moe-max-tokens.md) | `int` | `65536` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 融合 MC2/MegaMoe 路径中 dispatch 后每个 rank 的 token 容量参考值。超出可能出现精度下降，需按实际 expert 负载调整。 |
| [`mlapo_keep_prefill_weights`](mlapo-keep-prefill-weights.md) | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | MLAPO 下在 kv_consumer（仅 decode 的 D 节点）保留 prefill 权重而非释放。用 NPU 内存换取稳定性，规避权重释放后本地 prefill 路径崩溃（issue |
| [`msmonitor_use_daemon`](msmonitor-use-daemon.md) | `bool` | `false` | :white_check_mark: active | `MSMONITOR_USE_DAEMON` | :white_check_mark: :white_check_mark: :white_check_mark: | All | msmonitor 是否使用守护进程模式。 |
| [`multistream_dsv4_dsa_overlap`](multistream-dsv4-dsa-overlap.md) | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为 DeepSeek V4 启用 DSA 多流重叠。 |
| [`multistream_overlap_gate`](multistream-overlap-gate.md) | `bool` | `false` | :x: removed | — | :white_check_mark: — — | All | 启用多流重叠门控，仅对含共享专家的 MoE 模型生效。 |
| [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用多流共享专家重叠，仅对含共享专家的 MoE 模型生效。 |
| [`pa_shape_list`](pa-shape-list.md) | `list` | `[]` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | page attention 算子的自定义 shape 列表。 |
| [`profiling_chunk_config`](profiling-chunk-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 动态分块流水线并行（profiling chunk）配置。 |
| [`recompute_scheduler_enable`](recompute-scheduler-enable.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用重计算调度器。仅在 PD 分离的 D 节点（kv_consumer）有效；在 P 节点或 PD-mixed 模式下启用会在启动时报明确错误。 |
| [`refresh`](refresh.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 是否刷新全局 Ascend 配置内容。通常用于 RLHF 或 ut/e2e 测试用例。 |
| [`rejection_sampler_config`](rejection-sampler-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 拒绝采样器配置（block verify 与 entropy verify）。 |
| [`rl_config`](rl-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 一键 RL 模式总开关（enabled: true 时强制 weight_nz_mode=0、设置 VLLM_SERVER_DEV_MODE=1 等固定行为）。子键含 sleep_mode_extra_cleanup、enable_training_consistency、enable_batch_invariant。 |
| [`runtime_config`](runtime-config.md) | `dict` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | 启动时叠加层，与运行时配置默认值合并（检测器、dump 配额、报告标志）。 |
| [`runtime_config_hot_reload`](runtime-config-hot-reload.md) | `bool` | `false` | :white_check_mark: active | — | — — :white_check_mark: | All | 启用 runtime_config.json 热重载（仅启动时生效；不是 JSON 字段）。 |
| [`runtime_config_path`](runtime-config-path.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Runtime Guard JSON 配置路径，默认 /runtime/config/runtime_config.json。 |
| [`runtime_dump_dir`](runtime-dump-dir.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | 设置 KV dump 根目录（dump.dump_dir），默认由报告根目录派生。 |
| [`runtime_report_dir`](runtime-report-dir.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | 覆盖报告根目录，默认 /runtime/report。 |
| [`scheduler_config`](scheduler-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 调度器扩展配置的规范层级，包含均衡调度、重计算调度、DyntraLB、ShortRequestFirst、动态分块流水线并行等。过渡期旧顶层键仍兼容但已弃用。 |
| [`short_request_first_config`](short-request-first-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | ShortRequestFirst prefill 调度配置，用于 FCFS 同步/异步、PD-prefill（P）或 PD-mixed 节点。 |
| [`weight_nz_mode`](weight-nz-mode.md) | `int` | `1` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_NZ` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 权重 NZ 格式模式。0 禁用，1 仅量化权重，2 扩展至 BF16/FP16。 |
| [`weight_prefetch_config`](weight-prefetch-config.md) | `dict` | `{}` | :x: removed | — | :white_check_mark: — — | All | 权重预取配置。 |
| [`xlite_graph_config`](xlite-graph-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Xlite 图模式配置。 |
<!-- TABLE_ZH_END -->

## English quick reference

<!-- TABLE_EN_START -->
| Config key | Type | Default | Status | Legacy env var | v0.23 / v0.30 / main | Hardware | Description |
|---|---|---|---|---|---|---|---|
| [`ascend_compilation_config`](ascend-compilation-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Configuration for Ascend compilation. |
| [`ascend_warmup_config`](ascend-warmup-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Startup warmup configuration that overlaps with weight loading. |
| [`batch_job_sched_config`](batch-job-sched-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Configuration for the batch-job-aware scheduler. |
| [`combine_quant_mode`](combine-quant-mode.md) | `int` | `0` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Communication quantization mode for the fused combine op, passed as comm_quant_mode to npu_moe_distribute_combine_v2. See operator docs for valid values. |
| [`dump_config`](dump-config.md) | `dict` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Inline msprobe dump configuration; vLLM-Ascend materializes it to a temporary JSON file passed to the debugger. |
| [`dump_config_path`](dump-config-path.md) | `str` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Path to the msprobe dump configuration file (legacy-compatible option). |
| [`dynamic_eplb`](dynamic-eplb.md) | `bool` | `false` | :white_check_mark: active | `DYNAMIC_EPLB` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | Enable dynamic Expert Parallelism Load Balancer. Part of eplb_config; legacy mode also requires the DYNAMIC_EPLB=true env var as a safety guard. |
| [`dynamic_spec_config`](dynamic-spec-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Configuration for Dynamic Speculative Decoding. |
| [`dyntra_lb_config`](dyntra-lb-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | DyntraLB load-balancing configuration for PD-disaggregated decode nodes. |
| [`enable_balance_scheduling`](enable-balance-scheduling.md) | `bool` | `false` | :warning: deprecated | `VLLM_ASCEND_BALANCE_SCHEDULING` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable balance scheduling. Deprecated, use scheduler_config.enable_balance_scheduling instead. |
| [`enable_context_parallel`](enable-context-parallel.md) | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` | — — — | All | Enable Context Parallelism. |
| [`enable_cpu_binding`](enable-cpu-binding.md) | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable Ascend-native CPU binding on ARM servers. Set to false to disable. |
| [`enable_flashcomm1`](enable-flashcomm1.md) | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FLASHCOMM1` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable FlashComm1 for SP MoE. Model Runner V1 only and requires sequence parallelism; errors on MRv2 — use PCP instead. |
| [`enable_flashcomm2_parallel_size`](enable-flashcomm2-parallel-size.md) | `int` | `0` | :x: removed | `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` | :white_check_mark: — — | All | FlashComm2 parallel size; 0 disables it. |
| [`enable_force_eplb`](enable-force-eplb.md) | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Force deterministic round-robin expert routing, for profiling only. Replaces real MoE routing so model output/accuracy is invalid — never use in production. |
| [`enable_fused_mc2`](enable-fused-mc2.md) | `int` | `0` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FUSED_MC2` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3, A5 | Fused MC2 (MoE dispatch/combine) configuration. On A5, MegaMoe requires SiTU models to expose the CANN MegaMoe wrapper. |
| [`enable_kv_nz`](enable-kv-nz.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable NZ layout for KV cache; only effective for MLA models such as DeepSeek. |
| [`enable_matmul_allreduce`](enable-matmul-allreduce.md) | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` | :white_check_mark: — — | All | Enable fused Matmul+AllReduce optimization. |
| [`enable_mc2_hierarchy_comm`](enable-mc2-hierarchy-comm.md) | `bool` | `false` | :warning: deprecated | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | Enable inter-node RoCE communication for dispatch/combine ops. Deprecated, replaced by mc2_comm_alg="hierarchy". |
| [`enable_mlapo`](enable-mlapo.md) | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_MLAPO` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable MLAPO (Model Layer-wise Adaptive Parallel Optimization). |
| [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | When PCP size > 1, shard embedding and LM Head weights across PCP ranks within each TP shard. Incompatible with batch-sharded sampling and fine-grained TP for these modules. |
| [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Whether PCP shards O-projection weights inside the group (SFA-PCP o_proj and DSA-PCP two-stage wo_a/wo_b). Auto-disabled with a warning when unsupported; unused by other attention backends. |
| [`enable_prefill_mc2`](enable-prefill-mc2.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Reserve mc2_token_capacity for prefill batches using max_num_batched_tokens. Temporary switch; will be removed once MC2 is complete. |
| [`enable_shared_expert_dp`](enable-shared-expert-dp.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Replicate shared-expert weights across TP ranks and run them data-parallel. Improves performance at higher memory cost; independent of upstream MoE sequence parallelism. |
| [`enable_transpose_kv_cache_by_block`](enable-transpose-kv-cache-by-block.md) | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Whether to enable block-wise transposed KV cache (fused-op path). |
| [`eplb_config`](eplb-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | EPLB (Expert Parallelism Load Balancer) config. dynamic_eplb enables dynamic balancing; expert_map_record_path records maps; expert_map_path loads static maps. |
| [`finegrained_tp_config`](finegrained-tp-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Configuration for fine-grained tensor parallelism. |
| [`kv_pool_range_debug`](kv-pool-range-debug.md) | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` | — :white_check_mark: :white_check_mark: | All | Emit per-layer KVPool ranged-transfer audit events as JSON. Debug only; keep disabled in production to avoid logging overhead. |
| [`mc2_comm_alg`](mc2-comm-alg.md) | `str` | `""` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | A2, A3 | Communication algorithm for dispatch/combine ops; supersedes enable_mc2_hierarchy_comm. |
| [`mega_moe_max_tokens`](mega-moe-max-tokens.md) | `int` | `65536` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Per-rank token capacity after dispatch in the fused MC2/MegaMoe path. Exceeding it may degrade accuracy; tune to actual expert load. |
| [`mlapo_keep_prefill_weights`](mlapo-keep-prefill-weights.md) | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Keep MLAPO prefill weights on kv_consumer (decode-only D nodes) instead of freeing them. Trades NPU memory for stability against local-prefill crashes after weight freeing (issue |
| [`msmonitor_use_daemon`](msmonitor-use-daemon.md) | `bool` | `false` | :white_check_mark: active | `MSMONITOR_USE_DAEMON` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Whether msmonitor uses daemon mode. |
| [`multistream_dsv4_dsa_overlap`](multistream-dsv4-dsa-overlap.md) | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable DSA multi-stream overlap for DeepSeek V4. |
| [`multistream_overlap_gate`](multistream-overlap-gate.md) | `bool` | `false` | :x: removed | — | :white_check_mark: — — | All | Enable multi-stream overlap gating; only effective on MoE models with shared experts. |
| [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable multi-stream overlap for the shared expert; only effective on MoE models with shared experts. |
| [`pa_shape_list`](pa-shape-list.md) | `list` | `[]` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Custom shape list for page-attention ops. |
| [`profiling_chunk_config`](profiling-chunk-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Configuration for dynamic chunked pipeline parallel (profiling chunk). |
| [`recompute_scheduler_enable`](recompute-scheduler-enable.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Enable the recompute scheduler. Only valid on PD-disaggregated D nodes (kv_consumer); enabling it on P nodes or PD-mixed mode fails startup with a clear error. |
| [`refresh`](refresh.md) | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Whether to refresh the global Ascend configuration. Usually used by RLHF or ut/e2e tests. |
| [`rejection_sampler_config`](rejection-sampler-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Rejection sampler configuration (block verify and entropy verify). |
| [`rl_config`](rl-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | One-click RL mode (enabled: true forces weight_nz_mode=0, VLLM_SERVER_DEV_MODE=1, etc.). Sub-keys include sleep_mode_extra_cleanup, enable_training_consistency, enable_batch_invariant. |
| [`runtime_config`](runtime-config.md) | `dict` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Startup overlay merged into runtime config defaults (detectors, dump quota, report flags). |
| [`runtime_config_hot_reload`](runtime-config-hot-reload.md) | `bool` | `false` | :white_check_mark: active | — | — — :white_check_mark: | All | Enable hot-reload of runtime_config.json (startup-only; not a JSON field). |
| [`runtime_config_path`](runtime-config-path.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Path to the Runtime Guard JSON config. Default: /runtime/config/runtime_config.json. |
| [`runtime_dump_dir`](runtime-dump-dir.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Set the KV dump root directory (dump.dump_dir). Default derived from the report root. |
| [`runtime_report_dir`](runtime-report-dir.md) | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Override the report root directory. Default: /runtime/report. |
| [`scheduler_config`](scheduler-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Canonical nesting for scheduler extensions: balance scheduling, recompute scheduling, DyntraLB, ShortRequestFirst, dynamic chunked pipeline parallel, etc. Legacy top-level keys still parse but are deprecated. |
| [`short_request_first_config`](short-request-first-config.md) | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | ShortRequestFirst prefill scheduling config for FCFS sync/async, PD-prefill (P) or PD-mixed nodes. |
| [`weight_nz_mode`](weight-nz-mode.md) | `int` | `1` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_NZ` | :white_check_mark: :white_check_mark: :white_check_mark: | All | Weight NZ layout mode. 0 disables NZ, 1 enables for quantized weights only, 2 extends to BF16/FP16 when supported. |
| [`weight_prefetch_config`](weight-prefetch-config.md) | `dict` | `{}` | :x: removed | — | :white_check_mark: — — | All | Weight prefetch configuration. |
| [`xlite_graph_config`](xlite-graph-config.md) | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Configuration for Xlite graph mode. |
<!-- TABLE_EN_END -->

## 如何阅读本表

- **配置键**：`--additional-config` 中使用的 JSON 键名，点击进入详情页。
- **旧环境变量**：该配置迁移前的环境变量名。PR #9064 起，环境变量统一迁移至 `--additional-config`，过渡期两者均可使用，未来版本将移除环境变量。
- **v0.23 / v0.30 / main**：该开关在三个版本中的支持情况（✅ 支持 / — 不存在），数据核验方式见[版本支持矩阵](../version-matrix.md)。
- **适用芯片**："All" 表示未观察到芯片限制；列出型号表示仅在该芯片上有意义。
- **说明**：一句话概括用途。详细原理、用法示例与风险提示见各详情页。
