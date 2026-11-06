---
title: kv-transfer-config
---

# `--kv-transfer-config`

> KV 传输配置（JSON）——PD 分离（Prefill/Decode 分离）架构的核心参数：KV 在节点间怎么传。

| 属性 | 值 |
|---|---|
| 类型 | `KVTransferConfig`（JSON） |
| 默认值 | `None`（不启用） |
| 分类 | KV 传输与 PD 分离 |

## 官方定义

> The config corresponding to the KV transfer... defines the KV connector and its transport properties.

（vLLM 源码：`KVTransferConfig`，[config/kv_transfer.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/kv_transfer.py)）

## 机制详解

**PD 分离是什么**：把 prefill（长计算）和 decode（长生成）拆到不同节点池。prefill 节点算完一条请求的整条 KV，**通过 KV 传输层把 KV 送给 decode 节点**，decode 节点接上继续生成。两池各自按负载弹性伸缩。

**本参数的角色**：告诉引擎"本节点是 KV 的生产者还是消费者、用什么 connector、走什么传输"。关键 JSON 字段（官方教程实证）：

| 字段 | 作用 |
|---|---|
| `kv_connector` | connector 实现（见下表） |
| `kv_role` | 本节点角色：`kv_producer`（prefill 侧）/ `kv_consumer`（decode 侧） |

**官方教程使用的 connector**（按出现频率）：

| Connector | 出处 |
|---|---|
| `MooncakeConnectorV2` | [PD 分离 Mooncake 教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) 等，当前主推 |
| `MooncakeConnectorV1` | 早期 Mooncake 部署 |
| `AscendStoreConnector` | Ascend 原生 KV 池方案 |
| `MultiConnector` | 多 connector 组合 |

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--enable-prefix-caching`](enable-prefix-caching.md) | **PD 下显式关闭**（`--no-enable-prefix-caching`，官方教程做法）——前缀复用语义由传输层接管 |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | 仅 MooncakeConnectorV1/V2 与 PCP 全兼容（官方矩阵） |
| [`--block-size`](block-size.md) | KV 块布局需与传输层对齐 |
| Ascend [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md) / [`dyntra_lb_config`](../flags/dyntra-lb-config.md) | PD 场景的重算调度与动态负载均衡 |

**类比**：PD 分离像"中央厨房 + 前店"——厨房（prefill 池）统一把菜做到半熟（KV 算好），本参数就是冷链物流协议（哪个仓库、用什么车、送到哪个门店），门店（decode 池）只管最后出餐。

## Ascend 语境与官方用法

- 官方 PD 教程普遍预置环境变量（如 Mooncake 地址、本地 KV 池路径）后传本参数；单节点 Mooncake 教程与多节点教程的命令均可在[部署配方](../recipes/features.md)页逐字查看。
- 与 PCP 组合时，connector 选型受限（上表），升级 vllm-ascend 版本后应重新核对兼容性。

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
- [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md) — Ascend PD 重算调度
