---
title: Feature Topics
---

# Feature Topics

> This page groups all 64 feature flags into 9 topics by the problem they solve. Each topic opens with the principle (what it is, what problem it solves), followed by a member table (one-liner + when to enable). For single-parameter lookup use the [feature flags overview](flags/index.md); for depth, each flag's detail page.

## 1. MoE Communication & Compute Overlap { #t-moe }

Every MoE layer runs two collective communications: dispatch routes tokens to experts, combine gathers results back. Communication grows linearly with EP size and can dominate compute. The flags here do three things: **fuse** (merge dispatch/combine into one operator), **overlap** (hide communication behind compute on extra streams), and **quantize** (shrink communication bytes). MoE-only (DeepSeek/GLM/Kimi class) — no effect on dense models.

| Flag | One-liner | When to enable |
|---|---|---|
| [`enable_fused_mc2`](flags/enable-fused-mc2.md) | Fused MC2 dispatch/combine operator (0 off / 1 on / 2 MegaMoE) | On per official model recipes; A5 MegaMoE requires SiTU models |
| [`mc2_comm_alg`](flags/mc2-comm-alg.md) | dispatch/combine communication algorithm (fullmesh/hierarchy/fullmesh_v2) | Cross-node MoE, per chip: hierarchy A2/A3 only, fullmesh_v2 A3 only |
| [`combine_quant_mode`](flags/combine-quant-mode.md) | Combine communication quantization (e.g. 4 = FP8) | Cross-node combine bandwidth bottleneck, per official recipes (DeepSeek-V4 D node) |
| [`enable_shared_expert_dp`](flags/enable-shared-expert-dp.md) | Run shared experts data-parallel across TP ranks | TP>1 with high shared-expert share; trades memory for performance |
| [`multistream_overlap_shared_expert`](flags/multistream-overlap-shared-expert.md) | Overlap shared-expert compute and communication on a dedicated stream | MoE with shared experts; when TP=1 or shared_expert_dp is on |
| [`multistream_dsv4_dsa_overlap`](flags/multistream-dsv4-dsa-overlap.md) | DSA multi-stream overlap for DeepSeek V4 | On by default; applies to DSV4 models |
| [`multistream_engram_overlap`](flags/multistream-engram-overlap.md) | Engram module multi-stream overlap | A5-only by default; explicit value overrides |
| [`enable_flashcomm1`](flags/enable-flashcomm1.md) | FlashComm1 communication optimization for SP MoE | Model Runner V1 only; use PCP on MRv2 |
| [`enable_prefill_mc2`](flags/enable-prefill-mc2.md) | Reserve MC2 token capacity for prefill batches | P node (PD-disaggregated); officially a temporary switch |
| [`mix_placement`](flags/mix-placement.md) | Mixed expert placement on the DP×TP plane | Sender and receiver configs must match (RFork weight-transfer fingerprint) |
| ~~enable_mc2_hierarchy_comm~~ | Deprecated | Use `mc2_comm_alg="hierarchy"` instead |
| ~~enable_matmul_allreduce~~ / ~~enable_flashcomm2_parallel_size~~ / ~~multistream_overlap_gate~~ | Removed | See detail pages / version history |

## 2. Load Balancing & Scheduling { #t-scheduling }

EP's pain is **routing imbalance**: hot experts queue while cold ones idle. This family covers four layers: EP weight balancing (EPLB), PD-disaggregated scheduling (recompute/balance/short-request-first), batch-job scenarios, and RL sampling. Many are mutually exclusive — **startup validates combinations** and fails loudly on illegal ones.

| Flag | One-liner | When to enable |
|---|---|---|
| [`eplb_config`](flags/eplb-config.md) | EPLB balancing config (dynamic_eplb / expert_map_record sub-keys) | Standard concern for EP deployments; dynamic balancing also needs `DYNAMIC_EPLB=true` |
| [`enable_force_eplb`](flags/enable-force-eplb.md) | Force deterministic round-robin expert routing | **Performance analysis only** — replaces real routing and invalidates outputs; never production |
| [`scheduler_config`](flags/scheduler-config.md) | Canonical aggregation layer for scheduling extensions | Since v0.30.0 all scheduling keys are unified here |
| [`recompute_scheduler_enable`](flags/recompute-scheduler-enable.md) | Recompute scheduling (recompute instead of storing KV on refill) | **PD-disaggregated D nodes only** — startup error on P / mixed |
| [`dyntra_lb_config`](flags/dyntra-lb-config.md) | DyntraLB dynamic load balancing | **PD-disaggregated D nodes only**, DP>1; never on P |
| [`enable_balance_scheduling`](flags/enable-balance-scheduling.md) | Balanced scheduling | **PD-mixed only** (A3 single-node / colocated) |
| [`short_request_first_config`](flags/short-request-first-config.md) | Short-request-first prefill scheduling | Ordinary / PD-mixed / P node; **not supported on D nodes** |
| [`batch_job_sched_config`](flags/batch-job-sched-config.md) | Batch-job-aware scheduling | Batch workloads; cannot combine with ShortRequestFirst |
| ~~old top-level keys~~ | Merged into scheduler_config since v0.30.0 | Old keys still work in transition but warn |

Official guides: [DyntraLB](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dyntra_lb.html) · [ShortRequestFirst](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/short_request_first.html) · [Dynamic chunked pipeline](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)

## 3. KV Cache Quantization & Memory Formats { #t-kvfmt }

KV cache is the #1 memory consumer in long-context serving. This family governs **layout** (NZ / T-major / per-block transpose), **quantization** (C8 sparse layouts, int8/mxfp8 — the latter via CLI value-domain patches), and **offloading** (sparse KV to DRAM) — cutting KV memory with no (or minimal) precision loss.

| Flag | One-liner | When to enable |
|---|---|---|
| [`weight_nz_mode`](flags/weight-nz-mode.md) | Weight NZ format (0 off / 1 quantized only / 2 incl. BF16/FP16) | Follow official model recipes per weight format |
| [`enable_kv_nz`](flags/enable-kv-nz.md) | NZ layout for KV cache | MLA models only (DeepSeek class) |
| [`enable_transpose_kv_cache_by_block`](flags/enable-transpose-kv-cache-by-block.md) | Per-block transposed KV cache (fused-op path) | On by default; required by fused attention path |
| [`sparse_kv_offload_config`](flags/sparse-kv-offload-config.md) | Offload sparse KV cache to DRAM | **Never on Prefill** (official); D node per memory pressure |
| ~~enable_sparse_li_c8~~ / ~~enable_sparse_sfa_c8~~ | Removed | Since v0.30.0 derived from `--attention_config.indexer_kv_dtype` / `--kv-cache-dtype` ∈ {fp8,int8} |
| ~~c8_enable_reshape_optim~~ / ~~hamming_sparse~~ | Removed | See version history |

Related engine arg: [kv-cache-dtype value patches](engine-args/kv-cache-dtype.md) (int8/mxfp8)

## 4. Graphs & Compilation { #t-graph }

Graph capture freezes a whole forward step into one replay, eliminating kernel-launch and CPU-scheduling overhead — decode steps (1 token per sequence) benefit most. The family splits into two layers: **vLLM layer** (`--compilation-config`, cross-platform) and **Ascend platform layer** (these flags: ACLGraph/Xlite and operator fusion). The platform layer arbitrates the final mode — don't let the two layers fight.

| Flag | One-liner | When to enable |
|---|---|---|
| [`ascend_compilation_config`](flags/ascend-compilation-config.md) | Ascend graph compilation config (enable_npugraph_ex etc.) | Official PD recipes enable npugraph_ex on D; P often runs eager |
| [`xlite_graph_config`](flags/xlite-graph-config.md) | Xlite graph mode (full_mode controls prefill capture) | Supported models per official graph_mode guide |
| [`ascend_fusion_config`](flags/ascend-fusion-config.md) | Fused-operator config (GmmSwigluQuant etc.) | Per model recipes; most sub-keys default on |
| [`ascend_warmup_config`](flags/ascend-warmup-config.md) | Startup warmup overlapping weight loading | Large models to cut startup time |

Related engine arg: [--compilation-config](engine-args/compilation-config.md) (all cudagraph_mode values) · official [graph_mode guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/graph_mode.html)

## 5. PD Disaggregation & Parallelism { #t-pd }

PD disaggregation splits prefill (compute-bound) from decode (bandwidth/memory-bound) onto separate nodes that scale independently. This family covers **long-context parallelism forms** (PCP for prefill / DCP for decode), **fine-grained TP** (memory for concurrency on D), **MLAPO layer-wise parallelism**, and **CPU binding**.

| Flag | One-liner | When to enable |
|---|---|---|
| [`enable_pcp_embedding_lmhead_weight_sharding`](flags/enable-pcp-embedding-lmhead-weight-sharding.md) | Shard Embedding/LMHead weights within PCP groups | Default on when PCP>1 |
| [`enable_pcp_o_proj_weight_sharding`](flags/enable-pcp-o-proj-weight-sharding.md) | Shard O-projection weights within PCP groups | Default on when PCP>1 |
| [`finegrained_tp_config`](flags/finegrained-tp-config.md) | Fine-grained TP (independent TP degrees for oproj/mlp/lmhead/embedding) | **PD-disaggregated D nodes only** (oproj/mlp>1 startup-validated), with recompute scheduling + preempt offload |
| [`enable_mlapo`](flags/enable-mlapo.md) | MLAPO layer-wise adaptive parallelism | **Decode nodes only in PD** (official); consumes more memory |
| [`mlapo_keep_prefill_weights`](flags/mlapo-keep-prefill-weights.md) | Keep prefill weights on D nodes instead of freeing | D-node local-prefill paths need it (issue #11882); memory for stability |
| [`enable_cpu_binding`](flags/enable-cpu-binding.md) | Ascend CPU binding on ARM servers | Widely enabled on both sides in official PD recipes |
| [`profiling_chunk_config`](flags/profiling-chunk-config.md) | Dynamic chunked pipeline parallelism | Requires PP>1; GLM5.2 evidences P node; incompatible with DyntraLB/balanced scheduling |
| ~~enable_context_parallel~~ / ~~enable_dsa_cp~~ | Removed | Superseded by PCP (enabling dsa_cp on main errors with a PCP hint) |

## 6. KV Reuse & Pooling { #t-kvp }

Two ways to "stop paying recompute for KV": **KVPP** splits redundant per-layer MLA/SFA KV across TP ranks within one node (same memory, longer context); **KV pooling** (Ascend Store) shares KV across nodes. Note pooling is **not an additional-config flag** — its entry is `--kv-transfer-config`.

| Flag | One-liner | When to enable |
|---|---|---|
| [`enable_kvpp`](flags/enable-kvpp.md) | KV layer-wise parallelism across TP ranks | **Prefill node only** (official); requires PIECEWISE graph mode |
| [`kv_pool_range_debug`](flags/kv-pool-range-debug.md) | Audit logging for KV pool layer-wise transfers | Debug only; keep off in normal runs |

Pooling config → [Engine args overview · KV pooling topic](engine-args/index.md) · official [KV Cache Pool](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_pool_ascend_store.html)

## 7. Speculative Decoding { #t-spec }

A small draft model predicts tokens that the large model verifies in one pass — trading acceptance rate for decode speed. This family governs **dynamic speculation** (adaptive draft length by load) and **draft KV sliding window** (draft attends to only the last N tokens).

| Flag | One-liner | When to enable |
|---|---|---|
| [`dynamic_spec_config`](flags/dynamic-spec-config.md) | Dynamic speculative decoding config | Fluctuating load where adaptive draft length pays off |
| [`draft_window_size`](flags/draft-window-size.md) | Draft KV sliding window (draft sees last N tokens) | Long context + eagle3/dflash paths; output quality unchanged |

Related engine arg: [--speculative-config](engine-args/speculative-config.md) · official [speculative decoding guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/speculative_decoding.html)

## 8. Stability & Monitoring: Runtime Guard { #t-guard }

vLLM-Ascend's **online anomaly detection and incident-response layer**: it watches decode-time signals (token repetition, garbled text, non-finite logits, speculative acceptance-rate drift, etc.), writes structured reports on trigger, and can optionally dump request-level KV cache blocks. Everything is off by default with negligible overhead; open switches level by level when investigating.

| Flag | One-liner | When to enable |
|---|---|---|
| [`runtime_config`](flags/runtime-config.md) | Startup overlay layer for runtime config | Tune detectors/dump quotas online |
| [`runtime_config_path`](flags/runtime-config-path.md) | Runtime Guard JSON path | Config not at the default location |
| [`runtime_config_hot_reload`](flags/runtime-config-hot-reload.md) | Hot-reload runtime config | Change config without restart |
| [`dump_config`](flags/dump-config.md) | Inline msprobe dump config | Integrating the msprobe debugger |
| [`dump_config_path`](flags/dump-config-path.md) | msprobe dump config file path | Legacy option |
| [`msmonitor_use_daemon`](flags/msmonitor-use-daemon.md) | msmonitor daemon mode | Per monitoring deployment needs |
| [`ascend_log_path`](flags/ascend-log-path.md) | vLLM-Ascend log path | Default `~/ascend/log/vllm_ascend` |

## 9. Training & RL { #t-rl }

RL training (rollout inference + weight sync) needs special inference-side cooperation. This family covers **one-shot RL mode** (force-disables inference-time optimizations, sets dev mode), **global config refresh** (reset Ascend config in training loops), and the **rejection sampler** (block/entropy two-level verification).

| Flag | One-liner | When to enable |
|---|---|---|
| [`rl_config`](flags/rl-config.md) | One-shot RL mode master switch | When wiring RL training frameworks; forces weight_nz_mode=0 etc. |
| [`refresh`](flags/refresh.md) | Refresh global Ascend config | RLHF training loops / test cases resetting config each iteration |
| [`rejection_sampler_config`](flags/rejection-sampler-config.md) | Rejection sampler (block / entropy verify) | RL rollout sampling quality filtering |

Related engine args: RL family (`--weight-transfer-config` etc.) in [engine args overview](engine-args/index.md) · official [RL guide](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html)
