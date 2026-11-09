---
title: kv-cache-dtype
---

# `--kv-cache-dtype`

> KV cache 存储量化类型——直接决定每 token KV 的显存占用，是"用精度换并发"的第一手段。

| 属性 | 值 |
|---|---|
| 类型 | `str`（CacheDType） |
| 默认值 | `"auto"`（跟随模型 dtype） |
| 分类 | 调度与内存 |

## 官方定义

> Data type for kv cache storage. If "auto", will use model data type. CUDA 11.8+ supports fp8 (=fp8_e4m3) and fp8_e5m2. ROCm (AMD GPU) supports fp8 (=fp8_e4m3). Intel Gaudi (HPU) supports fp8 (using fp8_inc). Some models (namely DeepSeekV3.2) default to fp8, set to bfloat16 to use bfloat16 instead...

（vLLM 源码：`CacheConfig.cache_dtype`，[cache.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/cache.py)）

## 机制详解

**量化对象是 KV cache，不是权重**：两者独立。权重量化由 [`--quantization`](quantization.md) 控制；本参数控制 attention 过程中 K/V 张量的存储格式。fp8 KV 相对 bf16 每 token 省一半显存，等效于把 KV 池容量翻倍。

**官方定义里的三个要点**（源码 docstring 直译）：

1. `auto` = 跟随模型权重 dtype；
2. **部分模型默认就是 fp8**（源码点名 DeepSeekV3.2）——这类模型想退回 bf16 要显式设 `bfloat16`；
3. 显式 `fp16`/`bfloat16` **必须与模型 dtype 一致**，否则报错；
4. 平台后端可通过 `register_kv_cache_dtype` 注册自定义 KV dtype——**Ascend 的 fp8/int8 KV 支持就走这个机制**。

## 参数联动

| 联动对象 | 关系 |
|---|---|
| `--attention_config.indexer_kv_dtype` | **Ascend 侧 C8 派生对**：v0.30.0 起，SFA 稀疏注意力模型的 C8 布局由本参数（cache_dtype ∈ {fp8, int8}）派生；Lightning Indexer 稀疏层的 C8 布局由 `indexer_kv_dtype ∈ {fp8, int8}` 派生——官方教程两者成对出现（如 `--kv-cache-dtype fp8 --attention_config.indexer_kv_dtype fp8`），P/D 两侧取值必须一致 |
| [`--gpu-memory-utilization`](gpu-memory-utilization.md) | KV 量化 = 等效扩大池容量；两者都是扩容手段，可叠加 |
| [`--block-size`](block-size.md) | 官方教程常组合配置（fp8 + block 32） |
| [`--max-num-seqs`](max-num-seqs.md) | 池子大了，同样并发下抢占更少 |
| 权重 NZ（[`weight_nz_mode`](../flags/weight-nz-mode.md)） | 别混淆：那是权重格式，本参数是 KV cache |
| Ascend 派生开关 | v0.30.0 起 `cache_dtype ∈ {fp8, int8}` 在 SFA 模型上派生 [`enable_sparse_sfa_c8`](../flags/enable-sparse-sfa-c8.md)；`cache_dtype == turboquant_4bit_nc` 派生 `enable_sparse_sfa_turboquant` |

**显存账**：KV 池能装的 token 数 ≈ 池容量 ÷（2 × 层数 × KV 头数 × 头维度 × 每元素字节数）。`kv-cache-dtype fp8` 把"每元素字节数"从 2 降到 1，容量直接 ×2。

## 调优思路

| 场景 | 建议 |
|---|---|
| MoE 大模型长上下文（官方教程主流） | fp8（参考 DeepSeek-V4-Pro 配方），关注精度回归 |
| 精度敏感 | auto / bfloat16，靠其他手段腾显存 |
| Mamba/SSM 类模型 | 对应参数是 `--mamba-ssm-cache-dtype`，默认 auto |

## Ascend 语境与官方用法

- 官方教程显式取值：
  - **fp8**——[DeepSeek-V4-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Pro.html)：`--kv-cache-dtype fp8`，并配 `--attention_config.indexer_kv_dtype fp8`
  - **int8** / **mxfp8**——见下节补丁扩展取值
- 注意精度与显存的权衡是显式的：fp8 KV 省一半显存，但需按业务验证精度。

## Ascend 补丁扩展取值（int8 / mxfp8）

上游 `CacheDType` 的合法取值（auto / fp8 / fp8_e5m2 / fp8_e4m3 / bf16 / fp16…）**不含 int8**。vLLM-Ascend 通过平台补丁 [`patch/platform/patch_kv_cache_dtype.py`](https://github.com/vllm-project/vllm-ascend/blob/main/vllm_ascend/patch/platform/patch_kv_cache_dtype.py) 把两个 Ascend 专属取值追加进 `CacheConfig.cache_dtype` 的 Literal——**同一个 `--kv-cache-dtype` 参数，在 Ascend 环境下多两个合法值**：

| 补丁值 | 含义 | 适用 |
|---|---|---|
| `int8` | KV cache 以 int8 存储 | DeepSeek V4 类稀疏 MLA 模型的 MLA KV cache；在 SFA 模型上派生 [`enable_sparse_sfa_c8`](../flags/enable-sparse-sfa-c8.md)（v0.30.0 起） |
| `mxfp8` | C8-MXFP 布局：FP8 KV + E8M0 scales | A5 芯片 QFA 路径（补丁注释原文 "the A5 QFA path"）；C8-MXFP 后端要求 512-token 页 |

**补丁机制**：改写 `CacheConfig` 的三处 Literal 引用（模块符号 `CacheDType`、类注解、dataclass 字段类型）后 `rebuild_dataclass(force=True)` 重建 pydantic 校验 schema；main 分支还同步追加 `KV_CACHE_DTYPES` 镜像列表（`is_known_kv_cache_dtype` 校验读它），CLI choices 在 `platform.py::pre_register_and_update` 一并加宽；worker 进程经 `patch/worker/patch_kv_cache_dtype.py` 二次套用。补丁幂等，可重复调用。

**坑**：离开 Ascend 环境这两个值不合法——校验逻辑由插件激活时注入，光看 vLLM 官方文档不知道它们存在。v0.30.0 的 `derive_and_validate` 已消费 `int8`（`cache_dtype in ["fp8", "int8"]` 派生 SFA-C8），即 int8 值域至少从 v0.30.0 起可用。

配套的 [`patch/platform/patch_indexer_kv_dtype.py`](https://github.com/vllm-project/vllm-ascend/blob/main/vllm_ascend/patch/platform/patch_indexer_kv_dtype.py) 对 `--attention_config.indexer_kv_dtype` 做同样的事：上游 Literal 为 `auto / bf16 / fp8 / mxfp4 / nvfp4`，补丁追加 `int8`（DeepSeek V4 Ascend indexer K cache）。这也是 v0.30.0 起 `indexer_kv_dtype ∈ {fp8, int8}` 派生 LI-C8 的前提。

## 用法

```bash
vllm serve deepseek-ai/DeepSeek-V3.2 --kv-cache-dtype fp8 --block-size 32
```

## 相关参数

- [`--quantization`](quantization.md) — 权重量化（与本参数独立）
- [`--block-size`](block-size.md) — 官方教程常组合配置
- [`--mamba-ssm-cache-dtype`](index.md) — Mamba 类模型的对应参数
