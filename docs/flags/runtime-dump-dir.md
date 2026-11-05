---
title: runtime_dump_dir
---

# `runtime_dump_dir`

> KV dump 根目录设置。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None`（由报告根目录派生） |
| 状态 | ✅ active |

## 说明

设置 Runtime Guard 的 KV dump 根目录（对应 `dump.dump_dir`）。不设置时，dump 目录由 `runtime_report_dir` 派生。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"runtime_dump_dir": "/data/runtime/dump"}'
```
