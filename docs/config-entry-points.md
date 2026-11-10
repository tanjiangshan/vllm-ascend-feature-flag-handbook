---
title: Ascend 配置入口总览
---

# Ascend 配置入口总览

> vLLM-Ascend 的配置**不止 `--additional-config` 一处**。本页把全部 6 类入口放在一张地图里：每类讲清"是什么、谁在读、典型键、容易踩的坑"，细节深入对应专页。

## 入口地图

| # | 入口 | 形态 | 谁在读 | 深入 |
|---|---|---|---|---|
| 1 | vLLM 顶层 CLI 参数 | `--key val` | vLLM 引擎（跨平台） | [引擎参数总览](engine-args/index.md) |
| 2 | `--additional-config` JSON | `'{"key": val}'` | Ascend 插件（`AscendConfig`） | [特性开关总览](flags/index.md) |
| 3 | CLI 值域的 Ascend 补丁 | 同 #1 参数的 Ascend 扩展取值 | Ascend 平台补丁 | [下文 §3](#3-cli-值域的-ascend-补丁) |
| 4 | `--kv-transfer-config` 的 connector 字段 | 嵌套 JSON | Ascend connector 实现 | [kv-transfer-config 详情页](engine-args/kv-transfer-config.md) |
| 5 | 环境变量 | `export X=y` | 构建脚本 / 运行时 | [环境变量](env-vars.md) |
| 6 | `runtime_config.json` 文件 | JSON(C) 文件 | Runtime Guard | [下文 §6](#6-runtime_configjson-runtime-guard) |

六类入口并非互斥：同一个参数可能同时是 #1 和 #3（补丁扩了它的值域），`runtime_config` 的启动键走 #2、内容走 #6。下文在每个交叉处标明。

## 1. vLLM 顶层 CLI 参数（跨平台引擎参数）

`vllm serve --max-num-seqs 256 --kv-cache-dtype fp8 ...`——vLLM 主仓定义的命令行参数，CUDA/ROCm/NPU 通用，由 vLLM 引擎本体校验和消费。

- 手册收录 78 个：**在 vLLM-Ascend 官方教程命令行中实证出现** + vLLM 源码 CLI 定义存在。
- 注意：部分参数的取值会被 Ascend 插件二次消费，派生出 #2 的开关（见 [kv-cache-dtype](engine-args/kv-cache-dtype.md) 页）——所以引擎参数页与特性开关页互有交叉链接。
- 典型例子：`--compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'`——PD 分离 D 节点只给 decode 录图的官方主流配方，深入见 [compilation-config 详情页](engine-args/compilation-config.md)。

## 2. `--additional-config` JSON（AscendConfig 特性开关）

`vllm serve --additional-config '{"enable_kvpp": true, "eplb_config": {...}}'`——Ascend 插件自己的配置键，定义在 `vllm_ascend/ascend_config.py` 的 `AscendConfig` 中，**仅 Ascend 有**，经 pydantic 校验（`extra="forbid"`，写错键名直接报错）。

- 手册收录 64 个，按状态（active/deprecated/removed/planned）与版本支持（v0.23.0/v0.30.0/main）整理。
- 三个 Runtime Guard 启动键（`runtime_config` / `runtime_config_path` / `runtime_config_hot_reload`）也走这里，但它们的**内容**在 #6 的文件里。

## 3. CLI 值域的 Ascend 补丁

最容易漏的一类：vLLM-Ascend **不新增 CLI 参数**，而是给既有参数**扩合法取值**（`vllm_ascend/patch/platform/` 在平台激活时打补丁）。

| 参数 | 上游合法值 | Ascend 补丁追加 | 用途 |
|---|---|---|---|
| `--kv-cache-dtype` | auto / fp8 / fp8_e5m2 / bf16 / fp16 … | `int8`、`mxfp8` | `int8`：DeepSeek V4 类稀疏 MLA 模型的 KV cache；`mxfp8`：A5 QFA 路径的 C8-MXFP 布局（FP8 KV + E8M0 scales） |
| `--attention_config.indexer_kv_dtype` | auto / bf16 / fp8 / mxfp4 / nvfp4 | `int8` | DeepSeek V4 的 indexer K cache |

**坑**：光看 vLLM 官方文档不知道这些值合法——校验在被补丁重建的 pydantic Literal 里。官方 GLM5/5.2 教程里的 `--kv-cache-dtype int8 --attention_config.indexer_kv_dtype int8` 就是补丁值域的实证。

细节见 [kv-cache-dtype 详情页](engine-args/kv-cache-dtype.md) 与 [enable_sparse_li_c8](flags/enable-sparse-li-c8.md) / [enable_sparse_sfa_c8](flags/enable-sparse-sfa-c8.md)。

## 4. `--kv-transfer-config` 的 connector 字段

PD 分离的 KV 传输配置本身是 #1 的 CLI 参数，但**值里的 connector 字段是 Ascend 实现**：

- `AscendStoreConnector`：`backend`（mooncake/memcache/yuanrong）、`use_layerwise`、`lookup_rpc_port` —— KV 池化入口
- `MooncakeConnectorV2`：`use_ascend_direct`、prefill/decode 拓扑声明
- `MultiConnector`：把多个 connector 组合（P2P 传输 + 池化写入）

字段级拆解见 [kv-transfer-config 详情页](engine-args/kv-transfer-config.md) 的「KV 池化」专节。

## 5. 环境变量

两类：

- **运行时**：`VLLM_ASCEND_ENABLE_BATCH_MEMCPY`（无 additional-config 对应键，只能走环境变量）、`DYNAMIC_EPLB`、`EXPERT_MAP_RECORD`
- **构建期**：`COMPILE_CUSTOM_KERNELS`、`MAX_JOBS`、`SOC_VERSION`、`ASCEND_HOME_PATH`、`HCCL_SO_PATH` 等

完整清单见 [环境变量](env-vars.md)。判断准则：**配置有 additional-config 键就不用环境变量**；环境变量只覆盖没有键的开关与构建行为。

## 6. `runtime_config.json`（Runtime Guard）

vLLM-Ascend 的**在线异常检测与事故响应层**：监视 decode 期信号（token 重复、乱码、非有限 logits、投机接受率漂移等），触发时写结构化报告（`runtime/report/`）并可选 dump 请求级 KV cache 块（`dump_kv`）。

- **内容走文件**：默认 `<cwd>/runtime/config/runtime_config.json`，支持 JSONC 注释；顶层键 `actions` / `dump` / `ascend_log` / `report` / `detector`
- **启动键走 #2**：`runtime_config_path`（改路径）、`runtime_config_hot_reload`（启动时热重载）、`runtime_config`（启动叠加层，会**覆盖**已有文件——先启动再手改文件，或全部走叠加）
- 默认部署 detectors off、hot-reload off，开销可忽略

官方文档：[Runtime Guard](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/runtime_guard.html) · [runtime_config JSON schema](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/runtime_config.html)。相关开关：[runtime_config](flags/runtime-config.md)、[runtime_config_path](flags/runtime-config-path.md)、[runtime_config_hot_reload](flags/runtime-config-hot-reload.md)。

## 怎么选入口

| 你想配的东西 | 走哪个入口 |
|---|---|
| 并发、并行、显存、量化等通用行为 | #1 CLI 参数 |
| Ascend 专属功能（KVPP、EPLB、RL 模式…） | #2 additional-config |
| 稀疏模型 KV 量化取值（int8/mxfp8） | #1 + #3（补丁值域） |
| PD 分离 / KV 池化传输 | #1 的 `--kv-transfer-config` + #4 connector 字段 |
| 没有对应键的编译/运行时开关 | #5 环境变量 |
| 线上质量监控与事故 dump | #6 runtime_config.json |
