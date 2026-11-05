---
title: eplb_config
---

# `eplb_config`

> EPLB（Expert Parallelism Load Balancer，专家并行负载均衡）的完整配置入口。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |
| 适用 | MoE 模型；A2（`num_redundant_experts` 必须为 0）/ A3 |

## 三种模式总览

| 模式 | 关键子键 | 说明 | 详情 |
|---|---|---|---|
| 动态 EPLB | `dynamic_eplb: true` | 运行时自动均衡专家热点 | [dynamic_eplb](dynamic-eplb.md) |
| 录制 | `expert_map_record_path` | 录制专家映射供后续静态加载 | [dynamic_eplb](dynamic-eplb.md) |
| 静态 EPLB | `expert_map_path` | 加载预录制映射，无运行时开销 | 本文「静态模式」 |

动态与录制模式还需环境变量 `DYNAMIC_EPLB=true`（或 `EXPERT_MAP_RECORD=true`）作为安全防护。

## 子键速查

| 子键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `dynamic_eplb` | bool | `false` | 开启动态均衡 |
| `expert_map_path` | str | — | 静态映射文件路径 |
| `expert_map_record_path` | str | — | 录制输出路径 |
| `expert_heat_collection_interval` | int | `600` | 热度收集间隔 |
| `algorithm_execution_interval` | int | `50` | 均衡算法执行间隔 |
| `eplb_policy_type` | int | `2` | 策略类型（当前推荐 2 = SwiftBalanceEplb） |
| `num_redundant_experts` | int | `0` | 冗余专家数；**A2 上必须为 0** |
| `eplb_heat_collection_stage` | str | `"all"` | 热度统计阶段：`all` / `prefill` / `decode` |

## 静态模式用法

```bash
# 先用录制模式生成映射（需 DYNAMIC_EPLB=true 或 EXPERT_MAP_RECORD=true）
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"eplb_config": {"expert_map_record_path": "/data/expert_map.json"}}'

# 再用静态模式加载（无需环境变量，适合生产）
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"eplb_config": {"expert_map_path": "/data/expert_map.json"}}'
```

## 互斥

- [`enable_force_eplb`](enable-force-eplb.md) 与 `eplb_config.dynamic_eplb` **互斥**，同时设置启动报错。

## 相关开关

- [dynamic_eplb](dynamic-eplb.md) — 动态模式详解
- [enable_force_eplb](enable-force-eplb.md) — 性能上限测量（分析用）
