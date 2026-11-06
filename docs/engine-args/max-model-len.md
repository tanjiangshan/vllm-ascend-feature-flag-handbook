---
title: max-model-len
---

# `--max-model-len`

> 模型服务的最大上下文长度（prompt + output）——超长请求会被直接拒绝。

| 属性 | 值 |
|---|---|
| 类型 | `int`（支持 `k/m/g/t` 后缀简写） |
| 默认值 | `None`（从模型 config 自动推断） |
| 分类 | 调度与内存 |

## 官方定义

> Model context length (prompt and output). If unspecified, will be automatically derived from the model config.

（vLLM 源码：`ModelConfig.max_model_len`，[model.py](https://github.com/vllm-project/vllm/blob/main/vllm/config/model.py)）

## 机制详解

**两条生效路径**：

1. **不显式设置**：取模型 config 里的上下文上限（不同模型来源不同——`max_position_embeddings`、rope 推导值等，以实际 config 为准）；
2. **显式设置**：作为服务级硬上限。超过它的请求在**准入时直接拒绝**（报错提示序列过长），不会进入调度。

**k/m/g/t 后缀简写**：vLLM 的 CLI 层会把裸数字后缀展开（[`human_readable_int`](https://github.com/vllm-project/vllm/blob/main/vllm/utils/argparse_utils.py)，且 JSON 参数里的同类写法也会被 [`_expand_json_human_readable_numbers`](https://github.com/vllm-project/vllm/blob/main/vllm/engine/arg_utils.py) 展开）：

| 写法 | 含义 | 结果 |
|---|---|---|
| `--max-model-len 128k` | 小写 = 十进制 | 128000 |
| `--max-model-len 128K` | 大写 = 二进制 | 131072 |

> ⚠️ 大小写语义不同：小写 `k/m/g/t` 是 10 的幂，大写 `K/M/G/T` 是 2 的幂。写配置时注意区分。

## 参数联动

**与 KV cache 容量的关系**：每条序列的最大显存需求 ≈ `max_model_len × 每 token KV 占用`。它直接决定"一条序列最多能占多少 KV"，因此是 KV 池规划的第一输入：池子至少要能同时容纳若干条接近 `max_model_len` 的序列，否则并发能力趋近于零。

**与 `max_num_batched_tokens` 的启动校验**（[scheduler.py `verify_max_model_len`](https://github.com/vllm-project/vllm/blob/main/vllm/config/scheduler.py)）：

```
关闭 chunked prefill 时：max_num_batched_tokens < max_model_len → 启动报错
```

原因：不开分块时，单条 prefill 必须在一步内完成，预算必须装得下最长序列。开启 chunked prefill 后该约束解除——这也是长上下文部署几乎都开 chunked prefill 的原因。

**与抢占的关系**：`max_model_len` 越大，单条序列可能占用的 KV 越多，长请求混部时越容易把池子顶满触发 `vllm:num_preemptions`。缩小它是最直接的"给并发腾地方"手段。

## 调优思路

| 场景 | 建议 |
|---|---|
| 长文档/Agent 场景 | 按业务最大输入 + 最大输出设置；宁可拒绝超长请求也不要让全局长度膨胀拖垮所有人 |
| 显存紧张 | 优先缩小本参数（等价于限制单请求峰值），其次降并发 |
| 与官方教程对齐 | 大模型教程普遍显式设置（见下），照抄模型对应教程值最稳妥 |

## Ascend 语境与官方用法

- 官方教程几乎全部**显式设置**（它是 KV cache 显存压力的第一决定因素）：
  - [DeepSeek-V4-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/DeepSeek-V4-Flash.html) / [GLM5.3-Flash](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.3-Flash.html) / [Kimi-K3.1-Pro](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.1-Pro.html)：`1048576`（1M）
  - [GLM5](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/GLM5.html) / [Kimi-K3](https://docs.vllm.ai/projects/ascend/en/latest/tutorials/models/Kimi-K3.html)：`131072`
  - 其他如 `133120`、`135168`、`40000` 等按模型裁剪的值
- 长 prefill 在 Ascend 上可叠加 [`prefill-context-parallel-size`](prefill-context-parallel-size.md) 进一步切分到多卡（见该页兼容性矩阵）。

## 用法

```bash
vllm serve Qwen/Qwen3-8B --max-model-len 131072
vllm serve Qwen/Qwen3-8B --max-model-len 128K   # 131072
```

## 相关参数

- [`--max-num-batched-tokens`](max-num-batched-tokens.md) — 关闭 chunked prefill 时的启动约束
- [`--enable-chunked-prefill`](enable-chunked-prefill.md) — 解除上述约束的关键
- [`--prefill-context-parallel-size`](prefill-context-parallel-size.md) — 长上下文 prefill 的多卡加速
- [`--gpu-memory-utilization`](gpu-memory-utilization.md) — KV 池总容量的来源
