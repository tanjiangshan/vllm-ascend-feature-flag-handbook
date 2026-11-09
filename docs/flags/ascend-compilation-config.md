---
title: ascend_compilation_config
---

# `ascend_compilation_config`

> Ascend 图编译配置。typed 为 `AscendCompilationConfig`（pydantic dataclass，`extra="forbid"`），控制 npugraph_ex 后端、static/super kernel 与编译期融合 pass。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}`（各子键取类内默认） |
| 状态 | ✅ active |

## 子键

| 子键 | 类型 | 默认值 | 说明 | 版本 |
|---|---|---|---|---|
| `enable_npugraph_ex` | bool | `true` | npugraph_ex 后端：Dynamo 产出的 Fx 图交由 npugraph_ex 优化编译 | 全版本 |
| `enable_static_kernel` | bool | `false` | 静态 kernel：图捕获期按当前 batch_size 编译对应形状的算子二进制，**编译耗时增加**；适合形状纯静态或变化小的场景，可提升网络性能 | 全版本 |
| `enable_super_kernel` | bool | 跟随 `enable_static_kernel` | Super Kernel 优化；缺省时继承 `enable_static_kernel`，可显式设置覆盖。**要求 static kernel 开启** | v0.30.0 起 |
| `fuse_norm_quant` | bool | `true` | norm + quant 融合 pass | 全版本 |
| `fuse_qknorm_rope` | bool | `true` | qknorm + rope 融合 pass。环境无 Triton 时置 `false` | 全版本 |
| `fuse_muls_add` | bool | `true` | muls + add 融合 pass | v0.30.0 起 |
| `fuse_allreduce_rms` | bool | `false` | allreduce + addrmsnorm 融合 pass | 仅 v0.23.0 |

子键表语义综合自 [官方 additional_config 文档](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/additional_config.html)与三个版本 tag 的 `AscendCompilationConfig` 类体。

## 依赖链与降级

```
enable_super_kernel → 要求 enable_static_kernel → 要求 enable_npugraph_ex
```

- v0.30.0 起为硬断言（`assert`）：只开 `enable_super_kernel` 不开 `enable_static_kernel` 会启动失败。
- **缺省继承**：只设 `enable_static_kernel: true` 时，`enable_super_kernel` 自动跟随为 `true`（model_validator 在 pydantic 校验前补齐）；想只开 static 不开 super 要显式写 `"enable_super_kernel": false`。
- **硬件降级**：硬件 profile 不支持 NPUGRAPH_EX 时（如 v0.23.0 的 310P），三个 kernel 开关全部自动置 `false` 并打 warning，不会报错。

## 官方用法

[Qwen3.8-Flash-Next 教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.8-Flash-Next.html)的推荐配置（多处方出现）：

```json
"ascend_compilation_config": {
  "fuse_norm_quant": false,
  "enable_npugraph_ex": true,
  "enable_static_kernel": true,
  "enable_super_kernel": false
}
```

注意该配方显式关掉 super kernel——static 已按 batch_size 编译，super 的额外优化对这些模型未必划算，以官方教程为准。

## 用法

```bash
vllm serve Qwen/Qwen3-8B \
  --additional-config='{"ascend_compilation_config": {"enable_static_kernel": true, "enable_super_kernel": false}}'
```

## 相关开关

- [`ascend_fusion_config`](ascend-fusion-config.md) — 融合算子开关（GMMSwiGLUQuant 等，与编译 pass 不同层）
- [`compilation-config`](../engine-args/compilation-config.md) — vLLM 顶层的 torch.compile / cudagraph 参数（`--compilation-config`），与本开关互补
