---
title: DeepSeek family recipes
---

# DeepSeek family deployment recipes

> Commands are quoted verbatim from vLLM-Ascend official docs (`main` branch). Each recipe's "Source" link shows the full context (env vars, hardware notes, etc.).
> Auto-generated from `data/recipes.json` by `scripts/generate_tables.py`; do not edit the command region.

Official deployment commands for DeepSeek V4 family (V4-Flash / V4-Pro / V4.1-Flash).

<!-- RECIPES_START -->
??? quote "DeepSeek-V4-Flash (`DeepSeek-V4-Flash`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html>

    ```bash
    vllm serve /path/to/DeepSeek-V4-Flash-0731-w8a8  \
        --max-model-len 1048576  \
        --max-num-batched-tokens 10240  \
        --served-model-name dsv4  \
        --gpu-memory-utilization 0.9  \
        --max-num-seqs 64  \
        --data-parallel-size 4  \
        --tensor-parallel-size 1  \
        --prefill-context-parallel-size 4  \
        --enable-expert-parallel  \
        --tokenizer-mode deepseek_v4  \
        --tool-call-parser deepseek_v4  \
        --enable-auto-tool-choice  \
        --reasoning-parser deepseek_v4  \
        --model-loader-extra-config='{"enable_multithread_load": true, "num_threads": 128}'  \
        --quantization ascend  \
        --port 8000  \
        --block-size 32  \
        --attention_config.indexer_kv_dtype int8  \
        --speculative-config '{"method":"dspark","num_speculative_tokens":7,"enforce_eager":true}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --additional-config '{
                "ascend_compilation_config": {
                    "enable_npugraph_ex": true,
                    "enable_static_kernel": false
                },
                "enable_cpu_binding": true,
                "multistream_overlap_shared_expert": true
            }'
    ```

??? quote "DeepSeek-V4-Pro (`DeepSeek-V4-Pro`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html>

    ```bash
    vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/DeepSeek-V4-Pro-0813-w4a8  \
        --host 0.0.0.0  \
        --port $2  \
        --data-parallel-address $5  \
        --data-parallel-rpc-port $6  \
        --data-parallel-size $3  \
        --data-parallel-rank $4  \
        --tensor-parallel-size $7  \
        --enable-expert-parallel  \
        --seed 1024  \
        --served-model-name dsv4  \
        --max-model-len 150000  \
        --max-num-batched-tokens 256  \
        --max-num-seqs 32  \
        --async-scheduling  \
        --gpu-memory-utilization 0.92  \
        --block-size 32  \
        --no-enable-prefix-caching  \
        --no-disable-hybrid-kv-cache-manager  \
        --tokenizer-mode deepseek_v4  \
        --tool-call-parser deepseek_v4  \
        --enable-auto-tool-choice  \
        --reasoning-parser deepseek_v4  \
        --attention_config.indexer_kv_dtype int8  \
        --model-loader-extra-config='{"enable_multithread_load": true, "num_threads": 128}'  \
        --trust-remote-code  \
        --quantization ascend  \
        --speculative-config '{"num_speculative_tokens": 7, "method":"dspark", "enforce_eager": true}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --additional-config '{"ascend_compilation_config":{"enable_npugraph_ex":true,"enable_static_kernel":false}, "enable_cpu_binding":true, "multistream_overlap_shared_expert":true, "scheduler_config":{"recompute_scheduler_enable":true}}'  \
        --kv-transfer-config  \
        '{"kv_connector": "MooncakeHybridConnector",
                    "kv_role": "kv_consumer",
    ```

??? quote "DeepSeek-V4.1-Flash (`DeepSeek-V4.1-Flash`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4.1-Flash.html>

    ```bash
    vllm serve "$MODEL_PATH"  \
        --host 0.0.0.0  \
        --port 8900  \
        --max-model-len 150000  \
        --max-num-batched-tokens 8192  \
        --served-model-name dsv41  \
        --gpu-memory-utilization 0.9  \
        --max-num-seqs 32  \
        --data-parallel-size 4  \
        --tensor-parallel-size 4  \
        --enable-expert-parallel  \
        --tokenizer-mode deepseek_v41  \
        --reasoning-parser deepseek_v41  \
        --tool-call-parser deepseek_v41  \
        --enable-auto-tool-choice  \
        --safetensors-load-strategy lazy  \
        --quantization ascend  \
        --block-size 128  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --async-scheduling  \
        --engram-config '{"cpu_offload":true,"dp_shared_memory":true}'  \
        --additional-config '{
                "ascend_compilation_config":{
                    "enable_npugraph_ex":true,
                    "enable_static_kernel":false
                },
                "enable_cpu_binding":true,
                "enable_fused_mc2":1,
                "enable_dsa_cp":true,
                "enable_flashcomm1":true,
                "enable_shared_expert_dp":true
            }'
    ```
<!-- RECIPES_END -->
