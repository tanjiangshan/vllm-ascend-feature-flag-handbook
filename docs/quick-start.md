---
title: 快速上手
---

# 快速上手：`--additional-config`

vLLM-Ascend 的特性开关通过 vLLM 的 `--additional-config` 参数传入，值为一个 JSON 对象。

!!! warning "过渡期提醒"
    PR #9064 起，环境变量正在统一迁移至 `--additional-config`。过渡期两者均可用，但**新部署请使用 `--additional-config`**，环境变量将在未来版本移除。详见[迁移对照表](migration.md)。

## 在线服务（`vllm serve`）

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"enable_fused_mc2": 1, "weight_nz_mode": 2}'
```

## 离线推理（Python API）

```python
from vllm import LLM

llm = LLM(
    model="Qwen/Qwen3-8B",
    additional_config={
        "enable_fused_mc2": 1,
        "weight_nz_mode": 2,
    },
)
```

## 嵌套配置

部分开关是对象（dict）类型，例如调度器与 EPLB 配置：

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{
    "scheduler_config": {"enable_balance_scheduling": true},
    "eplb_config": {"dynamic_eplb": true}
  }'
```

!!! note "动态 EPLB 的特殊要求"
    `eplb_config.dynamic_eplb: true` 之外，还必须设置环境变量 `DYNAMIC_EPLB=true` 作为安全防护，否则启动断言会失败。详见 [`dynamic_eplb`](flags/dynamic-eplb.md)。

## 常见错误

| 错误 | 原因 | 修正 |
|---|---|---|
| `must be either '0' or '1'` | 布尔开关传了 `"true"`/`"1"` 以外的字符串 | 布尔开关在 JSON 中用 `true`/`false` |
| 配置未生效 | 键名拼错或层级错误 | 对照[总览表](flags/index.md)检查键名与嵌套层级 |
| 启动报配置冲突 | 同时设置了互斥开关（如 `enable_force_eplb` 与 `eplb_config.dynamic_eplb`） | 查看详情页的 `conflicts` 字段 |
| MRv2 下 `enable_flashcomm1` 报错 | FlashComm1 仅支持 Model Runner V1 | MRv2 请改用 PCP，见对应版本说明 |

## 下一步

- [特性开关总览](flags/index.md)：全量速查表
- [迁移对照表](migration.md)：环境变量 → 配置键对照
- [环境变量](env-vars.md)：仍生效的独立环境变量
