---
title: Engine args overview
---

# vLLM Engine Args Overview (Ascend context)

> Tables on this page are auto-generated from `data/engine-args.yaml` by `scripts/generate_tables.py`. Do not edit the table region by hand.
>
> **Inclusion rule**: only args that actually appear in vLLM-Ascend official docs (model tutorials, feature guides, quick_start, FAQs). Every arg exists in the vLLM source CLI definitions. **78 args**, grouped into 9 categories.
>
> Args here are `vllm serve` command-line args (`--xxx`); for vLLM-Ascend proprietary keys see the [feature flags overview](../flags/index.md).

## Relationship to official docs

- vLLM's official args docs cover 270+ args; this table focuses on the **Ascend deployment context** (real usage in official tutorials, recommended values, Ascend notes).
- Each arg's "Official docs" column links to the specific tutorial page it was taken from — click through to see the original command line.
- Defaults come from the vLLM source dataclass definitions (`ParallelConfig`/`ModelConfig`/`VllmConfig`), not prose.
- Key args have dedicated detail pages (linked arg names).

<!-- EA_TABLE_START -->
### Parallelism

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--api-server-count` | `str` | `None` | Number of API server processes. Improves request ingress throughput under high concurrency. | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) |
| `--cp-kv-cache-interleave-size` | `int` | `None` | KV cache interleave size in CP mode. Tuning knob; default 1 usually suffices. | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html) |
| `--data-parallel-address` | `str` | `None` | Address of the data parallel cluster head node. | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-backend` | `DataParallelBackend` | `"mp"` | DP backend implementation. Default 'mp'; use 'ray' for Ray clusters. | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html) |
| `--data-parallel-rank` | `int` | `None` | Data parallel rank of this instance (headless / Ray mode). | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-rpc-port` | `int` | `None` | Fixed port for DP RPC communication. Required for multi-node DP. | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--data-parallel-size`](data-parallel-size.md) | `int` | `1` | Number of data parallel groups. MoE experts are sharded by TP×PCP×DP. Required for multi-node EP. | [docs×39](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--data-parallel-size-local` | `int` | `None` | Number of DP replicas on this node. Used with data-parallel-size for multi-node DP. | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-start-rank` | `int` | `None` | Starting DP rank for this node. Multi-node DP node addressing. | [docs×16](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--decode-context-parallel-size` | `int` | `1` | Decode context parallel size. Complements PCP for decode phase. | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--distributed-executor-backend`](distributed-executor-backend.md) | `(` | `None` | Distributed executor backend: 'mp' (single node) or 'ray' (multi-node). Official multi-node tutorials use ray. | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| [`--enable-expert-parallel`](enable-expert-parallel.md) | `bool` | `false` | Use expert parallelism instead of TP for MoE layers. Standard in official MoE tutorials. | [docs×45](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| `--eplb-config` | `EPLBConfig` | `"EPLBConfig()"` | Expert parallelism load balancer config (vLLM core). Ascend dynamic EPLB is via additional-config eplb_config. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/expert_parallelism_load_balancer.html) |
| `--headless` | `str` | `None` | Headless mode: no API server on this node, DP inference only. Used for multi-node DP clusters. | [docs×19](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--master-addr` | `str` | `"127.0.0.1"` | Master node address (torchrun launcher). | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--master-port` | `int` | `29501` | Master node port (torchrun launcher). | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--nnodes` | `int` | `1` | Number of cluster nodes (torchrun launcher). Passed via torchrun in official multi-node tutorials. | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--node-rank` | `int` | `0` | Rank of this node (torchrun launcher). | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | `int` | `1` | Number of pipeline parallel groups. Used for multi-node large models, often combined with DP. | [docs×11](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | `int` | `1` | Prefill context parallel (PCP) size. Speeds up long-context prefill on A2/A3. | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | `int` | `1` | Number of tensor parallel groups. A2 tutorials use 1–8; large A3 models often 8–16. | [docs×64](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |

### Scheduling & Memory

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--async-scheduling` | `bool` | `None` | Async scheduling. Default None (auto); some official tutorials enable it explicitly for throughput. | [docs×16](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--block-size`](block-size.md) | `int` | `None` | KV cache block size. Default None (auto, typically 16); DeepSeek-V4-Pro tutorial sets 32; KVPP etc. use other values. | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--disable-hybrid-kv-cache-manager` | `bool` | `"("` | Disable hybrid KV cache manager. Auto-detected by default; rarely set manually. | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--enable-chunked-prefill`](enable-chunked-prefill.md) | `bool` | `None` | Chunked prefill. Enabled by default on vLLM main (SchedulerConfig default True), chunked by remaining max_num_batched_tokens; auto-disabled for encoder-decoder models. | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--enable-prefix-caching`](enable-prefix-caching.md) | `bool` | `None` | Prefix caching. Default None (auto per model); PD disaggregation tutorials pass --no-enable-prefix-caching on decode nodes. | [docs×34](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | `float` | `None` | Fraction of device memory for the executor (0–1). Default None → resolves to 1.0 with extensible KV cache, else 0.92 (vLLM main source); tutorials set 0.80–0.90 explicitly. | [docs×46](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/suffix_speculative_decoding.html) |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | `CacheDType` | `"auto"` | KV cache dtype (fp8, int8). Used in Ascend quantized-model tutorials to save HBM. | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--kv-cache-memory-bytes` | `int` | `None` | KV cache memory limit in bytes. Finer-grained alternative to gpu-memory-utilization. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--long-prefill-token-threshold` | `int` | `0` | Long prefill token threshold. Requests above this use the chunked path. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/MiniMax-M3.html) |
| `--mamba-ssm-cache-dtype` | `MambaDType` | `"auto"` | Cache dtype for Mamba/SSM models. Default auto. | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html) |
| [`--max-model-len`](max-model-len.md) | `int` | `None` | Model context length. Auto-derived from model config if unset; must be set for long-context. | [docs×52](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--max-num-batched-tokens`](max-num-batched-tokens.md) | `int` | `None` | Max tokens per iteration. Default None (auto); the CPP dynamic-chunk guide suggests search space [8192, 16384, 24576, 32768]. | [docs×50](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--max-num-seqs`](max-num-seqs.md) | `int` | `None` | Max sequences per iteration (concurrency cap). Default None (auto); official tutorials use 12–128, trade off memory vs latency. | [docs×47](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |

### Compilation & Graphs

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--attention-config` | `AttentionConfig` | `"AttentionConfig()"` | Attention backend and config. Ascend FA3 consistency etc. via this. | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--compilation-config`](compilation-config.md) | `CompilationConfig` | `"CompilationConfig()"` | torch.compile and CUDA Graph capture config. Ascend tutorials set cudagraph_capture_sizes for TTFT. | [docs×53](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| [`--enforce-eager`](enforce-eager.md) | `bool` | `false` | Force eager mode (skip CUDA Graph). For first deploy/debug; disable in production for graph-capture speed. | [docs×21](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Cohere-Transcribe.html) |

### Model & Loading

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--dtype` | `ModelDType` | `"auto"` | Weight dtype (auto/bfloat16/float16). Ascend quantized models often use bfloat16. | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| `--enable-lora` | `bool` | `false` | Enable LoRA. Supported on Ascend; use with lora-modules. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--generation-config` | `str` | `"auto"` | Generation config (auto-loaded from model or overridden). | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--hf-overrides` | `HfOverrides` | `"{}"` | HF config overrides (JSON). For architecture tweaks like rope scaling. | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) |
| `--load-format` | `str` | `"auto"` | Weight load format (auto/pt/safetensors). safetensors is the default recommendation. | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/netloader.html) |
| `--logprobs-mode` | `LogprobsMode` | `"raw_logprobs"` | Logprobs output mode (raw_logprobs/processed_logprobs). | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--lora-modules` | `list[LoRAModulePath]` | `None` | LoRA modules list (JSON). Use with enable-lora. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--max-lora-rank` | `MaxLoRARanks` | `16` | Max LoRA rank. Caps the size of loadable LoRA adapters. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--model` | `str` | `"Qwen/Qwen3-0.6B"` | Model path or HF model ID. Positional, but tutorials sometimes pass it explicitly. | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen-VL-Dense.html) |
| `--model-loader-extra-config` | `dict` | `"dict()"` | Model loader extra config. For advanced scenarios like Ascend NetLoader. | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--quantization`](quantization.md) | `QuantizationMethods` | `None` | Weight quantization method. Ascend tutorials use 'ascend', 'deepseek_v4_fp8', 'mxfp8'; None infers from model config. | [docs×38](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--safetensors-load-strategy` | `SafetensorsLoadStrategy` | `"("` | safetensors load strategy (lazy/prefetch). lazy saves startup memory. | [docs×14](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--seed` | `int` | `0` | Random seed. Set explicitly for reproducibility tests and RL rollouts. | [docs×10](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--tokenizer-mode` | `TokenizerMode` | `"auto"` | Tokenizer mode. Set to a specific tokenizer for DeepSeek-V4/Kimi-K3 in official tutorials. | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--trust-remote-code` | `bool` | `false` | Trust custom code in model repo. Required for some models (InternVL, newer architectures). | [docs×53](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |

### Speculative Decoding

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| [`--speculative-config`](speculative-config.md) | `dict[str, Any]` | `None` | Speculative decoding config (JSON). MTP/EAGLE3 for DeepSeek/Kimi in Ascend tutorials. | [docs×40](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/suffix_speculative_decoding.html) |

### KV Transfer & PD

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--ec-transfer-config` | `ECTransferConfig` | `None` | EC transfer config. For encoder cache scenarios. | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/encoder_cache_cpu_offload.html) |
| [`--kv-transfer-config`](kv-transfer-config.md) | `KVTransferConfig` | `None` | KV transfer config (JSON). Core of PD disaggregation: NixlConnector/Mooncake etc. | [docs×17](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |

### Multimodal

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--allowed-local-media-path` | `str` | `""` | Allowed local media path prefix. For local image/video inference. | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--limit-mm-per-prompt` | `dict[str, int]` | `None` | Per-prompt multimodal limit (JSON). E.g. {"image":1,"video":0}. | [docs×14](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-encoder-tp-mode` | `MMEncoderTPMode` | `"weights"` | MM encoder TP mode (weights/data). Tuning for vision models. | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-processor-cache-gb` | `float` | `4` | MM processor cache size (GB). Default 4; may need increase for video models. | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-processor-cache-type` | `MMCacheType` | `"("` | MM processor cache type (lru etc.). | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html) |
| `--skip-mm-profiling` | `bool` | `false` | Skip MM profiling. Speeds up startup for known models. | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |

### Server

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| [`--additional-config`](additional-config.md) | `dict` | `"{}"` | Platform extension config (JSON). Sole entry for vLLM-Ascend's 51 feature flags — see the flags overview. | [docs×66](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| `--chat-template` | `str` | `None` | Chat template path. For custom chat formats. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/SigLIP2.html) |
| `--default-chat-template-kwargs` | `dict[str, Any]` | `None` | Default chat template kwargs (JSON). E.g. enable_thinking. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--enable-auto-tool-choice` | `bool` | `false` | Auto tool choice. Use with tool-call-parser. | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--enable-return-routed-experts` | `bool` | `false` | Return routed expert info. For MoE debugging/analysis. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--host` | `str` | `None` | API listen address. Default 127.0.0.1; use 0.0.0.0 for cluster. | [docs×47](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--port` | `int` | `8000` | API service port. Default 8000. | [docs×57](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--profiler-config` | `ProfilerConfig` | `"ProfilerConfig()"` | Profiler config (JSON). Entry for Ascend msprof profiling toolchain. | [docs×3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K2.6.html) |
| `--reasoning-parser` | `str` | `""` | Reasoning parser (deepseek_v41, glm45). Separates chain-of-thought content. | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4.1-Flash.html) |
| `--runner` | `RunnerOption` | `"auto"` | Runner type (generate/pooling). Default auto. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/SigLIP2.html) |
| `--served-model-name` | `str` | `None` | Model name(s) exposed in API. Can differ from path; supports aliases. | [docs×63](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--tokens-only` | `bool` | `false` | Return tokens only, no text. For benchmarking/dev. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--tool-call-parser` | `str` | `None` | Tool call parser (deepseek_v4, glm47). Use with enable-auto-tool-choice. | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |

### RL Training

| Argument | Type | Default | Description | Official docs |
|---|---|---|---|---|
| `--ec-manager-config` | `EcManagerConfig` | `None` | Encoder cache manager config. Capacity/eviction policy for multimodal encoder cache. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/encoder_cache_manager.html) |
| `--enable-sleep-mode` | `bool` | `false` | Sleep mode. Frees HBM for the trainer during RL training, at the cost of wakeup latency. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--engram-config` | `EngramConfig` | `None` | Engram config. Ascend-specific graph optimization mode. | [docs×1](https://docs.vllm.ai/projects/ascend/en/v0.30.0/tutorials/models/DeepSeek-V4.1-Flash.html) |
| `--weight-transfer-config` | `WeightTransferConfig` | `None` | Weight transfer config (JSON). For rollout→train weight sync in RL. | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
<!-- EA_TABLE_END -->

## Recommended combos (from official tutorials)

| Scenario | Typical args |
|---|---|
| Single-card A2 small model | `--tensor-parallel-size 1 --max-model-len 32768 --gpu-memory-utilization 0.9 --max-num-seqs 32` |
| MoE large model EP | `--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M` (M×DP = experts) |
| Long context | `--max-model-len <big> --enable-chunked-prefill --max-num-batched-tokens 16384+` |
| PD disaggregation | `--kv-transfer-config '{...}' --enable-prefix-caching/--no-enable-prefix-caching` per node |
| Production | Drop `--enforce-eager` (enable CUDA Graph); set `--compilation-config` capture policy |

For full commands and per-model deployment guides, see the official tutorials: [Model Deployment Tutorials](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/index.html).

## How this data is verified

- **Existence**: all 78 args are defined via `add_argument()` in vLLM source.
- **Ascend context**: every arg appears in ≥1 real command line in official docs (`doc_count` shows file count).
- **Defaults**: extracted from `EngineArgs`/`FrontendArgs` dataclasses and `vllm/config/*.py`; `None` means "auto-infer" or "unset".
- **Descriptions**: faithful translations of official help text plus observed usage in official tutorials — everything is traceable.
