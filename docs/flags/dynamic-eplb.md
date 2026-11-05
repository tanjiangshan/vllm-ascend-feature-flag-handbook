---
title: dynamic_eplb
---

# `dynamic_eplb`

> 动态专家并行负载均衡（Dynamic EPLB）。MoE 模型在 expert 热点明显时的关键优化。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active |
| 嵌套位置 | `eplb_config.dynamic_eplb` |
| 安全防护 | 必须同时设置环境变量 `DYNAMIC_EPLB=true` |
| 适用 | MoE 模型；A2（`num_redundant_experts` 必须为 0）/ A3 |

!!! warning "双重开关缺一不可"
    仅在配置中设置 `eplb_config.dynamic_eplb: true` 是不够的——启动断言要求同时设置环境变量 `DYNAMIC_EPLB=true`（录制模式为 `EXPERT_MAP_RECORD=true`）。这是有意设计的安全防护。

## 用法

```bash
export DYNAMIC_EPLB=true
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"eplb_config": {"dynamic_eplb": true}}'
```

## 配套参数（`eplb_config` 内）

| 参数 | 默认值 | 说明 |
|---|---|---|
| `expert_heat_collection_interval` | `600` | 收集专家热度的间隔 |
| `algorithm_execution_interval` | `50` | 执行均衡算法的间隔 |
| `eplb_policy_type` | `2` | EPLB 策略类型（当前版本建议 SwiftBalanceEplb(2)） |
| `num_redundant_experts` | `0` | 冗余专家数量；**A2 上必须为 0** |
| `eplb_heat_collection_stage` | `"all"` | 热度收集的请求阶段：`all` / `prefill` / `decode` |

## 三种工作模式

| 模式 | 配置 | 环境变量 |
|---|---|---|
| 动态 EPLB | `dynamic_eplb: true` | `DYNAMIC_EPLB=true` |
| 录制（生成专家映射） | `expert_map_record_path` | `DYNAMIC_EPLB=true` 或 `EXPERT_MAP_RECORD=true` |
| 静态 EPLB（加载预录映射） | `expert_map_path` | 无需设置 |

## 互斥开关

- [`enable_force_eplb`](enable-force-eplb.md) 与本开关**互斥**，不可同时启用。

## 相关开关

- [`enable_force_eplb`](enable-force-eplb.md) — 仅用于性能分析上限测量的确定性路由
