---
title: 特性专题导览
---

# 特性专题导览

> 本页按**解决的问题**把 64 个特性开关归入 9 个专题：每个专题先讲原理（是什么、解决什么问题），再给成员速览表（一句话 + 何时开）。适合系统性学习；查单个参数仍去[特性开关总览](flags/index.md)，深入细节去各详情页。

## 1. MoE 通信与计算重叠 { #t-moe }

MoE 模型每层有两次集合通信：dispatch 把 token 按路由发到各专家，combine 把结果收回，通信量随 EP 规模线性增长，容易盖过计算成为瓶颈。这组开关围绕三件事：**融合**（把 dispatch/combine 合成一个算子）、**重叠**（用多余流把通信藏到计算背后）、**量化**（降低通信字节）。都是 MoE 模型（DeepSeek/GLM/Kimi 等）专属，CPU 密集场景无感。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`enable_fused_mc2`](flags/enable-fused-mc2.md) | 融合 MC2 dispatch/combine 算子（0 关 / 1 开 / 2 MegaMoE） | 官方模型配方默认开；A5 MegaMoE 需 SiTU 模型 |
| [`mc2_comm_alg`](flags/mc2-comm-alg.md) | dispatch/combine 通信算法（fullmesh/hierarchy/fullmesh_v2） | 跨机 MoE 按芯片选：hierarchy 仅 A2/A3，fullmesh_v2 仅 A3 |
| [`combine_quant_mode`](flags/combine-quant-mode.md) | combine 通信量化（如 4 = FP8） | 跨机 combine 带宽瓶颈时，按官方模型配方（DeepSeek-V4 D 节点） |
| [`enable_shared_expert_dp`](flags/enable-shared-expert-dp.md) | 共享专家在 TP rank 间以数据并行运行 | TP>1 且共享专家占比高；以更多显存换性能 |
| [`multistream_overlap_shared_expert`](flags/multistream-overlap-shared-expert.md) | 独立流重叠共享专家计算与通信 | 含共享专家的 MoE；TP=1 或开了 shared_expert_dp 时 |
| [`multistream_dsv4_dsa_overlap`](flags/multistream-dsv4-dsa-overlap.md) | DeepSeek V4 的 DSA 多流重叠 | 默认开；DSV4 模型自动生效 |
| [`multistream_engram_overlap`](flags/multistream-engram-overlap.md) | Engram 模块多流重叠 | 默认仅 A5 开；显式设置可覆盖 |
| [`enable_flashcomm1`](flags/enable-flashcomm1.md) | SP MoE 的 FlashComm1 通信优化 | 仅 Model Runner V1；MRv2 请改用 PCP |
| [`enable_prefill_mc2`](flags/enable-prefill-mc2.md) | 为 prefill 批次预留 MC2 token 容量 | P 节点（PD 分离）；官方注明的临时开关 |
| [`mix_placement`](flags/mix-placement.md) | DP×TP 平面专家混合放置策略 | 收发两端配置必须一致（RFork 权重传输指纹） |
| ~~enable_mc2_hierarchy_comm~~ | 已弃用 | 用 `mc2_comm_alg="hierarchy"` 取代 |
| ~~enable_matmul_allreduce~~ / ~~enable_flashcomm2_parallel_size~~ / ~~multistream_overlap_gate~~ | 已移除 | 见详情页/版本历史 |

## 2. 负载均衡与调度 { #t-scheduling }

专家并行的痛点是**路由不均**：热点专家排队、冷点专家闲置。这组开关覆盖四个层面：EP 权重均衡（EPLB）、PD 分离下的调度策略（重算/均衡/短请求优先）、批作业场景、RL 采样。多数据互斥——**启动时校验组合合法性**，配错会直接报错。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`eplb_config`](flags/eplb-config.md) | EPLB 均衡配置（dynamic_eplb / expert_map_record 等子键） | EP 部署默认关注；动态均衡需配 `DYNAMIC_EPLB=true` 环境变量 |
| [`enable_force_eplb`](flags/enable-force-eplb.md) | 强制确定性轮询专家路由 | **仅性能分析**——替换真实路由使结果无效，切勿生产 |
| [`scheduler_config`](flags/scheduler-config.md) | 调度扩展的规范聚合层 | v0.30.0 起各调度键统一收编于此 |
| [`recompute_scheduler_enable`](flags/recompute-scheduler-enable.md) | 重计算调度（请求回填时重算而非存 KV） | **仅 PD 分离 D 节点**；P 节点/混部开启会启动报错 |
| [`dyntra_lb_config`](flags/dyntra-lb-config.md) | DyntraLB 动态负载均衡 | **仅 PD 分离 D 节点**，DP>1；勿配 P 节点 |
| [`enable_balance_scheduling`](flags/enable-balance-scheduling.md) | 均衡调度 | **仅 PD 混部**（A3 单机/共置场景） |
| [`short_request_first_config`](flags/short-request-first-config.md) | 短请求优先 prefill 调度 | 普通部署 / PD 混部 / P 节点；**不支持 D 节点** |
| [`batch_job_sched_config`](flags/batch-job-sched-config.md) | batch 作业感知调度 | 批作业场景；不可与 ShortRequestFirst 组合 |
| ~~batch_job_sched_config 等旧顶层键~~ | v0.30.0 起收编 scheduler_config | 过渡期旧键仍可用但发弃用警告 |

官方功能页：[DyntraLB](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dyntra_lb.html) · [ShortRequestFirst](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/short_request_first.html) · [动态分块流水线](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/dynamic_chunk_pipeline_parallel.html)

## 3. KV Cache 量化与内存格式 { #t-kvfmt }

KV cache 是长上下文服务的第一显存消费者。这组开关管**布局**（NZ / T-major / 按块转置）、**量化**（C8 稀疏布局、int8/mxfp8——后者走 CLI 值域补丁）、**卸载**（稀疏 KV 下沉 DRAM），目标都是在不损精度（或少损）的前提下把 KV 显存砍下来。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`weight_nz_mode`](flags/weight-nz-mode.md) | 权重 NZ 格式（0 关 / 1 仅量化权重 / 2 含 BF16/FP16） | 按权重格式跟随官方模型配方 |
| [`enable_kv_nz`](flags/enable-kv-nz.md) | KV cache NZ 布局 | 仅 MLA 模型（DeepSeek 类） |
| [`enable_transpose_kv_cache_by_block`](flags/enable-transpose-kv-cache-by-block.md) | 按块转置 KV cache（融合算子路径） | 默认开；融合 attention 路径要求 |
| [`sparse_kv_offload_config`](flags/sparse-kv-offload-config.md) | 稀疏 KV 卸载到 DRAM | **勿配 P 节点**（官方明示）；D 节点按显存压力开 |
| ~~enable_sparse_li_c8~~ / ~~enable_sparse_sfa_c8~~ | 已移除 | v0.30.0 起由 `--attention_config.indexer_kv_dtype` / `--kv-cache-dtype` ∈ {fp8,int8} 自动派生 |
| ~~c8_enable_reshape_optim~~ / ~~hamming_sparse~~ | 已移除 | 见版本历史 |

相关引擎参数：[kv-cache-dtype 值域补丁](engine-args/kv-cache-dtype.md)（int8/mxfp8）

## 4. 图与编译 { #t-graph }

录图把一整步前向固化成一次图重放，砍掉 kernel launch 与 CPU 调度开销——decode 步（每序列仅 1 token）收益最大。这组开关分两层：**vLLM 层**（`--compilation-config`，跨平台）与 **Ascend 平台层**（本组开关，管 ACLGraph/Xlite 与算子融合）。最终图模式由平台代码裁决，两层别打架。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`ascend_compilation_config`](flags/ascend-compilation-config.md) | Ascend 图编译配置（enable_npugraph_ex 等子键） | 官方 PD 配方 D 侧常开 npugraph_ex；P 侧多跑 eager |
| [`xlite_graph_config`](flags/xlite-graph-config.md) | Xlite 图模式（full_mode 控制 prefill 是否入图） | 支持的模型按官方 graph_mode 指南 |
| [`ascend_fusion_config`](flags/ascend-fusion-config.md) | 融合算子配置（GmmSwigluQuant 等子键） | 按模型配方；默认子键多已开 |
| [`ascend_warmup_config`](flags/ascend-warmup-config.md) | 与权重加载重叠的启动预热 | 大模型缩短启动时间 |

相关引擎参数：[--compilation-config](engine-args/compilation-config.md)（cudagraph_mode 全取值） · 官方 [graph_mode 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/graph_mode.html)

## 5. PD 分离与并行 { #t-pd }

PD 分离把 prefill（算得慢、吃算力）与 decode（跑得快、吃带宽/显存）拆到不同节点，各自独立扩缩。这组开关管**长文本并行的两种形态**（PCP prefill 侧 / DCP decode 侧）、**细粒度 TP**（D 节点内存换并发）、**MLAPO 逐层并行**与 **CPU 绑定**。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`enable_pcp_embedding_lmhead_weight_sharding`](flags/enable-pcp-embedding-lmhead-weight-sharding.md) | PCP 组内 Embedding/LMHead 权重分片 | PCP>1 时默认开 |
| [`enable_pcp_o_proj_weight_sharding`](flags/enable-pcp-o-proj-weight-sharding.md) | PCP 组内 O 投影权重分片 | PCP>1 时默认开 |
| [`finegrained_tp_config`](flags/finegrained-tp-config.md) | 细粒度 TP（oproj/mlp/lmhead/embedding 独立 TP 度） | **仅 PD 分离 D 节点**（oproj/mlp>1 启动校验），配重算调度 + 预取卸载 |
| [`enable_mlapo`](flags/enable-mlapo.md) | MLAPO 逐层自适应并行优化 | **PD 场景仅 D 节点**（官方明示）；耗更多显存 |
| [`mlapo_keep_prefill_weights`](flags/mlapo-keep-prefill-weights.md) | D 节点保留 prefill 权重不释放 | D 节点本地 prefill 路径需要（issue #11882），以显存换稳定 |
| [`enable_cpu_binding`](flags/enable-cpu-binding.md) | ARM 服务器昇腾 CPU 绑定 | 官方 PD 配方 P/D 两侧普遍开启 |
| [`profiling_chunk_config`](flags/profiling-chunk-config.md) | 动态分块流水线并行 | 需 PP>1；GLM5.2 实证 P 节点；与 DyntraLB/均衡调度互斥 |
| ~~enable_context_parallel~~ / ~~enable_dsa_cp~~ | 已移除 | PCP 取代（main 上开 dsa_cp 会报错提示） |

## 6. KV 复用与池化 { #t-kvp }

两个"让 KV 不吃重复计算"的特性：**KVPP** 在单机内把 MLA/SFA 各层冗余 KV 分摊到 TP rank（等显存换更长上下文）；**KV 池化**（Ascend Store）跨节点共享 KV。注意池化**不是 additional-config 开关**，入口在 `--kv-transfer-config`。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`enable_kvpp`](flags/enable-kvpp.md) | KV 按层并行，TP rank 分摊 KV | **仅 P 节点**（官方明示）；要求 PIECEWISE 图模式 |
| [`kv_pool_range_debug`](flags/kv-pool-range-debug.md) | KV pool 逐层传输审计日志 | 仅调试时开，正常运行保持禁用 |

池化配置 → [引擎参数总览 · KV 池化专题](engine-args/index.md) · 官方 [KV Cache Pool](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_pool_ascend_store.html)

## 7. 投机解码 { #t-spec }

用小模型（草稿）先猜 token、大模型一次验证多 token，用验证通过率换 decode 加速。这组开关管**动态投机**（按负载自适应草稿长度）与**草稿 KV 滑窗**（草稿只看最近 N token 省显存）。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`dynamic_spec_config`](flags/dynamic-spec-config.md) | 动态投机解码配置 | 负载波动大、想自适应草稿长度的场景 |
| [`draft_window_size`](flags/draft-window-size.md) | 草稿 KV 滑窗（草稿只看最近 N token） | 长上下文 + eagle3/dflash 路径；输出质量不变 |

相关引擎参数：[--speculative-config](engine-args/speculative-config.md) · 官方[投机解码指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/speculative_decoding.html)

## 8. 稳定性与监控：Runtime Guard { #t-guard }

vLLM-Ascend 的**在线异常检测与事故响应层**：监视 decode 期信号（token 重复、乱码、非有限 logits、投机接受率漂移等），触发时写结构化报告并可选 dump 请求级 KV cache。默认全关、开销可忽略；出问题时再按开关逐级打开。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`runtime_config`](flags/runtime-config.md) | 运行时配置启动叠加层 | 需要在线调整检测器/dump 配额时 |
| [`runtime_config_path`](flags/runtime-config-path.md) | Runtime Guard JSON 路径 | 配置不放默认路径时 |
| [`runtime_config_hot_reload`](flags/runtime-config-hot-reload.md) | 配置热重载 | 想运行时改配置不重启用 |
| [`dump_config`](flags/dump-config.md) | 内联 msprobe dump 配置 | 对接 msprobe 调试器 |
| [`dump_config_path`](flags/dump-config-path.md) | msprobe dump 配置文件路径 | 兼容旧版选项 |
| [`msmonitor_use_daemon`](flags/msmonitor-use-daemon.md) | msmonitor 守护进程模式 | 按监控部署需要 |
| [`ascend_log_path`](flags/ascend-log-path.md) | vLLM-Ascend 日志路径 | 默认 `~/ascend/log/vllm_ascend` |

## 9. 训练与 RL { #t-rl }

RL 训练（rollout 推理 + 权重同步）需要推理侧的特殊配合：这组开关管**一键 RL 模式**（强制关闭推理期优化、设置开发模式）、**全局配置刷新**（训练循环里重置 Ascend 配置）、**拒绝采样器**（block/entropy 两级验证）。

| 开关 | 一句话 | 何时开 |
|---|---|---|
| [`rl_config`](flags/rl-config.md) | 一键 RL 模式总开关 | RL 训练框架接入时；enabled 时强制 weight_nz_mode=0 等 |
| [`refresh`](flags/refresh.md) | 刷新全局 Ascend 配置 | RLHF 训练循环 / 测试用例每次重置配置时 |
| [`rejection_sampler_config`](flags/rejection-sampler-config.md) | 拒绝采样器（block / entropy verify） | RL rollout 采样质量过滤 |

相关引擎参数：RL 类（`--weight-transfer-config` 等）见[引擎参数总览](engine-args/index.md) · 官方 [RL 指南](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html)
