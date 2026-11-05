---
title: GLM 系列部署配方
---

# GLM 系列部署配方

> 本页命令逐字摘自 vLLM-Ascend 官方文档（`main` 分支），每条配方的"官方原文"链接可点击查看上下文（含环境变量设置、硬件要求等）。
> 由 `scripts/generate_tables.py` 从 `data/recipes.json` 自动生成，请勿手改命令区域。

GLM5 / GLM5.2 / GLM5.3-Flash 的官方部署推荐命令。

<!-- RECIPES_START -->
??? quote "GLM-5.2 & GLM-5.3 (`GLM5.2`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html>

    ```bash
    vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/GLM-5.3-w8a8c8  \
        --host 0.0.0.0  \
        --port 8000  \
        --headless  \
        --max-model-len 135000  \
        --data-parallel-size 4  \
        --data-parallel-size-local 1  \
        --data-parallel-start-rank ${dp_start_rank}  \
        --data-parallel-address "${node0_ip}"  \
        --data-parallel-rpc-port 12980  \
        --tensor-parallel-size 8  \
        --enable-expert-parallel  \
        --seed 1024  \
        --served-model-name glm  \
        --reasoning-parser glm47  \
        --safetensors-load-strategy prefetch  \
        --max-num-seqs 128  \
        --max-num-batched-tokens 8192  \
        --trust-remote-code  \
        --quantization ascend  \
        --gpu-memory-utilization 0.92  \
        --speculative-config '{"num_speculative_tokens": 3, "method": "deepseek_mtp", "enforce_eager": true}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --kv-cache-dtype int8  \
        --attention_config.indexer_kv_dtype int8  \
        --additional-config '{
                "enable_dsa_cp": true,
                "scheduler_config": {"enable_balance_scheduling": true},
                "ascend_compilation_config": {"fuse_muls_add": true},
                "multistream_overlap_shared_expert": true,
                "enable_flashcomm1": true
            }'  \
        --enable-prefix-caching  \
        --async-scheduling
    ```

??? quote "GLM-5.3-Flash (`GLM5.3-Flash`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html>

    ```bash
    vllm serve /path/to/GLM-5.3-Flash-w8a8  \
        --host 0.0.0.0  \
        --port 8000  \
        --headless  \
        --max-model-len 133120  \
        --data-parallel-size 2  \
        --data-parallel-size-local 1  \
        --data-parallel-start-rank 1  \
        --data-parallel-address $node0_ip  \
        --data-parallel-rpc-port 12321  \
        --tensor-parallel-size 8  \
        --enable-expert-parallel  \
        --seed 1024  \
        --served-model-name glm  \
        --safetensors-load-strategy prefetch  \
        --max-num-seqs 32  \
        --max-num-batched-tokens 8192  \
        --trust-remote-code  \
        --quantization ascend  \
        --limit-mm-per-prompt '{"image":1,"video":0}'  \
        --gpu-memory-utilization 0.85  \
        --speculative-config '{"num_speculative_tokens":3,"method":"deepseek_mtp","enforce_eager":true}'  \
        --compilation-config '{"cudagraph_mode":"FULL_DECODE_ONLY","cudagraph_capture_sizes":[4,8,16,32,64,96,128]}'
    ```

??? quote "GLM-5 & GLM-5.1 (`GLM5`)"
    官方原文 / Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html>

    ```bash
    vllm serve /root/.cache/modelscope/hub/models/vllm-ascend/GLM-5.1-w8a8c8-MTP  \
        --host 0.0.0.0  \
        --port 8000  \
        --headless  \
        --data-parallel-size 8  \
        --data-parallel-size-local 4  \
        --data-parallel-start-rank 4  \
        --data-parallel-address $node0_ip  \
        --enable-expert-parallel  \
        --data-parallel-rpc-port 12980  \
        --tensor-parallel-size 1  \
        --prefill-context-parallel-size 4  \
        --hf-overrides '{"use_index_cache": true, "index_topk_freq": 4}'  \
        --seed 1024  \
        --served-model-name glm-5.1  \
        --tool-call-parser glm47  \
        --reasoning-parser glm45  \
        --enable-auto-tool-choice  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.92  \
        --quantization ascend  \
        --enable-chunked-prefill  \
        --enable-prefix-caching  \
        --async-scheduling  \
        --kv-cache-dtype int8  \
        --attention_config.indexer_kv_dtype int8  \
        --additional-config '{"enable_balance_scheduling": true, "ascend_compilation_config": {"fuse_muls_add": true}, "enable_flashcomm1": true, "enable_fused_mc2": true, "enable_mlapo": true}'  \
        --compilation-config '{"cudagraph_mode": "FULL_DECODE_ONLY"}'  \
        --speculative-config '{"num_speculative_tokens": 3, "method": "deepseek_mtp","enforce_eager":true}'
    ```
<!-- RECIPES_END -->
