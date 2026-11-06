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

### 典型池化配置拆解（PD 分离 + MemCache 池化）

> 官方 GLM5.2/5.3 教程的标准写法：`MultiConnector` 组合**点对点传输 + 池化写入**两个 connector。逐字段含义如下，逐字命令见[官方教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html)。

**顶层字段**

| 字段 | 含义 |
|---|---|
| `kv_connector: "MultiConnector"` | 组合器：把下面 `connectors` 列表里的多个 connector 绑成一份配置，同一份 KV 同时走多条路 |
| `engine_id` | 引擎实例编号，同机多引擎共存时区分（官方示例第二个 prefill 引擎用 `"1"`） |
| `kv_role: "kv_producer"` | 本节点角色：prefill 侧是生产者；decode 侧对应 `kv_consumer` |
| `kv_port` | 传输端口 |

**Connector ① `MooncakeConnectorV2`——P2P 传输（管"当下"：本条请求的 KV 送到 decode）**

| 字段 | 含义 |
|---|---|
| `use_ascend_direct: true` | 启用 Ascend 直传：KV cache 在 NPU 间直通，不经主机内存中转 |
| `prefill: {dp_size, pp_size, tp_size, pp_layer_partition}` | 声明 prefill 侧并行拓扑（如 `"42,36"` 表示 78 层按 PP 切两段），供 KV 按层映射 |
| `decode: {dp_size, tp_size}` | 声明 decode 侧拓扑，P/D 切分不同，KV 需按对端形状重切 |

**Connector ② `AscendStoreConnector`——池化写入（管"将来"：撞前缀的请求免算 prefill）**

| 字段 | 含义 |
|---|---|
| `backend: "memcache"` | 池后端选型：`memcache`（MemFabric 底座，A3 HCCS 低延迟场景）/ `mooncake` / `yuanrong` |
| `use_layerwise` | `false`=整块池化（本例）；`true`=逐层传输分层池化（GLM5.2 的 1M 长上下文变体，仅 Mooncake/Memcache 后端 prefill 节点） |
| `lookup_rpc_port` | 池化调度进程与 worker 间的本地 IPC 端点标识；共享同一 RPC 基目录的独立服务必须取不同值 |

**类比**：MultiConnector 像快递的"直送 + 入仓"组合——MooncakeConnectorV2 是骑手直送（本条包裹立刻送达），AscendStoreConnector 是同步入仓（包裹同时进共享仓库，下次有人要同款直接从仓库发）。

### 完整示例：PD 分离 + MemCache 池化（prefill 节点）

```bash
vllm serve <MODEL_PATH> \
  --kv-transfer-config '{
    "kv_connector": "MultiConnector",
    "kv_role": "kv_producer",
    "engine_id": "0",
    "kv_port": "30000",
    "kv_connector_extra_config": {
      "connectors": [
        {
          "kv_connector": "MooncakeConnectorV2",          # ① P2P 传输：KV 直送 decode
          "kv_role": "kv_producer",
          "kv_port": "30000",
          "kv_connector_extra_config": {
            "use_ascend_direct": true,                     # NPU 间直通
            "prefill": {"dp_size": 1, "pp_size": 2, "tp_size": 16, "pp_layer_partition": "42,36"},
            "decode":  {"dp_size": 16, "tp_size": 2}        # 拓扑按你的部署改
          }
        },
        {
          "kv_connector": "AscendStoreConnector",          # ② 池化写入：KV 入 memcache 池
          "kv_role": "kv_producer",
          "kv_connector_extra_config": {
            "backend": "memcache",
            "use_layerwise": false,                        # false=整块；1M 长上下文变体用 true
            "lookup_rpc_port": "0"                         # 同机多服务须各不相同
          }
        }
      ]
    }
  }'
```

> 📌 来源：官方 [GLM5.2 教程](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) MemCache KV pooling 章节（有删减）。拓扑数值（pp/tp/dp 与层分片）随部署形态变化，**逐字命令与 decode 侧配置以官方原文为准**。

**读懂这条命令的路径**：先看 `kv_role` 确认这是 prefill 节点 → `MultiConnector.connectors` 里两个 connector 各司其职 → 每个 connector 的 `kv_connector_extra_config` 回到上面三张字段表对照。

**与特性开关的组合**：官方 GLM5.2 池化示例同传 `--additional-config '{"enable_cpu_binding": true, "recompute_scheduler_enable": true, "enable_dsa_cp": true, "enable_flashcomm1": true, "enable_fused_mc2": 1}'`——PD 池化部署常与重算调度、DSA CP（v0.30.0，main 已改为 PCP）、FlashComm1 一起开。

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
