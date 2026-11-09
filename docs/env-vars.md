---
title: 环境变量
---

# 环境变量

除正在迁移的 10+ 个开关外（见[迁移对照表](migration.md)），以下环境变量**仍作为独立入口生效**，暂无迁移计划。

## 运行时环境变量

| 环境变量 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `VLLM_ASCEND_ENABLE_BATCH_MEMCPY` | `"1"` / `"0"` / 未设置 | 未设置（自动） | 控制 KV cache 卸载的 `aclrtMemcpyBatchAsync` 编译路径。`"1"` 强制启用，`"0"` 强制禁用，未设置则按 CANN 头文件自动检测。**注意**：没有对应的 `--additional-config` 键，只能用环境变量。 |
| `DYNAMIC_EPLB` | `"true"` / `"false"` | `"false"` | 动态 EPLB 的安全防护开关。仅在配置中也设置 `dynamic_eplb: true` 或录制模式时生效。详见 [`dynamic_eplb`](flags/dynamic-eplb.md) |
| `EXPERT_MAP_RECORD` | bool | 未设置 | EPLB 录制模式开关：录制专家映射并保存至 `expert_map_record_path` |
| `HCCL_SO_PATH` | 路径 | 未设置（`libhccl.so`） | pyhccl 通信后端使用的 HCCL 库路径。仅在使用 pyhccl 后端时需要显式指定 |

## 构建期环境变量

以下变量影响**源码编译**，不影响运行时行为，完整列表见[官方构建文档](https://docs.vllm.ai/projects/ascend/en/latest/installation/ascend.html)：

| 环境变量 | 默认值 | 说明 |
|---|---|---|
| `COMPILE_CUSTOM_KERNELS` | `1` | 是否编译自定义算子。无 NPU 环境跑单测时置 `0` |
| `MAX_JOBS` | CPU 核数 | 编译并行度 |
| `SOC_VERSION` | 自动检测 | 芯片版本，构建期通过 `npu-smi` 自动查询 |
| `ASCEND_HOME_PATH` | `/usr/local/Ascend/ascend-toolkit/latest` | CANN 工具包路径 |
| `VERBOSE` | `"0"` | 编译期详细日志开关，置 `1` 输出更多编译日志 |
| `CMAKE_BUILD_TYPE` | `Release` | CMake 构建类型：`Release` / `Debug` / `RelWithDebugInfo` |
| `C_COMPILER` | 系统默认 | C 编译器路径（源码编译自定义算子时指定） |
| `CXX_COMPILER` | 系统默认 | C++ 编译器路径（同上） |
| `VLLM_VERSION` | 未设置 | 源码安装 vLLM 时的版本覆写：本地源码装的 vLLM 版本号常与 PyPI 不一致，设此变量确保 vllm-ascend 依赖解析到正确版本（开发者场景） |

## 使用建议

- **部署配置优先用 `--additional-config`**：除上表"运行时环境变量"外，新配置一律走配置键，见[快速上手](quick-start.md)。
- **不要混用两种形式**：同一个开关同时以环境变量和配置键设置时，行为以源码实现为准（通常是配置键优先），混用会增加排查成本。
