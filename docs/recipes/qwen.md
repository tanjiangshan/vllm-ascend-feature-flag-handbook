---
title: Qwen 系列部署配方
---

# Qwen 系列部署配方

> 本页命令逐字摘自 vLLM-Ascend 官方文档（`main` 分支），每条配方的"官方原文"链接可点击查看上下文（含环境变量设置、硬件要求等）。
> 由 `scripts/generate_tables.py` 从 `data/recipes.json` 自动生成，请勿手改命令区域。

Qwen3 系列（Dense / MoE / VL / 超大模型）的官方部署推荐命令。

<!-- RECIPES_START -->
??? quote "Qwen-VL-Dense(Qwen3-VL-8B/32B) (`Qwen-VL-Dense`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen-VL-Dense.html>

    ```bash
    vllm serve Qwen/Qwen3-VL-8B-Instruct  \
        --dtype float16  \
        --max_model_len 16384  \
        --host 0.0.0.0  \
        --port $2  \
        --dtype bfloat16  \
        --served-model-name qwen3vl  \
        --no-enable-prefix-caching  \
        --data-parallel-size $3  \
        --tensor-parallel-size $4  \
        --trust-remote-code  \
        --max-num-seqs 128  \
        --max-model-len 32768  \
        --max-num-batched-tokens 16384  \
        --gpu-memory-utilization 0.91  \
        --async-scheduling  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [1,2,4,8,16,32]}'  \
        --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex":false}}'  \
        --mm-processor-cache-gb 0
    ```

??? quote "Qwen3-30B-A3B (`Qwen3-30B-A3B`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-30B-A3B.html>

    ```bash
    vllm serve your_model_path  \
        --served-model-name qwen3  \
        --trust-remote-code  \
        --max-num-seqs 100  \
        --max-model-len 40960  \
        --max-num-batched-tokens 16384  \
        --tensor-parallel-size 4  \
        --enable-expert-parallel  \
        --quantization ascend  \
        --distributed_executor_backend "mp"  \
        --no-enable-prefix-caching  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --additional-config '{"weight_nz_mode": 2}'  \
        --gpu-memory-utilization 0.95  \
        --port 8000  \
        --speculative-config '{"method": "eagle3", "model": "your_eagle3_model_path", "num_speculative_tokens": 3}'
    ```

??? quote "Qwen3-Dense (Qwen3-0.6B/1.7B/4B/8B/14B/32B) (`Qwen3-Dense`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-Dense.html>

    ```bash
    vllm serve Eco-Tech/Qwen3-8B-w8a8sc-310-vllm/TP1/Qwen3-8B-w8a8sc-310-vllm-tp1  \
        --host 127.0.0.1  \
        --port 8080  \
        --tensor-parallel-size 1  \
        --gpu-memory-utilization 0.90  \
        --max-num-seqs 32  \
        --served-model-name qwen3  \
        --dtype float16  \
        --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex":false}}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [1,2,4,8,16,32]}'  \
        --quantization ascend  \
        --max-model-len 20480  \
        --no-enable-prefix-caching  \
        --load-format sharded_state
    ```

??? quote "Qwen3-VL-30B-A3B-Instruct (`Qwen3-VL-30B-A3B-Instruct`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3-VL-30B-A3B-Instruct.html>

    ```bash
    vllm serve Qwen/Qwen3-VL-30B-A3B-Instruct --additional-config '{"enable_fused_mc2":1}'  \
        --host 0.0.0.0  \
        --port 8000  \
        --served-model-name qwen3-vl-30b  \
        --data-parallel-size 1  \
        --tensor-parallel-size 2  \
        --enable-expert-parallel  \
        --seed 1024  \
        --max-num-seqs 32  \
        --max-model-len 32768  \
        --max-num-batched-tokens 16384  \
        --gpu-memory-utilization 0.9  \
        --no-enable-prefix-caching  \
        --mm-processor-cache-gb 0  \
        --limit-mm-per-prompt.image 1  \
        --limit-mm-per-prompt.video 0  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY","cudagraph_capture_sizes":[1,2,4,8,16,24,32]}'  \
        --additional-config '{"enable_fused_mc2": 1}'
    ```

??? quote "Qwen3.5-27B & Qwen3.6-27B (`Qwen3.5-27B-Qwen3.6-27B`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html>

    ```bash
    vllm serve $MODEL_PATH  \
        --host 0.0.0.0  \
        --port 8000  \
        --data-parallel-size 1  \
        --tensor-parallel-size 1  \
        --quantization ascend  \
        --kv-cache-dtype mxfp8  \
        --served-model-name qwen3.6  \
        --max-num-seqs 32  \
        --max-model-len 153600  \
        --max-num-batched-tokens 16384  \
        --trust-remote-code  \
        --allowed-local-media-path /  \
        --mm-processor-cache-gb 0  \
        --mm-encoder-tp-mode data  \
        --mm-processor-cache-type shm  \
        --gpu-memory-utilization 0.90  \
        --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}'  \
        --compilation-config '{"cudagraph_capture_sizes": [1,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128],"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --additional-config '{"enable_cpu_binding": true, "enable_flashcomm1": true}'
    ```

??? quote "Qwen3.5-397B-A17B (`Qwen3.5-397B-A17B`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-397B-A17B.html>

    ```bash
    vllm serve Eco-Tech/Qwen3.5-397B-A17B-w8a8-mtp  \
        --host 0.0.0.0  \
        --port 8000  \
        --headless  \
        --data-parallel-size 2  \
        --data-parallel-size-local 1  \
        --data-parallel-start-rank 1  \
        --data-parallel-address $node0_ip  \
        --data-parallel-rpc-port 13389  \
        --seed 1024  \
        --tensor-parallel-size 8  \
        --served-model-name qwen3.5  \
        --max-num-seqs 16  \
        --max-model-len 32768  \
        --max-num-batched-tokens 4096  \
        --enable-expert-parallel  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.90  \
        --no-enable-prefix-caching  \
        --quantization ascend  \
        --speculative-config '{"method": "qwen3_5_mtp", "num_speculative_tokens": 3}'  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --additional-config '{"enable_cpu_binding":true, "multistream_overlap_shared_expert": true}'
    ```

??? quote "Qwen3.5-Dense (Qwen3.5-2B/4B/9B) (`Qwen3.5-Dense`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-Dense.html>

    ```bash
    vllm serve $MODEL_PATH  \
        --host 127.0.0.1  \
        --port 8080  \
        --tensor-parallel-size 1  \
        --served-model-name qwen3.5  \
        --max-num-seqs 32  \
        --max-model-len 16384  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.90  \
        --mamba-ssm-cache-dtype float16  \
        --dtype float16  \
        --speculative-config '{"method": "qwen3_5_mtp","num_speculative_tokens":1}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY", "cudagraph_capture_sizes": [2,16]}'  \
        --additional-config '{"ascend_compilation_config": {"enable_npugraph_ex": false}}'
    ```

??? quote "Qwen3.6-35B-A3B (`Qwen3.6-35B-A3B`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.6-35B-A3B.html>

    ```bash
    vllm serve Eco-Tech/Qwen3.6-35B-A3B-w8a8-mxfp8  \
        --host 0.0.0.0  \
        --port 8000  \
        --served-model-name qwen3.6  \
        --trust-remote-code  \
        --quantization ascend  \
        --safetensors-load-strategy lazy  \
        --tensor-parallel-size 1  \
        --data-parallel-size 1  \
        --max-model-len 135168  \
        --max-num-seqs 128  \
        --max-num-batched-tokens 4096  \
        --gpu-memory-utilization 0.90  \
        --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":3}'  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --additional-config '{"enable_cpu_binding":true,"ascend_compilation_config":{"enable_npugraph_ex":true,"enable_static_kernel":true,"enable_super_kernel":false}}'  \
        --enable-prefix-caching
    ```

??? quote "Qwen3.8-Flash-Next (Experimental) (`Qwen3.8-Flash-Next`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.8-Flash-Next.html>

    ```bash
    vllm serve "$MODEL_PATH"  \
        --host 0.0.0.0  \
        --port 8088  \
        --served-model-name qwen3.8-flash-next  \
        --trust-remote-code  \
        --quantization ascend  \
        --tensor-parallel-size 8  \
        --data-parallel-size 1  \
        --data-parallel-size-local 1  \
        --data-parallel-start-rank 0  \
        --enable-expert-parallel  \
        --max-model-len 131072  \
        --max-num-seqs 8  \
        --max-num-batched-tokens 4096  \
        --gpu-memory-utilization 0.93  \
        --enable-prefix-caching  \
        --mamba-cache-mode align  \
        --enable-auto-tool-choice  \
        --tool-call-parser qwen3_xml  \
        --reasoning-parser qwen3  \
        --compilation-config '{"cudagraph_capture_sizes":[4,8,12,16,20,24,28,32],"cudagraph_mode":"FULL_DECODE_ONLY"}'  \
        --speculative-config '{"method":"qwen3_5_mtp","num_speculative_tokens":3,"enforce_eager":true}'  \
        --additional-config '{"enable_cpu_binding":true,"ascend_compilation_config":{"fuse_norm_quant":false}}'
    ```
<!-- RECIPES_END -->
