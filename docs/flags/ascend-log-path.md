---
title: ascend_log_path
---

# `ascend_log_path`

> vLLM-Ascend 日志输出路径。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `~/ascend/log/vllm_ascend` |
| 状态 | ✅ active |
| 适用 | 全部 |

## 用法

```bash
vllm serve <model> \
  --additional-config='{"ascend_log_path": "/var/log/vllm-ascend"}'
```

## 注意事项

- 仅控制 vLLM-Ascend 侧日志；vLLM 主日志、CANN 驱动日志另有路径。
- 目录不存在时会自动创建；多节点部署建议统一挂载到共享存储便于排查。

## 相关开关

- [`ascend_compilation_config`](ascend-compilation-config.md) — Ascend 编译配置
- [`runtime_report_dir`](runtime-report-dir.md) — 报告根目录（已移除，见 runtime_config.report_dir）
