---
title: MiniMax 系列部署配方
---

# MiniMax 系列部署配方

> 本页命令逐字摘自 vLLM-Ascend 官方文档（`main` 分支），每条配方的"官方原文"链接可点击查看上下文（含环境变量设置、硬件要求等）。
> 由 `scripts/generate_tables.py` 从 `data/recipes.json` 自动生成，请勿手改命令区域。

MiniMax M3 / M3.1-Flash 的官方部署推荐命令。

<!-- RECIPES_START -->
??? quote "MiniMax-M3.1-Flash (Experimental) (`MiniMax-M3.1-Flash`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/MiniMax-M3.1-Flash.html>

    ```bash
    vllm serve ${MODEL_PATH}  \
        --host 0.0.0.0  \
        --port 11223  \
        --served-model-name minimax-m3.1-flash  \
        --trust-remote-code  \
        --max-model-len "$MAX_MODEL_LEN"  \
        --tensor-parallel-size 4  \
        --data-parallel-size 4  \
        --enable-expert-parallel  \
        --max-num-seqs 32  \
        --disable-hybrid-kv-cache-manager  \
        --gpu-memory-utilization 0.92  \
        --quantization ascend  \
        --reasoning-parser minimax_m3  \
        --enable-auto-tool-choice  \
        --tool-call-parser minimax_m3  \
        --limit-mm-per-prompt '{"image":1,"video":0}'  \
        --enable-chunked-prefill  \
        --enable-prefix-caching  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --additional-config '{
              "enable_cpu_binding": true,
              "enable_flashcomm1": true,
              "multistream_overlap_shared_expert": true,
              "enable_shared_expert_dp":true,
              "weight_nz_mode": 2
          }'  \
        --speculative-config '{
              "method":"dspark",
              "num_speculative_tokens":7,
              "enforce_eager":true,
              "draft_sample_method":"probabilistic"
          }'  \
        --safetensors-load-strategy prefetch
    ```

??? quote "MiniMax-M3 (`MiniMax-M3`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/MiniMax-M3.html>

    ```bash
    vllm serve` settings as Section 5.3.1 (one P plus two D nodes). The 950DT pool example retains its two-node 1P1D topology. Prefill and Decode switch to `MultiConnector` so live P→D KV transfer and Mooncake KV Cache Pool work together:
    
    - `MooncakeConnectorV1` transfers KV from Prefill to Decode in real time (same role as Section 5.3.1).
    - `AscendStoreConnector` stores KV in the Mooncake KV Cache Pool so later Prefills with the same prefix can hit the pool instead of recomputing.
    - By default the Prefill node performs pool lookup, load, and write.
    
    The examples below enable three-tier KV storage: the active NPU KV cache, the Mooncake memory pool, and SSD offload.
    
    For backend selection, `mooncake.json`, Mooncake Master, eviction, tenant options, and hardware-specific pooling exports, refer to the [KV Cache Pool Deployment Guide](../../user_guide/feature_guide/kv_cache_pool_ascend_store.md). For MiniMax-specific issues, refer to [Chapter 10 FAQ](#10-faq).
    
    **Compared with normal PD in Section 5.3.1, pay attention to these pooling-only requirements:**
    
    | Item | Normal PD (5.3.1) | Pooled PD (this section) |
    | ---- | --------------- | ------------------------ |
    | Connector | Single `MooncakeConnectorV1` | `MultiConnector` wrapping `MooncakeConnectorV1` + `AscendStoreConnector` |
    | Mooncake Master | Not required | Start `mooncake_master --enable_offload=true` before Decode / Prefill |
    | `mooncake.json` | Not required | Required on every rank; A3 P and both D nodes use `15GB`; 950D
    ```
<!-- RECIPES_END -->
