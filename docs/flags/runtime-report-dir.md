---
title: runtime_report_dir
---

# `runtime_report_dir`

> Runtime Guard 报告根目录覆盖。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（默认 `/runtime/report`） |
| 状态 | ✅ active |

## 说明

覆盖 Runtime Guard 的报告输出根目录。`runtime_dump_dir` 未显式设置时，dump 目录由本目录派生。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"runtime_report_dir": "/data/runtime/report"}'
```
