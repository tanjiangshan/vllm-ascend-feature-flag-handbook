---
title: ascend_log_path
---

# `ascend_log_path`

> vLLM-Ascend 日志输出路径。
> 📚 所属专题：[8. 稳定性与监控：Runtime Guard](../feature-topics.md#t-guard)

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

<!-- DEPLOY_START -->
## 部署形态

> 混部 = PD 共置（colocated）或同机多实例共享 NPU；PD 分离 = P/D 节点经 KV 传输分离部署。「未见官方说明」≠ 不能开，仅表示官方文档未给出专门约束。

| 维度 | 结论 |
|---|---|
| 混部（colocated） | ◻️ 未见官方说明 |
| PD 分离 | ◻️ 未见官方说明 |

未见官方文档对本开关在混部（colocated）或 PD 分离部署下的专门说明；实践上可按全节点统一配置处理，欢迎补充实测结论。


<!-- DEPLOY_END -->

## 相关开关

- [`ascend_compilation_config`](ascend-compilation-config.md) — Ascend 编译配置
- [`runtime_report_dir`](runtime-report-dir.md) — 报告根目录（已移除，见 runtime_config.report_dir）
