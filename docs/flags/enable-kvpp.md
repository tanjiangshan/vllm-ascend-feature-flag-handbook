---
title: enable_kvpp
---

# `enable_kvpp`

> KVPP（KV 流水线并行）总开关：把 MLA/SFA 非混合模型在 TP 各 rank 间冗余的 KV cache 按层分摊，同等显存容纳更多上下文 token 或并发请求。

| 属性 | 值 |
|---|---|
| 类型 | `bool` |
| 默认值 | `false` |
| 状态 | ✅ active（Experimental） |
| 适用 | 非混合 MLA/SFA 模型（如 DeepSeek 系列、GLM-5.2） |

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3 \
  --additional-config='{"enable_kvpp": true}'
```

## 机制

- KVPP 将 KV cache 的所有权按层划分到 TP 各 rank，而非每 rank 存全量副本，显存容量随 TP 数近似线性放大。
- 官方 GLM-5.2-W4A8C8 实测：单机 8 卡 TP8+EP 时 KV 容量 **6.25×**；两机 TP8+PP2+EP（38/40 层）时 **5.35×**（该数字仅对文中配置成立，非吞吐倍数）。
- 可与 TP/EP/PP/PCP 组合；PCP 时按 `TP × PCP` 的层分摊域划分。
- 派生的 `kvpp_config` 不是用户可设的顶层键，而是 `enable_kvpp=true` 后由 `KVPPConfig.from_vllm_config` 自动注入（`size = TP × PCP`），启动时校验通过即生效。

## 注意事项

- **与 DCP 互斥**：`decode_context_parallel_size != 1` 时启动报错。
- **仅非混合 MLA/SFA 模型**：GQA/MHA 或混合注意力模型启用会报 `KVPP currently supports only non-hybrid MLA models.`。
- **图模式受限**：仅支持 eager 或 `PIECEWISE`；`FULL` 图启动报错。
- **PD 分离仅在 prefill 节点开启**；decode（kv_consumer）节点必须关闭。
- **连接器受限**：PD 时 `kv_connector` 必须是 `MultiConnector`（且 `connectors` 列表非空），且不得为 `MooncakeConnectorV2` 的 `kv_consumer` 角色。
- 派生校验未通过会直接 `raise`，配置错误不会静默跳过。

## 相关开关

- [`enable_pcp_embedding_lmhead_weight_sharding`](enable-pcp-embedding-lmhead-weight-sharding.md) — PCP 相关的层分摊域
- [`kv_pool_range_debug`](kv-pool-range-debug.md) — KV pool 审计日志（配合 KVPP 调试用）
- [`sparse_kv_offload_config`](sparse-kv-offload-config.md) — 稀疏 KV 卸载（同为显存扩容手段）
