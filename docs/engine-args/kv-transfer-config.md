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
| `AscendStoreConnector` | Ascend 原生 KV 池化方案（KV Cache Pool / Ascend Store） |
| `MultiConnector` | 多 connector 组合 |

## KV 池化（Ascend Store）

**KV 池化**（KV Cache Pool / Ascend Store）是 vLLM-Ascend 提供的**跨节点 KV 缓存池化存储**特性：把 KV cache 写入外部存储后端，配合 PD 分离架构在多个 vLLM 实例间共享复用 KV，避免相同前缀的重复 prefill 计算。它的配置入口就是本参数的 `AscendStoreConnector`，**不是 `additional_config` 开关**——所以在特性开关总览里搜不到「池化」，属于正常现象。

| 后端 | 选型场景（官方文档） |
|---|---|
| Mooncake | 默认后端；需要 SSD Offload 扩容 KV 容量或多租户配额管理时选它 |
| Memcache | 基于 MemFabric；A3 HCCS 高速互联低延迟传输、或需要逐层 KV 传输（`use_layerwise`）时选它 |
| Yuanrong | 基于 openyuanrong-datasystem；多机部署、Remote H2D 传输、openEuler 生态集成时选它 |

**关键约束**（官方特性页）：

- 自 vLLM-Ascend **v0.23.0** 起支持；硬件 A2 / A3 / 950PR&950DT；
- `use_layerwise` 逐层传输**仅支持 Mooncake / Memcache 后端的 prefill 节点**；
- `kv_load_failure_policy=recompute` 暂不支持混合注意力模型（如 DeepSeekV4、Qwen 3.5）；
- Mooncake 后端需 >= 0.3.11.post1（逐层传输需 >= 0.3.14）；Memcache 后端需 `memfabric-hybrid` / `memcache-hybrid` >= 1.3.0；
- 与 [`enable_kvpp`](../flags/enable-kvpp.md) 可组合（KV 池化按 `kv_role` 选 `kv_producer` / `kv_both` + 整块加载）；Mooncake 分层池化（`backend="mooncake"` + `use_layerwise=true`）为 Experimental。

官方详情：[KV Cache Pool (Ascend Store)](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_pool_ascend_store.html) · [Mooncake 分层池化适配与优化](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/mooncake_layerwise_adaptation_and_optimization.html)

## 参数联动

| 联动对象 | 关系 |
|---|---|
| [`--enable-prefix-caching`](enable-prefix-caching.md) | **PD 下显式关闭**（`--no-enable-prefix-caching`，官方教程做法）——前缀复用语义由传输层接管 |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | 仅 MooncakeConnectorV1/V2 与 PCP 全兼容（官方矩阵） |
| [`--block-size`](block-size.md) | KV 块布局需与传输层对齐 |
| Ascend [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md) / [`dyntra_lb_config`](../flags/dyntra-lb-config.md) | PD 场景的重算调度与动态负载均衡 |

**类比**：PD 分离像"中央厨房 + 前店"——厨房（prefill 池）统一把菜做到半熟（KV 算好），本参数就是冷链物流协议（哪个仓库、用什么车、送到哪个门店），门店（decode 池）只管最后出餐。

## Ascend 语境与官方用法

- 官方 PD 教程普遍预置环境变量（如 Mooncake 地址、本地 KV 池路径）后传本参数；逐字命令与环境变量说明见官方教程（[Mooncake 单节点部署](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html)）。
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
