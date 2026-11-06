---
title: kv-transfer-config
---

# `--kv-transfer-config`

> KV transfer configuration (JSON) — the core parameter of PD (Prefill/Decode) disaggregation: how KV moves between nodes.

| Property | Value |
|---|---|
| Type | `KVTransferConfig` (JSON) |
| Default | `None` (disabled) |
| Category | KV Transfer & PD |

## Official definition

> The config corresponding to the KV transfer... defines the KV connector and its transport properties.

(vLLM source: `KVTransferConfig`, [config/kv_transfer.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/kv_transfer.py))

## How it works

**What PD disaggregation is**: prefill (heavy compute) and decode (long generation) are split into separate node pools. A prefill node computes a request's full KV, then **sends the KV through the KV transfer layer to a decode node**, which resumes generation. Each pool scales with its own load.

**This parameter's role**: tells the engine "is this node a KV producer or consumer, which connector, which transport". Key JSON fields (evidenced from official tutorials):

| Field | Role |
|---|---|
| `kv_connector` | connector implementation (below) |
| `kv_role` | this node's role: `kv_producer` (prefill side) / `kv_consumer` (decode side) |

**Connectors used in official tutorials** (by frequency):

| Connector | Where |
|---|---|
| `MooncakeConnectorV2` | [PD disaggregation Mooncake tutorial](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) etc. — current default recommendation |
| `MooncakeConnectorV1` | earlier Mooncake deployments |
| `AscendStoreConnector` | Ascend-native KV pooling (KV Cache Pool / Ascend Store) |
| `MultiConnector` | multi-connector composition |

## KV pooling (Ascend Store)

**KV pooling** (KV Cache Pool / Ascend Store) is vLLM-Ascend's **cross-node KV cache pooling storage**: KV cache is written to external storage backends and shared/reused across multiple vLLM instances under the PD disaggregation architecture, avoiding redundant prefill of identical prefixes. It is configured through this arg's `AscendStoreConnector` — **not** an `additional-config` flag, which is why "pooling" yields no hit in the feature-flags overview.

| Backend | When to choose (official docs) |
|---|---|
| Mooncake | Default backend; pick it for SSD Offload (extended KV capacity) or multi-tenant quota management |
| Memcache | Based on MemFabric; pick it for A3 HCCS low-latency transfer or layer-by-layer KV transfer (`use_layerwise`) |
| Yuanrong | Based on openyuanrong-datasystem; pick it for multi-node deployment, Remote H2D transfer, or openEuler integration |

**Key constraints** (official feature page):

- Supported since vLLM-Ascend **v0.23.0**; hardware A2 / A3 / 950PR&950DT;
- `use_layerwise` layer-wise transfer is supported **only on the prefill node of the Mooncake / Memcache backends**;
- `kv_load_failure_policy=recompute` does not yet support hybrid-attention models (e.g. DeepSeekV4, Qwen 3.5);
- Mooncake backend requires >= 0.3.11.post1 (layer-wise needs >= 0.3.14); Memcache backend requires `memfabric-hybrid` / `memcache-hybrid` >= 1.3.0;
- Combines with [`enable_kvpp`](../flags/enable-kvpp.md) (pooling uses `kv_role` = `kv_producer` / `kv_both` with whole-block loading); Mooncake layerwise pooling (`backend="mooncake"` + `use_layerwise=true`) is Experimental.

Official details: [KV Cache Pool (Ascend Store)](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/kv_cache_pool_ascend_store.html) · [Mooncake layerwise pooling adaptation](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/mooncake_layerwise_adaptation_and_optimization.html)

## Parameter interplay

| Related arg | Relationship |
|---|---|
| [`--enable-prefix-caching`](enable-prefix-caching.md) | **explicitly disabled under PD** (`--no-enable-prefix-caching`, official tutorial practice) — prefix-reuse semantics are owned by the transfer layer |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | only MooncakeConnectorV1/V2 are fully PCP-compatible (official matrix) |
| [`--block-size`](block-size.md) | KV block layout must align with the transfer layer |
| Ascend [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md) / [`dyntra_lb_config`](../flags/dyntra-lb-config.md) | recomputation scheduling and dynamic load balancing for PD |

**Analogy**: PD disaggregation is a "central kitchen + front stores" model — the kitchen (prefill pool) cooks everything to half-done (KV computed), this parameter is the cold-chain logistics protocol (which warehouse, which truck, which store), and the stores (decode pool) only do the final plating.

## Ascend context & official usage

- Official PD tutorials set companion env vars first (Mooncake address, local KV pool path), then pass this arg; verbatim commands and env-var setup are in the official docs ([Mooncake single-node deployment](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html)).
- When combined with PCP, connector choice is constrained (table above); re-verify compatibility after each vllm-ascend upgrade.

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
- [`recompute_scheduler_enable`](../flags/recompute-scheduler-enable.md) — Ascend PD recomputation scheduling
