---
title: sparse_kv_offload_config
---

# `sparse_kv_offload_config`

> 稀疏 KV cache 卸载到 DRAM 的配置，把长上下文的冷 KV 块搬出 HBM，扩大可并发 token 数。

| 属性 | 值 |
|---|---|
| 类型 | `dict` |
| 默认值 | `{}` |
| 状态 | ✅ active |
| 适用 | 仅 950 系列产品（A5） |

## 用法

```bash
vllm serve <model> \
  --additional-config='{"sparse_kv_offload_config": {"enabled": true, "dram_size_per_dp_GB": 110}}' \
  --kv-transfer-config='{"kv_connector": "SfaRemoteD2HConnector", "kv_role": "kv_consumer", "kv_port": 20050}'
```

## 子键

| 键 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `enabled` | `bool` | `false` | 是否启用稀疏 KV 卸载 |
| `topk_buffer_size` | `int` | `-1` | `-1` 时自动解析为 `(1 + 投机 token 数) × 2048` |
| `dram_size_per_dp_GB` | `int` | `110` | 每 DP 的 DRAM 容量上限（GB） |
| `keep_device_kv_cache` | `bool` | `false` | 是否同时保留 HBM 中的 KV cache |
| `use_fused_overlap` | `bool` | `false` | 是否启用融合 overlap 路径（false 时走 fused LIM + Copy-SFA） |

## 注意事项

- **仅 950 系列产品（A5）**：`from_additional_config` 里有 `is_950()` 前置校验，其他芯片会启动报错。
- **勿在 prefill 节点设置**：`kv_consumer`（decode 侧）专属，prefill 节点配置无意义且可能报错。
- `dram_size_per_dp_GB` 必须为正，否则 `sparse_kv_offload_config.dram_size_per_dp_GB must be positive`。
- 需搭配 `SfaRemoteD2HConnector` / `AscendStoreConnector` 等 KV 传输连接器使用。

## 相关开关

- [`enable_kvpp`](enable-kvpp.md) — KVPP 显存扩容（HBM 侧按层分摊）
- [`multistream_engram_overlap`](multistream-engram-overlap.md) — A5 上 Engram 模型的多流重叠
- [`kv_pool_range_debug`](kv-pool-range-debug.md) — KV pool 审计日志（调试用）
