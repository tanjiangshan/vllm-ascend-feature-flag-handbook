---
title: kv-transfer-config
---

# `--kv-transfer-config`

> KV transfer configuration (JSON) — the core parameter of PD (Prefill/Decode) disaggregation.

| Property | Value |
|---|---|
| Type | `KVTransferConfig` (JSON) |
| Default | `None` (disabled) |
| Category | KV Transfer & PD |

## Official definition

The config corresponding to the KV transfer... defines the KV connector and its transport properties. (vLLM source: `KVTransferConfig`)

## Ascend context & official usage

- KV connectors used in official tutorials (by frequency):
  | Connector | Where |
  |---|---|
  | `MooncakeConnectorV2` | [PD disaggregation Mooncake tutorial](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) etc. — current default recommendation |
  | `MooncakeConnectorV1` | Earlier Mooncake deployments |
  | `AscendStoreConnector` | Ascend-native KV pool |
  | `MultiConnector` | Multi-connector composition |
- In typical PD setups, prefill/decode nodes are configured with different roles, and often combined with `--no-enable-prefix-caching` (see [`enable-prefix-caching`](enable-prefix-caching.md)).
- With PCP, only `MooncakeConnectorV1/V2` are fully compatible (official matrix).

## Usage

```bash
# decode node example (simplified from the official tutorial)
vllm serve Qwen/Qwen3-8B \
  --kv-transfer-config '{"kv_connector":"MooncakeConnectorV2","kv_role":"kv_consumer",...}' \
  --no-enable-prefix-caching
```

## Related args

- [`--enable-prefix-caching`](enable-prefix-caching.md) — explicitly disabled under PD
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) — long-context PD
- Ascend PD flags: [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md), [`dyntra_lb_config`](../flags/dyntra-lb-config.md)
