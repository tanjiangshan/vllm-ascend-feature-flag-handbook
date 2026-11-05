---
title: 贡献指南
---

# 贡献指南

## 仓库结构

```
├── data/flags/            # 单一事实来源：每个开关一个 YAML
├── docs/                  # MkDocs 文档源文件
│   └── flags/             # 每个开关的详情页（可手写，缺失时自动生成占位页）
├── scripts/generate_tables.py   # 从 YAML 生成总览表 + 占位页 + flags.json
├── docs/flags.json        # 机器可读导出（自动生成，勿手改）
└── mkdocs.yml
```

## 新增一个开关

1. 在 `data/flags/` 新建 `<key>.yaml`，必填字段：

```yaml
key: enable_xxx
type: bool            # bool | int | float | str | dict | list
default: false
status: active        # active | deprecated | removed | planned
version_support:      # 在三个版本中的支持情况（true/false）
  v0.23.0: false
  v0.30.0: true
  main: true
desc:
  zh: 一句话中文说明。
  en: One-line English description.
```

   常用可选字段：`legacy_env`（迁移前环境变量）、`hardware`（适用芯片列表）、`models`（适用模型）、`requires` / `conflicts`（关联开关）、`values`（取值含义表）、`version_note`（版本相关备注，中英双语）、`source`（源码出处）。

2. 运行生成脚本：

```bash
pip install -r requirements.txt
python scripts/generate_tables.py
```

   脚本会：校验 YAML → 更新总览表 → 为缺少详情页的开关生成占位页 → 导出 `flags.json`。

3. （推荐）把占位页 `docs/flags/<key>.md` 扩写成完整详情页：原理、用法示例、适用场景、风险、与其他开关的组合关系。
4. 提交 PR。CI 会重新生成并校验一致性。

## 修改现有开关

- **改默认值/状态/迁移信息**：只改 `data/flags/*.yaml`，不要手改总览表（会被覆盖）。
- **改详情页内容**：直接编辑 `docs/flags/*.md` 对应文件。
- **脚本运行后 `docs/flags.json` 与 `docs/includes` 的变更需要一并提交**，CI 中 `git diff --exit-code` 会检查。

## 内容准则

1. **准确性优先**：默认值、状态、芯片适配必须有据可查（官方文档、源码、release notes），在 YAML 的 `source` 字段注明出处。
2. **与官方文档冲突时以官方为准**：发现冲突请同时向本仓提 issue。
3. **风险必须显式标注**：会破坏精度、仅限分析用途、有内存开销的开关，在详情页用 `!!! warning` 提示。
4. **中英双语**：YAML 的 `desc` 必须中英都填；详情页正文可先中文，欢迎补充英文。

## 本地预览

```bash
mkdocs serve
```

访问 <http://127.0.0.1:8000>。
