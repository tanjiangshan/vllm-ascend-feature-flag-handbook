---
title: 特性开关总览
---

# 特性开关总览

> 本页表格由 [`scripts/generate_tables.py`](https://github.com/tanjiangshan/vllm-ascend-feature-flag-handbook/blob/main/scripts/generate_tables.py) 从 `data/flags/*.yaml` 自动生成，请勿手改表格区域。

状态图例：:white_check_mark: active（生效中）｜:warning: deprecated（已弃用，即将移除）｜:x: removed（已移除）｜:construction: planned（规划中）

## 中文速查表

<!-- TABLE_ZH_START -->
| 配置键 | 中文名 | 类型 | 默认值 | 状态 | 旧环境变量 | v0.23 / v0.30 / main | 适用芯片 | 说明 |
|---|---|---|---|---|---|---|---|---|
| [`ascend_compilation_config`](ascend-compilation-config.md) | Ascend 编译配置 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Ascend 编译配置。 |
| [`ascend_fusion_config`](ascend-fusion-config.md) | 融合算子配置 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 融合算子配置。子键 fusion_ops_gmmswigluquant（默认 true）控制是否使用 GmmSwigluQuant 融合算子。pydantic 校验会拒绝未知子键。 |
| [`ascend_log_path`](ascend-log-path.md) | Ascend 日志路径 | `str` | `"~/ascend/log/vllm_ascend"` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | vLLM-Ascend 日志输出路径，默认 ~/ascend/log/vllm_ascend。 |
| [`ascend_warmup_config`](ascend-warmup-config.md) | 启动预热配置 | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 与权重加载重叠的启动预热配置。 |
| [`batch_job_sched_config`](batch-job-sched-config.md) | 批作业调度配置 | `dict` | `{}` | :warning: deprecated | — | — :white_check_mark: :white_check_mark: | All | 面向 batch-job-aware 调度器的配置。v0.30.0 起顶层键废弃，请改用 scheduler_config.batch_job_sched_config。 |
| [`c8_enable_reshape_optim`](c8-enable-reshape-optim.md) | C8 reshape 优化 | `bool` | `false` | :x: removed | — | :white_check_mark: — — | All | LI-C8 的 reshape 优化（仅在 enable_sparse_li_c8 开启时生效）。v0.30.0 起从源码移除。 |
| [`combine_quant_mode`](combine-quant-mode.md) | Combine 通信量化 | `int` | `0` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 融合 combine 算子的通信量化模式，作为 comm_quant_mode 传给 npu_moe_distribute_combine_v2。有效范围见算子文档。 |
| [`draft_window_size`](draft-window-size.md) | 草稿 KV 滑窗 | `int` | `"None"` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 投机解码的草稿 KV 滑窗：仅将草稿模型注意力限制在最近 N 个 token，目标模型仍用全上下文，输出质量不变。适配 eagle3/dflash/dspark 方法；长上下文运行时超出草稿训练长度导致接受率崩塌的场景使用。 |
| [`dump_config`](dump-config.md) | msprobe 内联 dump | `dict` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 内联 msprobe dump 配置，vLLM-Ascend 会物化为临时 JSON 文件传给调试器。 |
| [`dump_config_path`](dump-config-path.md) | msprobe dump 路径 | `str` | `None` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | msprobe dump 的配置文件路径（兼容旧版选项）。 |
| [`dynamic_eplb`](dynamic-eplb.md) | 动态专家负载均衡 | `bool` | `false` | :white_check_mark: active | `DYNAMIC_EPLB` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | 启用动态专家并行负载均衡（Dynamic EPLB）。属于 eplb_config 子配置；旧版需配合环境变量 DYNAMIC_EPLB=true。 |
| [`dynamic_spec_config`](dynamic-spec-config.md) | 动态投机解码配置 | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 动态投机解码（Dynamic Speculative Decoding）配置。 |
| [`dyntra_lb_config`](dyntra-lb-config.md) | DyntraLB 负载均衡 | `dict` | `{}` | :warning: deprecated | — | — :white_check_mark: :white_check_mark: | All | PD 分离解码节点 DyntraLB 负载均衡配置。仅配置在 Decode 节点上。v0.30.0 起顶层键废弃，请改用 scheduler_config.dyntra_lb_config。 |
| [`enable_balance_scheduling`](enable-balance-scheduling.md) | 均衡调度 | `bool` | `false` | :warning: deprecated | `VLLM_ASCEND_BALANCE_SCHEDULING` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用均衡调度。v0.30.0 起顶层键废弃（发 deprecation 警告），请改用 scheduler_config.enable_balance_scheduling。 |
| [`enable_context_parallel`](enable-context-parallel.md) | 上下文并行 | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_CONTEXT_PARALLEL` | — — — | All | 启用上下文并行（Context Parallel）。 |
| [`enable_cpu_binding`](enable-cpu-binding.md) | 昇腾 CPU 绑定 | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 在 ARM 服务器上启用昇腾原生 CPU 绑定。设为 false 可禁用。 |
| [`enable_flashcomm1`](enable-flashcomm1.md) | FlashComm1 通信优化 | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FLASHCOMM1` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 SP MoE 的 FlashComm1 通信优化。仅 Model Runner V1 支持且需序列并行；MRv2 下启用会报配置错误，请改用 PCP。 |
| [`enable_flashcomm2_parallel_size`](enable-flashcomm2-parallel-size.md) | FlashComm2 并行规模 | `int` | `0` | :x: removed | `VLLM_ASCEND_FLASHCOMM2_PARALLEL_SIZE` | :white_check_mark: — — | All | FlashComm2 并行规模，0 表示禁用。 |
| [`enable_force_eplb`](enable-force-eplb.md) | 强制轮询专家路由 | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 强制使用确定性轮询专家路由，仅用于性能分析。会替换真实 MoE 路由，导致模型结果与精度无效，切勿用于生产。 |
| [`enable_fused_mc2`](enable-fused-mc2.md) | 融合 MC2 算子 | `int` | `0` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_FUSED_MC2` | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3, A5 | 融合 MC2（MoE dispatch/combine）配置。A5 上 MegaMoe 需 SiTU 模型暴露 CANN MegaMoe 包装器。 |
| [`enable_kv_nz`](enable-kv-nz.md) | KV NZ 布局 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 KV cache 的 NZ 布局，仅对使用 MLA 的模型（如 DeepSeek）生效。 |
| [`enable_kvpp`](enable-kvpp.md) | KV 按层并行（KVPP） | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 启用 KVPP（KV 流水线并行），把 MLA/SFA 非混合模型在 TP 各 rank 间冗余的 KV cache 按层分摊，同等显存容纳更多上下文 token 或并发请求。Experimental；仅支持 eager 或 PIECEWISE 图模式；PD 分离时只能在 prefill 节点开启。 |
| [`enable_matmul_allreduce`](enable-matmul-allreduce.md) | Matmul-AllReduce 融合 | `bool` | `false` | :x: removed | `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE` | :white_check_mark: — — | All | 启用 Matmul 与 AllReduce 融合优化。 |
| [`enable_mc2_hierarchy_comm`](enable-mc2-hierarchy-comm.md) | MC2 跨机分层通信 | `bool` | `false` | :warning: deprecated | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | 通过 ROCE 启用 dispatch/combine 算子的节点间通信。已弃用，将由 mc2_comm_alg="hierarchy" 取代。 |
| [`enable_mlapo`](enable-mlapo.md) | MLAPO 逐层并行优化 | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_MLAPO` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用 MLAPO（模型逐层自适应并行优化）。 |
| [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) | PCP Embedding/LMHead 分片 | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | PCP size > 1 时，在每个 TP 分片内对 embedding 与 LM Head 权重跨 PCP rank 分片。与 batch-sharded sampling 及这两个模块的细粒度 TP 不兼容。 |
| [`enable_pcp_o_proj_weight_sharding`](enable-pcp-o-proj-weight-sharding.md) | PCP O 投影分片 | `bool` | `true` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | PCP 是否在组内对 O 投影权重分片（SFA-PCP 的 o_proj 与 DSA-PCP 两阶段 wo_a/wo_b）。不支持的权重方法/PCP 分区会警告并自动禁用；其他注意力后端不使用此选项。 |
| [`enable_prefill_mc2`](enable-prefill-mc2.md) | Prefill MC2 预留 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为 prefill 批次预留 mc2_token_capacity（用 max_num_batched_tokens 计算）。临时开关，未来 MC2 完备后默认启用并移除。 |
| [`enable_shared_expert_dp`](enable-shared-expert-dp.md) | 共享专家数据并行 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 在 TP rank 间复制共享专家权重并以数据并行运行。提升性能但消耗更多内存，与上游 MoE 序列并行相互独立。 |
| [`enable_sparse_li_c8`](enable-sparse-li-c8.md) | LI-C8 稀疏缓存 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为稀疏注意力（Lightning Indexer）启用 C8 KV cache 布局。与 enable_sparse_li_c4 互斥。官方 GLM5.2 教程实测开启。 |
| [`enable_sparse_sfa_c8`](enable-sparse-sfa-c8.md) | SFA-C8 稀疏缓存 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为 SFA（Sparse Flash Attention）稀疏注意力启用 C8 KV cache 布局。官方 GLM5 / GLM5.2 教程实测开启。 |
| [`enable_transpose_kv_cache_by_block`](enable-transpose-kv-cache-by-block.md) | KV 按块转置 | `bool` | `true` | :white_check_mark: active | `VLLM_ASCEND_FUSION_OP_TRANSPOSE_KV_CACHE_BY_BLOCK` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 是否启用按块转置 KV cache（融合算子路径）。 |
| [`eplb_config`](eplb-config.md) | EPLB 配置 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | A2, A3 | EPLB（专家并行负载均衡）配置。dynamic_eplb 启用动态均衡；expert_map_record_path 录制映射；expert_map_path 加载静态映射。 |
| [`finegrained_tp_config`](finegrained-tp-config.md) | 细粒度 TP 配置 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 细粒度张量并行配置。 |
| [`hamming_sparse`](hamming-sparse.md) | Hamming 稀疏注意力 | `dict` | `{"enabled": false, "sparse_json_location": ""}` | :x: removed | — | :white_check_mark: — — | All | Hamming 稀疏注意力配置，dict 含 enabled 与 sparse_json_location（稀疏 JSON 文件路径，须真实存在）。v0.30.0 起从源码移除。 |
| [`kv_pool_range_debug`](kv-pool-range-debug.md) | KV 池审计日志 | `bool` | `false` | :white_check_mark: active | `VLLM_ASCEND_KVPOOL_RANGE_DEBUG` | — :white_check_mark: :white_check_mark: | All | 为 KV pool 的整键操作、逐层范围和提交操作输出 JSON 审计日志。仅在调试时开启，正常运行保持禁用以避免日志开销。 |
| [`mc2_comm_alg`](mc2-comm-alg.md) | MC2 通信算法 | `str` | `""` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | A2, A3 | dispatch/combine 算子的通信算法选择，将取代 enable_mc2_hierarchy_comm。 |
| [`mega_moe_max_tokens`](mega-moe-max-tokens.md) | MegaMoe token 容量 | `int` | `65536` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 融合 MC2/MegaMoe 路径中 dispatch 后每个 rank 的 token 容量参考值。超出可能出现精度下降，需按实际 expert 负载调整。 |
| [`mix_placement`](mix-placement.md) | 专家混合放置 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 混合放置模式（DP×TP 平面上的专家/权重放置策略），计入 RFork 权重传输的兼容性指纹；发送端与接收端配置不一致会导致指纹不匹配。 |
| [`mlapo_keep_prefill_weights`](mlapo-keep-prefill-weights.md) | 保留 prefill 权重 | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | MLAPO 下在 kv_consumer（仅 decode 的 D 节点）保留 prefill 权重而非释放。用 NPU 内存换取稳定性，规避权重释放后本地 prefill 路径崩溃（issue |
| [`msmonitor_use_daemon`](msmonitor-use-daemon.md) | msmonitor 守护模式 | `bool` | `false` | :white_check_mark: active | `MSMONITOR_USE_DAEMON` | :white_check_mark: :white_check_mark: :white_check_mark: | All | msmonitor 是否使用守护进程模式。 |
| [`multistream_dsv4_dsa_overlap`](multistream-dsv4-dsa-overlap.md) | DSV4 DSA 多流重叠 | `bool` | `true` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 为 DeepSeek V4 启用 DSA 多流重叠。 |
| [`multistream_engram_overlap`](multistream-engram-overlap.md) | Engram 多流重叠 | `bool` | `"硬件派生（A5 默认 true，其余 false）"` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | Engram 模块多流重叠。默认仅在 A5（FP8 优化设备家族）开启；显式设置覆盖默认策略。FULL 图需在消费者侧等待描述符相关的外部事件，故默认策略因硬件而异。 |
| [`multistream_overlap_gate`](multistream-overlap-gate.md) | 多流门控重叠 | `bool` | `false` | :x: removed | — | :white_check_mark: — — | All | 启用多流重叠门控，仅对含共享专家的 MoE 模型生效。已移除（v0.30.0 起源码无读取点）。 |
| [`multistream_overlap_shared_expert`](multistream-overlap-shared-expert.md) | 共享专家多流重叠 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用多流共享专家重叠，仅对含共享专家的 MoE 模型生效。 |
| [`pa_shape_list`](pa-shape-list.md) | PA 算子 shape 列表 | `list` | `[]` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | page attention 算子的自定义 shape 列表。 |
| [`profiling_chunk_config`](profiling-chunk-config.md) | 分块流水线配置 | `dict` | `{}` | :warning: deprecated | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 动态分块流水线并行（profiling chunk）配置。v0.30.0 起顶层键废弃，请改用 scheduler_config.profiling_chunk_config。 |
| [`recompute_scheduler_enable`](recompute-scheduler-enable.md) | 重计算调度 | `bool` | `false` | :warning: deprecated | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 启用重计算调度器。仅在 PD 分离的 D 节点（kv_consumer）有效；在 P 节点或 PD-mixed 模式下启用会在启动时报明确错误。v0.30.0 起顶层键废弃，请改用 scheduler_config.recompute_scheduler_enable。 |
| [`refresh`](refresh.md) | 全局配置刷新 | `bool` | `false` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 是否刷新全局 Ascend 配置内容。通常用于 RLHF 或 ut/e2e 测试用例。 |
| [`rejection_sampler_config`](rejection-sampler-config.md) | 拒绝采样器配置 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | 拒绝采样器配置（block verify 与 entropy verify）。 |
| [`rl_config`](rl-config.md) | RL 模式总开关 | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 一键 RL 模式总开关（enabled: true 时强制 weight_nz_mode=0、设置 VLLM_SERVER_DEV_MODE=1 等固定行为）。子键含 sleep_mode_extra_cleanup、enable_training_consistency、enable_batch_invariant。 |
| [`runtime_config`](runtime-config.md) | 运行时配置叠加 | `dict` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | 启动时叠加层，与运行时配置默认值合并（检测器、dump 配额、报告标志）。 |
| [`runtime_config_hot_reload`](runtime-config-hot-reload.md) | 运行时配置热重载 | `bool` | `false` | :white_check_mark: active | — | — — :white_check_mark: | All | 启用 runtime_config.json 热重载（仅启动时生效；不是 JSON 字段）。 |
| [`runtime_config_path`](runtime-config-path.md) | Runtime Guard 路径 | `str` | `None` | :white_check_mark: active | — | — — :white_check_mark: | All | Runtime Guard JSON 配置路径，默认 /runtime/config/runtime_config.json。 |
| [`runtime_dump_dir`](runtime-dump-dir.md) | KV dump 目录 | `str` | `None` | :x: removed | — | — — — | All | 设置 KV dump 根目录（dump.dump_dir），默认由报告根目录派生。已移除，请改用 runtime_config.dump.dump_dir。 |
| [`runtime_report_dir`](runtime-report-dir.md) | 报告根目录 | `str` | `None` | :x: removed | — | — — — | All | 覆盖报告根目录，默认 /runtime/report。已移除，请改用 runtime_config.report_dir。 |
| [`scheduler_config`](scheduler-config.md) | 调度器扩展配置 | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | 调度器扩展配置的规范层级，包含均衡调度、重计算调度、DyntraLB、ShortRequestFirst、动态分块流水线并行等。过渡期旧顶层键仍兼容但已弃用。 |
| [`sfa_dcp_force_tmajor_restore`](sfa-dcp-force-tmajor-restore.md) | SFA DCP T-major 恢复 | `bool` | `false` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | All | SFA 注意力在 DCP（Decode Context Parallel）下强制 T-major 布局恢复，仅调试/兼容用途，正常部署无需设置。 |
| [`short_request_first_config`](short-request-first-config.md) | 短请求优先调度 | `dict` | `{}` | :warning: deprecated | — | — :white_check_mark: :white_check_mark: | All | ShortRequestFirst prefill 调度配置，用于 FCFS 同步/异步、PD-prefill（P）或 PD-mixed 节点。v0.30.0 起顶层键废弃，请改用 scheduler_config.short_request_first_config。 |
| [`sparse_kv_offload_config`](sparse-kv-offload-config.md) | 稀疏 KV 卸载 | `dict` | `{}` | :white_check_mark: active | — | — :white_check_mark: :white_check_mark: | A5 | 稀疏 KV cache 卸载到 DRAM 的配置。子键：enabled、topk_buffer_size（-1 自动解析为 (1+投机 token 数)×2048）、dram_size_per_dp_GB（110）、keep_device_kv_cache、use_fused_overlap。仅 950 系列产品（A5）；勿在 prefill 节点设置。 |
| [`weight_nz_mode`](weight-nz-mode.md) | 权重 NZ 格式 | `int` | `1` | :white_check_mark: active | `VLLM_ASCEND_ENABLE_NZ` | :white_check_mark: :white_check_mark: :white_check_mark: | All | 权重 NZ 格式模式。0 禁用，1 仅量化权重，2 扩展至 BF16/FP16。 |
| [`weight_prefetch_config`](weight-prefetch-config.md) | 权重预取配置 | `dict` | `{}` | :x: removed | — | :white_check_mark: — — | All | 权重预取配置。已移除（v0.30.0 起源码无读取点）。 |
| [`xlite_graph_config`](xlite-graph-config.md) | Xlite 图模式 | `dict` | `{}` | :white_check_mark: active | — | :white_check_mark: :white_check_mark: :white_check_mark: | All | Xlite 图模式配置。 |
<!-- TABLE_ZH_END -->


## 如何阅读本表

- **配置键**：`--additional-config` 中使用的 JSON 键名，点击进入详情页。
- **旧环境变量**：该配置迁移前的环境变量名。PR #9064 起，环境变量统一迁移至 `--additional-config`，过渡期两者均可使用，未来版本将移除环境变量。
- **v0.23 / v0.30 / main**：该开关在三个版本中的支持情况（✅ 支持 / — 不存在），数据核验方式见[版本支持矩阵](../version-matrix.md)。
- **适用芯片**："All" 表示未观察到芯片限制；列出型号表示仅在该芯片上有意义。
- **说明**：一句话概括用途。详细原理、用法示例与风险提示见各详情页。
