---
title: Other models recipes
---

# Other models deployment recipes

> Commands are quoted verbatim from vLLM-Ascend official docs (`main` branch). Each recipe's "Source" link shows the full context (env vars, hardware notes, etc.).
> Auto-generated from `data/recipes.json` by `scripts/generate_tables.py`; do not edit the command region.

Official deployment commands for Cohere / Dots3 / Gemma4 / Hy4 / SigLIP2 / Step-5 etc.

<!-- RECIPES_START -->
??? quote "Cohere Transcribe (`Cohere-Transcribe`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Cohere-Transcribe.html>

    ```bash
    vllm serve /data/llm-workspace/cohere-transcribe-arabic-07-2026  \
        --served-model-name cohere-transcribe  \
        --trust-remote-code  \
        --tensor-parallel-size 1  \
        --dtype bfloat16  \
        --enforce-eager  \
        --block-size 128  \
        --host 0.0.0.0  \
        --port 8000
    ```

??? quote "Dots3 Note (`Dots3-Note`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html>

    ```bash
    vllm serve "$MODEL_PATH"  \
        --served-model-name "$SERVED_NAME"  \
        --tensor-parallel-size 16  \
        --enable-expert-parallel  \
        --speculative-config  \
        '{"method":"mtp","num_speculative_tokens":3,"enforce_eager":true}'  \
        --additional-config  \
        '{"enable_fused_mc2":1}'  \
        --max-model-len 4096  \
        --kv-cache-memory-bytes 4G  \
        --safetensors-load-strategy lazy  \
        --enable-prefix-caching  \
        --enable-chunked-prefill  \
        --async-scheduling  \
        --limit-mm-per-prompt '{"image":0,"video":0,"audio":1}'  \
        --allowed-local-media-path "$MEDIA_ROOT"  \
        --mm-encoder-tp-mode data  \
        --max-num-batched-tokens 4096  \
        --max-num-seqs 4  \
        --default-chat-template-kwargs '{"enable_thinking":false}'  \
        --generation-config vllm  \
        --compilation-config  \
        '{"mode":"VLLM_COMPILE","cudagraph_mode":"FULL_DECODE_ONLY","cudagraph_capture_sizes":[4,8,16],"max_cudagraph_capture_size":16}'  \
        --port 8000
    ```

??? quote "Gemma4 (`Gemma4`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Gemma4.html>

    ```bash
    vllm serve ${MODEL_PATH}  \
        --served-model-name gemma4  \
        --trust-remote-code  \
        --tensor-parallel-size 4  \
        --data-parallel-size 2  \
        --enable-expert-parallel  \
        --quantization ascend  \
        --max-model-len 32768  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'
    ```

??? quote "Hy4-preview (Experimental) (`Hy4-preview`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Hy4-preview.html>

    ```bash
    vllm serve ${MODEL}  \
        --host 0.0.0.0  \
        --port ${PORT}  \
        --data-parallel-size 2  \
        --data-parallel-size-local 1  \
        --data-parallel-address ${NODE1_IP}  \
        --data-parallel-rpc-port ${DP_RPC_PORT}  \
        --tensor-parallel-size 16  \
        --served-model-name hy4  \
        --enable-expert-parallel  \
        --max-num-seqs 256  \
        --max-model-len 96000  \
        --max-num-batched-tokens 1024  \
        --trust-remote-code  \
        --quantization ascend  \
        --gpu-memory-utilization 0.85  \
        --enable-prefix-caching  \
        --seed 1024  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --speculative-config '{"method": "mtp","num_speculative_tokens": 3}'  \
        --additional-config '{"enable_mlapo": true, "enable_fused_mc2": 1, "ascend_compilation_config": {"enable_npugraph_ex": true}}'
    ```

??? quote "SigLIP2 (`SigLIP2`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/SigLIP2.html>

    ```bash
    vllm serve $MODEL_PATH  \
        --served-model-name $MODEL_PATH  \
        --runner pooling  \
        --chat-template template_basic.jinja  \
        --limit-mm-per-prompt '{"image": 1}'  \
        --compilation-config '{"cudagraph_capture_sizes": [64,32]}'  \
        --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'  \
        --dtype float16  \
        --port 8000  \
        --max-model-len 64
    ```

??? quote "Step-5-Preview (Experimental) (`Step-5-Preview`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Step-5-Preview.html>

    ```bash
    vllm serve ${WEIGHT_PATH}  \
        --host $local_ip  \
        --port 10086  \
        --served-model-name step  \
        --trust-remote-code  \
        --max-num-seqs 256  \
        --max-num-batched-tokens 2048  \
        --max-model-len 1048576  \
        --tensor-parallel-size 4  \
        --data-parallel-size 4  \
        --data-parallel-size-local 2  \
        --data-parallel-address $node0_ip  \
        --headless  \
        --data-parallel-start-rank 2  \
        --data-parallel-rpc-port 13389  \
        --enable-expert-parallel  \
        --gpu-memory-utilization 0.96  \
        --distributed_executor_backend "mp"  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --safetensors-load-strategy 'prefetch'  \
        --additional-config '{"enable_shared_expert_dp": true, "multistream_overlap_shared_expert": true}'  \
        --speculative-config '{"num_speculative_tokens": 3,"method": "mtp"}'
    ```
<!-- RECIPES_END -->
