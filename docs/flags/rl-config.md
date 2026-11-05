---
title: rl_config
---

# `rl_config`

> 一键 RL 模式总开关（v0.30.0 新增）。为 RLHF/训练-推理一体场景自动套用一组经过验证的固定行为。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active（v0.30.0 新增） |

## 子键

| 子键 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `enabled` | bool | `false` | RL 模式总开关；`false` 时其余子键全部忽略 |
| `sleep_mode_extra_cleanup` | bool | `false` | sleep 期间释放 HCCL 进程组 + 清理 ACL 图工作区，把更多 NPU 内存还给训练器，代价是唤醒延迟增加 |
| `enable_training_consistency` | bool | `false` | 启用训练-推理一致性 FA3 注意力后端；需要 `flash_attn_npu_v3` 包 |
| `enable_batch_invariant` | bool | `false` | 工作进程启动前设置 `VLLM_BATCH_INVARIANT=1`（批次不变确定性计算） |

## 启用时的固定行为（不可通过子键修改）

`rl_config.enabled = true` 时，vLLM-Ascend 每次初始化都会强制执行：

1. 刷新全局 Ascend 配置（等效 `refresh: true`）；
2. 强制 `weight_nz_mode = 0`（**优先于顶层 `weight_nz_mode` 配置**）；
3. 设置 `VLLM_SERVER_DEV_MODE=1`；
4. 从 `PYTORCH_NPU_ALLOC_CONF` 中移除 `expandable_segments` 条目。

## 批次不变性细节

`enable_batch_invariant = true` 时，工作进程侧的批次不变初始化会设置 `HCCL_DETERMINISTIC=strict` 和 `LCCL_DETERMINISTIC=1`。注意：

- 需要 `COMPILE_CUSTOM_KERNELS=1` 从源码构建 vllm-ascend；
- RL 模式已强制 `weight_nz_mode=0`，两者配合是批次不变的前提。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"rl_config": {"enabled": true, "sleep_mode_extra_cleanup": true}}'
```

## 相关开关

- [weight_nz_mode](weight-nz-mode.md) — RL 模式强制其为 0
- [refresh](refresh.md) — RL 模式隐式启用
- [VLLM_ASCEND_ENABLE_BATCH_MEMCPY](../env-vars.md) — KV cache offload 编译路径（环境变量）
