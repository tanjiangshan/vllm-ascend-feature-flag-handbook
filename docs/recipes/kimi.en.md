---
title: Kimi family recipes
---

# Kimi family deployment recipes

> Commands are quoted verbatim from vLLM-Ascend official docs (`main` branch). Each recipe's "Source" link shows the full context (env vars, hardware notes, etc.).
> Auto-generated from `data/recipes.json` by `scripts/generate_tables.py`; do not edit the command region.

Official deployment commands for Kimi K2.6 / K3 / K3.1-Pro.

<!-- RECIPES_START -->
??? quote "Kimi-K2.6 (`Kimi-K2.6`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K2.6.html>

    ```bash
    vllm serve Eco-Tech/Kimi-K2.6-w4a8  \
        --host 0.0.0.0  \
        --port $2  \
        --data-parallel-size $3  \
        --data-parallel-rank $4  \
        --data-parallel-address $5  \
        --data-parallel-rpc-port $6  \
        --tensor-parallel-size $7  \
        --enable-expert-parallel  \
        --seed 1024  \
        --quantization ascend  \
        --served-model-name Eco-Tech/Kimi-K2.6-w4a8  \
        --trust-remote-code  \
        --max-num-seqs 8  \
        --max-model-len 133720  \
        --max-num-batched-tokens 32  \
        --no-enable-prefix-caching  \
        --gpu-memory-utilization 0.91  \
        --enable-auto-tool-choice  \
        --tool-call-parser kimi_k2  \
        --reasoning-parser kimi_k2  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --additional-config '{"recompute_scheduler_enable":true,"multistream_overlap_shared_expert":true,"enable_mlapo":true}'  \
        --speculative-config '{"method": "eagle3", "model":"lightseekorg/kimi-k2.6-eagle3", "num_speculative_tokens": 3}'  \
        --kv-transfer-config  \
        '{"kv_connector": "MooncakeConnectorV1",
                "kv_role": "kv_consumer",
                "kv_port": "30200",
                "kv_connector_extra_config": {
                        "prefill": {
                                "dp_size": 4,
                                "tp_size": 4
                        },
                        "decode": {
                                "dp_size": 8,
                                "tp_size": 4
                        }
                    }
                }'
    ```

??? quote "Kimi K3.1 Pro (Experimental) (`Kimi-K3.1-Pro`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html>

    ```bash
    vllm serve '/root/.cache/Kimi-K3.1-Pro-w4a8'  \
        --host 0.0.0.0  \
        --port "$2"  \
        --quantization ascend  \
        --enable-auto-tool-choice  \
        --reasoning-parser kimi_k3  \
        --tool-call-parser kimi_k3  \
        --tokenizer-mode kimi_k3  \
        --data-parallel-size "$3"  \
        --data-parallel-size-local 1  \
        --data-parallel-rank "$4"  \
        --data-parallel-address "$5"  \
        --data-parallel-rpc-port "$6"  \
        --distributed-executor-backend mp  \
        --tensor-parallel-size "$7"  \
        --pipeline-parallel-size 1  \
        --prefill-context-parallel-size 1  \
        --decode-context-parallel-size 16  \
        --cp-kv-cache-interleave-size 768  \
        --block-size 768  \
        --enable-expert-parallel  \
        --seed 1024  \
        --served-model-name kimi-k3.1-pro  \
        --max-model-len 1048576  \
        --max-num-batched-tokens 8192  \
        --max-num-seqs 12  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.80  \
        --kv-cache-dtype int8  \
        --attention_config.indexer_kv_dtype int8  \
        --mm-encoder-tp-mode data  \
        --mm-processor-cache-gb 1  \
        --skip-mm-profiling  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --enable-prefix-caching  \
        --additional-config '{"enable_fused_mc2":0,"multistream_overlap_shared_expert":true,"enable_shared_expert_dp":false,"enable_mlapo":true,"scheduler_config":{"recompute_scheduler_enable":true}}'  \
        --limit-mm-per-prompt '{"vision_chunk":2}'  \
        --kv-transfer-config  \
        '{
    ```

??? quote "Kimi-K3 (`Kimi-K3`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html>

    ```bash
    vllm serve <YOUR_MODEL_PATH>  \
        --host 0.0.0.0  \
        --port $2  \
        --enable-auto-tool-choice  \
        --reasoning-parser kimi_k3  \
        --tool-call-parser kimi_k3  \
        --tokenizer-mode kimi_k3  \
        --data-parallel-size $3  \
        --data-parallel-rank $4  \
        --data-parallel-address $5  \
        --data-parallel-rpc-port $6  \
        --tensor-parallel-size $7  \
        --decode-context-parallel-size 16  \
        --cp-kv-cache-interleave-size 384  \
        --block-size 384  \
        --enable-expert-parallel  \
        --seed 1024  \
        --served-model-name kimi-k3  \
        --max-model-len 1048576  \
        --max-num-batched-tokens 8192  \
        --max-num-seqs 32  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.80  \
        --speculative-config "$SPECULATIVE_CONFIG"  \
        --mm-encoder-tp-mode data  \
        --mm-processor-cache-gb 1  \
        --skip-mm-profiling  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --enable-prefix-caching  \
        --additional-config '{"multistream_overlap_shared_expert":true,"enable_mlapo":true,"scheduler_config":{"recompute_scheduler_enable":true}}'  \
        --limit-mm-per-prompt '{"vision_chunk":2}'  \
        --kv-transfer-config  \
        '{
                  "kv_connector": "MooncakeConnectorV2",
                  "kv_role": "kv_consumer",
                  "kv_port": "'"$KV_PORT"'",
                  "kv_connector_extra_config": {
                    "prefill": {
                      "dp_size": 1,
                      "tp_size": '"$7"',
                      "pp_size": 4,
    ```
<!-- RECIPES_END -->
