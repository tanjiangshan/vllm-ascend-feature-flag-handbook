---
title: dump_config_path
---

# `dump_config_path`

> msprobe dump 配置文件路径。

| 属性 | 值 |
|---|---|
| 类型 | `str` |
| 默认值 | `None` |
| 状态 | ✅ active |

## 说明

指定外部 msprobe dump 配置文件的路径（兼容旧版选项）。与 [`dump_config`](dump-config.md)（内联字典）二选一。

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"dump_config_path": "/etc/vllm/msprobe_dump.json"}'
```
