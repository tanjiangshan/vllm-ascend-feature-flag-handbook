---
title: 部署配方
---

# 部署配方（官方推荐命令速查）

> 所有命令逐字摘自 vLLM-Ascend 官方文档（main 分支），每条附官方原文链接。**官方教程会随版本更新，命令以原文为准**；本站每次同步时重新生成本区。

## 按模型/场景分类

| 分类 | 内容 |
|---|---|
| [DeepSeek 系列](deepseek.md) | V4-Flash / V4-Pro / V4.1-Flash（dspark 投机、PCP、ascend 量化） |
| [Kimi 系列](kimi.md) | K2.6 / K3 / K3.1-Pro（dspark + FULL_DECODE_ONLY、NetLoader） |
| [GLM 系列](glm.md) | GLM5 / GLM5.2 / GLM5.3-Flash（w4a4c8-mxfp4 950 量化、PCP+DCP） |
| [Qwen 系列](qwen.md) | Qwen3 Dense/MoE/VL/超大模型 9 组（MP 单机到 Ray 多机） |
| [MiniMax 系列](minimax.md) | M3 / M3.1-Flash |
| [其他模型](others.md) | Cohere / Dots3 / Gemma4 / Hy4 / SigLIP2 / Step-5 |
| [特性场景](features.md) | PD 分离（Mooncake）/ Ray 多机 / 后缀投机解码 |

## 如何使用

1. 打开对应分类页，展开模型卡片，复制完整命令；
2. 命令中的 `$MODEL_PATH`、`$PORT` 等变量需替换为你的实际值（官方原文中有对应的环境变量设置段）；
3. 每条命令里的 `--additional-config` 键可参考[特性开关总览](../flags/index.md)，引擎参数可参考[引擎参数总览](../engine-args/index.md)。

## 数据核验

- 命令逐字摘录自官方文档代码块（仅做换行规范整理）；
- 每条卡片的"官方原文"链接指向 docs.vllm.ai 的对应教程页；
- `data/recipes.json` 由脚本从官方文档提取生成，禁止手改命令。
