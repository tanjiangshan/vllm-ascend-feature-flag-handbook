---
title: kv-transfer-config
---

# `--kv-transfer-config`

> KV 传输配置（JSON），PD 分离（Prefill/Decode 分离）架构的核心参数。

| 属性 | 值 |
|---|---|
| 类型 | `KVTransferConfig`（JSON） |
| 默认值 | `None`（不启用） |
| 分类 | KV 传输与 PD 分离 |

## 官方定义

The config corresponding to the KV transfer... define the KV connector and its transport properties.（vLLM 源码 `KVTransferConfig`）

## Ascend 语境与官方用法

- 官方教程使用的 KV connector（按出现频率）：
  | Connector | 出处 |
  |---|---|
  | `MooncakeConnectorV2` | [PD 分离 Mooncake 教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) 等，当前主推 |
  | `MooncakeConnectorV1` | 早期 Mooncake 部署 |
  | `AscendStoreConnector` | Ascend 原生 KV 池方案 |
  | `MultiConnector` | 多 connector 组合 |
- 典型 PD 部署中，prefill/decode 节点分别配置不同角色，并常配 `--no-enable-prefix-caching`（见 [`enable-prefix-caching`](enable-prefix-caching.md)）。
- 与 PCP 组合仅 `MooncakeConnectorV1/V2` 全兼容（官方兼容性矩阵）。

## 用法

```bash
# decode 节点示例（简化自官方教程）
vllm serve Qwen/Qwen3-8B \
  --kv-transfer-config '{"kv_connector":"MooncakeConnectorV2","kv_role":"kv_consumer",...}' \
  --no-enable-prefix-caching
```

## 相关参数

- [`--enable-prefix-caching`](enable-prefix-caching.md) — PD 下显式关闭
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) — 长上下文 PD
- Ascend PD 专属开关：[`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md)、[`dyntra_lb_config`](../flags/dyntra-lb-config.md)
