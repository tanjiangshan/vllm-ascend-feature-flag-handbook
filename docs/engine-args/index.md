---
title: 引擎参数总览
---

# vLLM 引擎参数总览（Ascend 语境）

> 本页表格由 `scripts/generate_tables.py` 从 `data/engine-args.yaml` 自动生成，请勿手改表格区域。
>
> 收录原则：**只收录 vLLM-Ascend 官方文档（模型教程、特性指南、quick_start、FAQs）中真实出现过的参数**；每个参数都在 vLLM 源码（`arg_utils.py`/`cli_args.py`/`config/`）中有定义。共 **78 个参数**，按功能分 9 类。
>
> 这里的参数指 `vllm serve` **顶层命令行参数**（`--xxx`），由 vLLM 主仓定义、跨平台通用；**vLLM-Ascend 插件专有的配置键**（`AscendConfig` 字段，经 `--additional-config` JSON 传入）见[特性开关总览](../flags/index.md)。

## 与官方文档的关系

- vLLM 官方参数文档覆盖全部 270+ 个参数；本表聚焦 **Ascend 部署语境**（官方教程中的实际用法、推荐值、注意事项）。
- 每个参数的"官方文档出处"链接到具体的 vLLM-Ascend 教程页面，可点击查看原始命令行上下文。
- 默认值取自 vLLM 源码 dataclass 定义（`ParallelConfig`/`ModelConfig`/`VllmConfig` 等），非文档文字描述。
- 重点参数有独立详情页（见带链接的参数名）。

<!-- EA_TABLE_START -->
### 并行策略

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--api-server-count` | `str` | `None` | API 服务器进程数。高并发时提升请求接入吞吐。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.2.html) |
| `--data-parallel-address` | `str` | `None` | DP 集群头节点地址。多节点 DP 时指向 head 节点。 | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-backend` | `DataParallelBackend` | `"mp"` | DP 后端实现。默认 'mp'（多进程）；Ray 多节点部署可换 'ray'。 | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html) |
| `--data-parallel-rank` | `int` | `None` | 当前实例的 DP rank（headless / Ray 场景用）。 | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-rpc-port` | `int` | `None` | DP RPC 通信固定端口。多节点 DP 必配。 | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--data-parallel-size`](data-parallel-size.md) | `int` | `1` | 数据并行组数。MoE 专家按 TP×PCP×DP 的乘积分片。多节点 EP 部署的必备参数。 | [docs×39](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--data-parallel-size-local` | `int` | `None` | 本节点上的 DP 副本数。多节点 DP 时与 data-parallel-size 配合。 | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--data-parallel-start-rank` | `int` | `None` | 该节点上 DP 副本的起始 rank。多节点 DP 的节点寻址参数。 | [docs×16](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--decode-context-parallel-size` | `int` | `1` | Decode 上下文并行。与 PCP 配合的 decode 阶段并行。 | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--distributed-executor-backend`](distributed-executor-backend.md) | `(` | `None` | 分布式执行后端：'mp'（多进程，单机）或 'ray'（多机）。Ascend 官方多机教程用 ray。 | [docs×20](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| [`--enable-expert-parallel`](enable-expert-parallel.md) | `bool` | `false` | MoE 专家用专家并行（而非 TP）切分。vLLM-Ascend 官方 MoE 教程的标配。 | [docs×45](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| `--eplb-config` | `EPLBConfig` | `"EPLBConfig()"` | 专家并行负载均衡配置（vLLM 核心侧）。Ascend 侧动态 EPLB 走 additional-config 的 eplb_config。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/expert_parallelism_load_balancer.html) |
| `--headless` | `str` | `None` | 无头模式：节点不启动 API 服务，仅作为 DP 推理节点。多机 DP 集群的非头节点使用。 | [docs×19](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--master-addr` | `str` | `"127.0.0.1"` | 主节点地址（torchrun 启动器用）。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--master-port` | `int` | `29501` | 主节点端口（torchrun 启动器用）。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--nnodes` | `int` | `1` | 集群节点数（torchrun 启动器用）。Ascend 官方多机教程中由脚本传入。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--node-rank` | `int` | `0` | 当前节点的 rank（torchrun 启动器用）。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--pipeline-parallel-size`](pipeline-parallel-size.md) | `int` | `1` | 流水线并行组数。多机部署大模型时启用，常与 DP 组合。 | [docs×11](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |
| [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) | `int` | `1` | Prefill 上下文并行（PCP）。长上下文场景的 prefill 加速。A2/A3 官方教程常用。 | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--tensor-parallel-size`](tensor-parallel-size.md) | `int` | `1` | 张量并行组数。官方教程中 A2 单卡/多卡用 1–8，A3 大模型常配 8–16。 | [docs×64](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/ray.html) |

### KV 缓存与内存

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--cp-kv-cache-interleave-size` | `int` | `None` | CP 模式下 KV cache 的交错粒度。调优参数，默认 1 通常够用。 | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html) |
| [`--block-size`](block-size.md) | `int` | `None` | KV cache block 大小。默认 None（自动，通常 16）；DeepSeek-V4-Pro 教程显式设 32，KVPP 等特性另有取值。 | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--enable-prefix-caching`](enable-prefix-caching.md) | `bool` | `None` | 前缀缓存。默认 None（按模型自动判断）；PD 分离教程中 decode 节点显式用 --no-enable-prefix-caching。 | [docs×34](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--kv-cache-dtype`](kv-cache-dtype.md) | `CacheDType` | `"auto"` | KV cache 量化类型（如 fp8、int8）。Ascend 量化模型教程常用以节省显存。 | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--kv-cache-memory-bytes` | `int` | `None` | KV cache 显存上限（字节）。比 gpu-memory-utilization 更精细的替代。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |

### 调度与内存

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--async-scheduling` | `bool` | `None` | 异步调度。默认 None（自动）；部分官方教程显式开启以提升吞吐。 | [docs×16](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| `--disable-hybrid-kv-cache-manager` | `bool` | `"("` | 禁用混合 KV cache 管理器。vLLM 默认按模型自动判断，一般不手动设。 | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--enable-chunked-prefill`](enable-chunked-prefill.md) | `bool` | `None` | 分块 prefill。vLLM main 默认开启（SchedulerConfig 默认 True），按 max_num_batched_tokens 剩余额度切分；encoder-decoder 模型自动禁用。 | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html) |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | `float` | `None` | 模型执行器显存占比（0–1）。默认 None → 可扩展 KV cache 时解析为 1.0，否则 0.92（vLLM main 源码）；官方教程多显式设 0.80–0.90。 | [docs×46](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/suffix_speculative_decoding.html) |
| `--long-prefill-token-threshold` | `int` | `0` | 长 prefill token 阈值。超过该值的请求走分块路径。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/MiniMax-M3.html) |
| `--mamba-ssm-cache-dtype` | `MambaDType` | `"auto"` | Mamba/SSM 模型的 cache dtype。默认为 auto。 | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html) |
| [`--max-model-len`](max-model-len.md) | `int` | `None` | 模型最大上下文长度。不设则从模型 config 自动推断。长文本场景必须显式设置。 | [docs×52](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--max-num-batched-tokens`](max-num-batched-tokens.md) | `int` | `None` | 单次迭代最大 token 数。默认 None（自动）；动态分块流水线并行（CPP）指南的调优搜索空间为 [8192, 16384, 24576, 32768]。 | [docs×50](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| [`--max-num-seqs`](max-num-seqs.md) | `int` | `None` | 单次迭代最大处理序列数（并发上限）。默认 None（自动）；官方教程实测取值 12–128，按显存与延迟权衡。 | [docs×47](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |

### 编译与图

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--attention-config` | `AttentionConfig` | `"AttentionConfig()"` | 注意力后端及配置。子键 indexer_kv_dtype 是 Lightning Indexer 稀疏注意力的 KV dtype（fp8/int8/mxfp4），v0.30.0 起分别派生 LI-C8/LI-C4 布局；与 --kv-cache-dtype 配对使用，P/D 两侧取值须一致。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--compilation-config`](compilation-config.md) | `CompilationConfig` | `"CompilationConfig()"` | torch.compile 与 CUDA Graph 捕获配置。Ascend 官方教程中常配 cudagraph_capture_sizes 提升首 token 延迟。 | [docs×53](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| [`--enforce-eager`](enforce-eager.md) | `bool` | `false` | 强制 eager 模式（跳过 CUDA Graph）。首次部署或调试时用；生产关闭以获取图捕获性能。 | [docs×21](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Cohere-Transcribe.html) |

### 模型与加载

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--dtype` | `ModelDType` | `"auto"` | 权重计算 dtype（auto/bfloat16/float16）。Ascend 量化模型常用 bfloat16。 | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| `--enable-lora` | `bool` | `false` | 启用 LoRA。Ascend 侧支持，配合 lora-modules 使用。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--generation-config` | `str` | `"auto"` | 生成配置（从模型 config 自动加载或覆盖）。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--hf-overrides` | `HfOverrides` | `"{}"` | HF config 覆盖（JSON）。用于修改模型架构参数（如 rope scaling）。 | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) |
| `--load-format` | `str` | `"auto"` | 权重加载格式（auto/pt/safetensors等）。safetensors 为默认推荐。 | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/netloader.html) |
| `--logprobs-mode` | `LogprobsMode` | `"raw_logprobs"` | logprobs 输出模式（raw_logprobs/processed_logprobs）。 | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--lora-modules` | `list[LoRAModulePath]` | `None` | LoRA 模块列表（JSON）。与 enable-lora 配合。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--max-lora-rank` | `MaxLoRARanks` | `16` | LoRA 最大 rank。限制可加载的 LoRA 适配器规模。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/lora.html) |
| `--model` | `str` | `"Qwen/Qwen3-0.6B"` | 模型路径或 HF 模型 ID。positional 参数，但官方教程中有时也显式写 --model。 | [docs×4](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen-VL-Dense.html) |
| `--model-loader-extra-config` | `dict` | `"dict()"` | 模型加载器额外配置。Ascend 网络加载器（NetLoader）等高级场景用。 | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| [`--quantization`](quantization.md) | `QuantizationMethods` | `None` | 权重量化方法。Ascend 教程用 'ascend'、'deepseek_v4_fp8'、'mxfp8' 等；None 则从模型 config 推断。 | [docs×38](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--safetensors-load-strategy` | `SafetensorsLoadStrategy` | `"("` | safetensors 加载策略（lazy/prefetch）。lazy 按需加载节省启动内存。 | [docs×14](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--seed` | `int` | `0` | 随机种子。可复现性测试和 RL rollout 场景常显式设置。 | [docs×10](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--tokenizer-mode` | `TokenizerMode` | `"auto"` | 分词器模式。Ascend 官方教程中为 DeepSeek-V4/Kimi-K3 设特定 tokenizer。 | [docs×8](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--trust-remote-code` | `bool` | `false` | 信任模型仓库中的自定义代码。部分模型（如 InternVL、某些新架构）必须开启。 | [docs×53](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |

### 投机解码

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| [`--speculative-config`](speculative-config.md) | `dict[str, Any]` | `None` | 投机解码配置（JSON）。Ascend 教程中为 DeepSeek/Kimi 配置 MTP/EAGLE3。 | [docs×40](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/suffix_speculative_decoding.html) |

### KV 传输与 PD 分离

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--ec-transfer-config` | `ECTransferConfig` | `None` | EC 传输配置。编码器缓存（Encoder Cache）场景用。 | [docs×1](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/encoder_cache_cpu_offload.html) |
| [`--kv-transfer-config`](kv-transfer-config.md) | `KVTransferConfig` | `None` | KV 传输配置（JSON）。PD 分离部署的核心：NixlConnector/Mooncake 等后端。 | [docs×17](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |

### 多模态

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--allowed-local-media-path` | `str` | `""` | 允许的本地媒体路径前缀。本地图片/视频推理服务时配置。 | [docs×7](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--limit-mm-per-prompt` | `dict[str, int]` | `None` | 单 prompt 多模态数量限制（JSON）。如 {"image":1,"video":0}。 | [docs×14](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-encoder-tp-mode` | `MMEncoderTPMode` | `"weights"` | 多模态编码器 TP 模式（weights/data）。视觉模型调优。 | [docs×9](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-processor-cache-gb` | `float` | `4` | 多模态处理器缓存大小（GB）。默认 4；视频模型可能需要调大。 | [docs×13](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--mm-processor-cache-type` | `MMCacheType` | `"("` | 多模态处理器缓存类型（lru等）。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Qwen3.5-27B-Qwen3.6-27B.html) |
| `--skip-mm-profiling` | `bool` | `false` | 跳过多模态 profiling。已知模型可加速启动。 | [docs×5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |

### 服务端

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| [`--additional-config`](additional-config.md) | `dict` | `"{}"` | 平台扩展配置（JSON）。vLLM-Ascend 64 个特性开关的唯一入口，详见本站特性开关总览。 | [docs×66](https://docs.vllm.ai/projects/ascend/en/latest/getting_started/quick_start/online/qwen3-0.6b-310p.inc.html) |
| `--chat-template` | `str` | `None` | 对话模板路径。自定义 chat 格式时指定。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/SigLIP2.html) |
| `--default-chat-template-kwargs` | `dict[str, Any]` | `None` | 对话模板默认参数（JSON）。如 enable_thinking。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Dots3-Note.html) |
| `--enable-auto-tool-choice` | `bool` | `false` | 自动工具选择。配合 tool-call-parser 使用。 | [docs×18](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |
| `--enable-return-routed-experts` | `bool` | `false` | 返回路由专家信息。MoE 调试/分析用。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--host` | `str` | `None` | API 服务监听地址。默认 127.0.0.1；集群部署用 0.0.0.0。 | [docs×47](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--port` | `int` | `8000` | API 服务端口。默认 8000。 | [docs×57](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--profiler-config` | `ProfilerConfig` | `"ProfilerConfig()"` | 性能分析器配置（JSON）。Ascend msprof 等 profiling 工具链入口。 | [docs×3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K2.6.html) |
| `--reasoning-parser` | `str` | `""` | 推理输出解析器（如 deepseek_v41、glm45）。用于分离思维链内容。 | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4.1-Flash.html) |
| `--runner` | `RunnerOption` | `"auto"` | 执行器类型（generate/pooling等）。默认 auto。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/SigLIP2.html) |
| `--served-model-name` | `str` | `None` | API 中暴露的模型名。可与实际路径不同，支持多别名。 | [docs×63](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/features/pd_disaggregation_mooncake_single_node.html) |
| `--tokens-only` | `bool` | `false` | 只返回 token 不返回文本。压测/开发场景用。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--tool-call-parser` | `str` | `None` | 工具调用解析器（如 deepseek_v4、glm47）。与 enable-auto-tool-choice 配合。 | [docs×15](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) |

### RL 训练

| 参数 | 类型 | 默认值 | 说明 | 官方文档出处 |
|---|---|---|---|---|
| `--ec-manager-config` | `EcManagerConfig` | `None` | 编码器缓存管理器配置。多模态编码器缓存的容量/淘汰策略。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/configuration/encoder_cache_manager.html) |
| `--enable-sleep-mode` | `bool` | `false` | 休眠模式。RL 训练中释放 GPU 显存给训练器，代价是唤醒延迟。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
| `--engram-config` | `EngramConfig` | `None` | Engram 配置。Ascend 侧特定图优化模式。 | [docs×1](https://docs.vllm.ai/projects/ascend/en/v0.30.0/tutorials/models/DeepSeek-V4.1-Flash.html) |
| `--weight-transfer-config` | `WeightTransferConfig` | `None` | 权重传输配置（JSON）。RL 训练中 rollout→train 权重同步用。 | [docs×2](https://docs.vllm.ai/projects/ascend/en/latest/user_guide/feature_guide/rl.html) |
<!-- EA_TABLE_END -->

## 部署建议

| 场景 | 关键参数组合（来自官方教程） |
|---|---|
| 单卡 A2 小模型 | `--tensor-parallel-size 1 --max-model-len 32768 --gpu-memory-utilization 0.9 --max-num-seqs 32` |
| MoE 大模型 EP | `--enable-expert-parallel --data-parallel-size N --tensor-parallel-size M`（M×DP = 专家数） |
| 长上下文 | `--max-model-len 大值 --enable-chunked-prefill --max-num-batched-tokens 16384+` |
| PD 分离 | 每个节点 `--kv-transfer-config '{...}' --enable-prefix-caching/--no-enable-prefix-caching` |
| 生产服务 | 关闭 `--enforce-eager`（启用 CUDA Graph），配 `--compilation-config` 捕获策略 |

完整命令示例与逐模型部署指南见官方教程：[Model Deployment Tutorials](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/index.html)。

## 数据核验方式

- **参数存在性**：全部 78 个参数在 vLLM 源码 `add_argument()` 中有定义。
- **Ascend 语境**：每个参数至少在 vLLM-Ascend 官方文档的 1 个真实命令行中出现（`doc_count` 列给出文件数）。
- **默认值**：从 vLLM 源码 `EngineArgs`/`FrontendArgs` dataclass 及 `vllm/config/*.py` 提取；`None` 表示"自动推断"或"不设"。
- **说明**：中文说明为官方 help 文本的忠实翻译 + 官方教程实际用法补充；标注"官方教程"的内容均可溯源。
