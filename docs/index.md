---
title: vLLM-Ascend 特性开关手册
hide:
  - navigation
---

<div class="hero" markdown>

# vLLM-Ascend 特性开关手册

**一份社区维护的 vLLM-Ascend 特性开关（Feature Flags）深度参考：**

`--additional-config` 全量配置 ｜ 环境变量 ｜ 迁移对照 ｜ 版本历史

</div>

## 这是什么？

vLLM-Ascend 通过**特性开关**控制大量实验性、场景化的优化能力：从 MoE 融合算子（MC2）、动态 EPLB，到权重量化 NZ 格式、均衡调度、RL 模式等。

官方文档将这些开关分散在多个页面中，且以简表为主。本手册尝试做到：

1. **全量**：收录 `--additional-config` 的每个配置键与仍生效的环境变量；
2. **可检索**：一张总表 + 按主题分组，每个开关独立成页；
3. **可追溯**：标注引入版本、迁移状态（PR #9064 环境变量迁移）、适用芯片；
4. **机器可读**：`docs/flags.json` 供脚本/工具直接消费。

!!! note "与官方文档的关系"
    本手册是**社区补充参考**，不替代[官方文档](https://docs.vllm.ai/projects/ascend/en/latest/)。发现与官方文档冲突时，以官方文档为准，并欢迎提 issue 修正本手册。

## 快速入口

<div class="grid cards" markdown>

-   :material-flag-outline:{ .lg .middle } **特性开关总览**

    ---

    64 个 vLLM-Ascend 专有开关：配置键 / 默认值 / 状态 / 版本支持

    [:octicons-arrow-right-24: 进入](flags/index.md)

-   :material-tune:{ .lg .middle } **引擎参数**

    ---

    78 个 `vllm serve` 参数的 Ascend 语境用法（官方教程实证）

    [:octicons-arrow-right-24: 进入](engine-args/index.md)

-   :material-table:{ .lg .middle } **版本支持矩阵**

    ---

    每个开关在 v0.23.0 / v0.30.0 / main 的支持情况

    [:octicons-arrow-right-24: 进入](version-matrix.md)

-   :material-swap-horizontal:{ .lg .middle } **迁移对照表**

    ---

    10 个环境变量 → `--additional-config` 的迁移速查

    [:octicons-arrow-right-24: 进入](migration.md)

-   :material-console:{ .lg .middle } **快速上手**

    ---

    `--additional-config` 在线/离线用法与常见错误

    [:octicons-arrow-right-24: 进入](quick-start.md)

-   :material-history:{ .lg .middle } **版本历史**

    ---

    各版本开关的引入、弃用与移除记录

    [:octicons-arrow-right-24: 进入](version-history.md)

</div>

## 常用开关 TOP 5

| 配置键 | 作用 | 默认值 |
|---|---|---|
| [`enable_fused_mc2`](flags/enable-fused-mc2.md) | MoE 融合 MC2 算子（性能关键） | `0` |
| [`weight_nz_mode`](flags/weight-nz-mode.md) | 权重 NZ 格式（量化模型性能） | `1` |
| [`enable_mlapo`](flags/enable-mlapo.md) | 模型逐层自适应并行优化 | `true` |
| [`scheduler_config`](flags/scheduler-config.md) | 调度器配置规范层级（v0.30.0 新增） | `{}` |
| [`rl_config`](flags/rl-config.md) | 一键 RL 模式（v0.30.0 新增） | `{}` |

## 贡献

本手册由社区维护，数据源是 [`data/flags/`](https://github.com/tanjiangshan/vllm-ascend-feature-flag-handbook/tree/main/data/flags) 下的 YAML 文件。修正一个默认值、补充一条风险提示、新增一个开关，都是受欢迎的贡献。详见[贡献指南](contributing.md)。
