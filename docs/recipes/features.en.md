---
title: Feature scenarios recipes
---

# Feature scenarios deployment recipes

> Commands are quoted verbatim from vLLM-Ascend official docs (`main` branch). Each recipe's "Source" link shows the full context (env vars, hardware notes, etc.).
> Auto-generated from `data/recipes.json` by `scripts/generate_tables.py`; do not edit the command region.

Official commands for feature scenarios: PD disaggregation (Mooncake), Ray multi-node, suffix speculative decoding.

<!-- RECIPES_START -->
??? quote "Prefill-Decode Disaggregation (Qwen2.5-VL) (`pd_disaggregation_mooncake_single_node`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html>

    ```bash
    vllm serve /model/Qwen2.5-VL-7B-Instruct   \
        --host 0.0.0.0  \
        --port 13700  \
        --no-enable-prefix-caching  \
        --tensor-parallel-size 1  \
        --seed 1024  \
        --served-model-name qwen25vl  \
        --max-model-len 40000   \
        --max-num-batched-tokens 40000   \
        --trust-remote-code  \
        --gpu-memory-utilization 0.9   \
        --kv-transfer-config  \
        '{"kv_connector": "MooncakeConnectorV1",
          "kv_role": "kv_producer",
          "kv_port": "30000",
          "kv_connector_extra_config": {
                    "prefill": {
                            "dp_size": 1,
                            "tp_size": 1
                     },
                     "decode": {
                            "dp_size": 1,
                            "tp_size": 1
                     }
              }
          }'
    ```

??? quote "Ray Distributed (Qwen3-235B-A22B) (`ray`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html>

    ```bash
    vllm serve Qwen/Qwen3-235B-A22B  \
        --distributed-executor-backend ray  \
        --pipeline-parallel-size 2  \
        --tensor-parallel-size 8  \
        --enable-expert-parallel  \
        --seed 1024  \
        --max-model-len 8192   \
        --max-num-seqs 25  \
        --served-model-name qwen  \
        --trust-remote-code  \
        --gpu-memory-utilization 0.9
    ```

??? quote "Suffix Speculative Decoding (`suffix_speculative_decoding`)"
    Source: <https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/suffix_speculative_decoding.html>

    ```bash
    vllm serve /data/Qwen3-32B  \
        --served-model-name qwen3  \
        --trust-remote-code  \
        --distributed-executor-backend mp  \
        --tensor-parallel-size 4  \
        --max-model-len 5500  \
        --max-num-batched-tokens 40960  \
        --speculative-config '{"method": "suffix", "num_speculative_tokens": 3}'  \
        --gpu-memory-utilization 0.9  \
        --additional-config '{"pa_shape_list":[48,64,72,80], "weight_prefetch_config":{"enable":true}}'  \
        --port 8011
    ```
<!-- RECIPES_END -->
