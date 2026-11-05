---
title: 版本历史
---

# 版本历史

记录特性开关的引入、默认值变更、弃用与移除。数据维护在各 flag 的 `data/flags/*.yaml` 中（`status` / `version_support` / `version_note` 字段），本页汇总版本级的大事件。

> 核验来源：各 release tag 的 `vllm_ascend/envs.py` 与 `vllm_ascend/ascend_config.py` 逐一比对，详见[版本支持矩阵](version-matrix.md)。

## v0.23.0（较早的稳定版）

- 存在一批纯环境变量 / 顶层键形式的开关（如 `VLLM_ASCEND_ENABLE_MATMUL_ALLREDUCE`、`enable_flashcomm2_parallel_size`）；
- `scheduler_config` 规范层级尚未建立，调度类开关多为顶层键或环境变量。

## v0.30.0（当前稳定版，变化最大）

**新增 14 个开关**：

- 调度体系：`scheduler_config`（规范层级）、`short_request_first_config`、`batch_job_sched_config`、`dyntra_lb_config`
- MoE 通信：`mc2_comm_alg`（取代 `enable_mc2_hierarchy_comm`）、`combine_quant_mode`
- RL：`rl_config`、`rejection_sampler_config` 相关能力
- 其他：`ascend_warmup_config`、`dynamic_spec_config`、`enable_force_eplb`、`enable_pcp_o_proj_weight_sharding`、`enable_pcp_embedding_lmhead_weight_sharding`、`kv_pool_range_debug`、`mlapo_keep_prefill_weights`

**移除 4 个开关**：

| 移除的开关 | 说明 |
|---|---|
| `enable_matmul_allreduce` | v0.23.0 仅环境变量形式，无直接替代 |
| `enable_flashcomm2_parallel_size` | FlashComm2 配置，无直接替代 |
| `multistream_overlap_gate` | 门控多流重叠；共享专家优化见 `multistream_overlap_shared_expert` |
| `weight_prefetch_config` | 权重预取；可关注 `ascend_warmup_config` |

**取代关系**：

- `enable_context_parallel`（v0.18 及更早的环境变量）→ `enable_dsa_cp` / PCP 方案。

## main（开发分支，下一版本）

- 新增 Runtime Guard 启动配置：`runtime_config`、`runtime_config_path`、`runtime_config_hot_reload`；
- 环境变量继续收敛：main 分支 `envs.py` 中 PR #9064 的迁移期环境变量已基本清理完毕（详见[版本支持矩阵](version-matrix.md)）。

## 历史事件

| 时间 | 事件 |
|---|---|
| 2026-05 | [PR #9064](https://github.com/vllm-project/vllm-ascend/pull/9064) 启动 10+ 个环境变量向 `--additional-config` 的迁移（过渡期双轨支持） |
| 后续 | `scheduler_config` 成为调度器配置的规范层级；`VLLM_ASCEND_KVPOOL_RANGE_DEBUG` 迁移至 `kv_pool_range_debug` |
| 计划中 | 根据 [issue #10381](https://github.com/vllm-project/vllm-ascend/issues/10381)，迁移期环境变量将彻底移除（main 分支已基本完成） |

## 如何补充本页

1. 在 `data/flags/<key>.yaml` 更新 `status` / `version_support` / `version_note`；
2. 在本表新增一行版本记录，注明来源（release tag 比对或 PR 号）；
3. 若变更影响默认值或语义，在对应详情页增加"变更历史"小节。
