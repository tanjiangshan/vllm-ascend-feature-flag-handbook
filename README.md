# vLLM-Ascend 特性开关手册

**Languages: [English](#english) | 中文**

> 🌐 **在线文档站**：<https://tanjiangshan.github.io/vllm-ascend-feature-flag-handbook/>
>
> 🌐 **Online docs site**: <https://tanjiangshan.github.io/vllm-ascend-feature-flag-handbook/>

社区维护的 vLLM-Ascend 特性开关（Feature Flags）深度参考手册，以「代码仓驱动文档站」的形式组织：

- **数据源**：`data/flags/*.yaml`，每个开关一个文件，标注类型 / 默认值 / 状态 / 迁移来源 / 适用芯片
- **自动生成**：`scripts/generate_tables.py` 从 YAML 生成中英双语总览表、缺失详情页的占位页、机器可读的 `docs/flags.json`
- **文档站**：MkDocs Material + mkdocs-static-i18n 中英双语，GitHub Actions 自动部署到 GitHub Pages

> 本手册是[官方文档](https://docs.vllm.ai/projects/ascend/en/latest/)的社区补充，不替代官方文档。冲突时以官方为准，欢迎提 issue 修正。

## 内容范围

| 模块 | 说明 |
|---|---|
| [特性开关总览](docs/flags/index.md) | `--additional-config` 全量配置键速查表（51 个开关，全部含手写详情页） |
| [引擎参数](docs/engine-args/index.md) | 78 个 `vllm serve` 参数的 Ascend 语境用法（官方文档实证 + 源码默认值），20 个重点参数含机制详解/联动/调优 |
| [版本支持矩阵](docs/version-matrix.md) | 每个开关在 v0.23.0 / v0.30.0 / main 的支持情况（源码核验） |
| [迁移对照表](docs/migration.md) | PR #9064 起 10+ 个环境变量 → 配置键的迁移速查 |
| [环境变量](docs/env-vars.md) | 仍独立生效的运行时 / 构建期环境变量 |
| [版本历史](docs/version-history.md) | 各版本开关的引入、弃用与移除记录 |
| [贡献指南](docs/contributing.md) | 如何新增 / 修正开关条目 |

## 快速开始

```bash
pip install -r requirements.txt
python scripts/generate_tables.py   # YAML 校验 + 生成表格/占位页/flags.json
mkdocs serve                        # 本地预览 http://127.0.0.1:8000
```

## 仓库结构

```
├── data/flags/            # 单一事实来源：每个开关一个 YAML
├── data/engine-args.yaml  # 78 个引擎参数（官方文档实证 + 源码默认值）
├── docs/                  # MkDocs 文档源（中英 *.md / *.en.md）
│   ├── flags/             # 每个开关的详情页（全部手写）
│   └── engine-args/       # 引擎参数总览 + 20 个重点参数详情页
├── scripts/generate_tables.py
├── scripts/audit_engine_args.py  # 溯源审计（参数∈vLLM CLI、示例值∈官方文档）
├── docs/flags.json        # 机器可读导出（自动生成，勿手改）
├── mkdocs.yml             # MkDocs Material + i18n 双语配置
└── .github/workflows/     # CI 校验 + GitHub Pages 自动部署
```

## 发布前必改

1. `mkdocs.yml`：将 `site_url` / `repo_url` / `extra.social.link` 中的 `tanjiangshan` 替换为实际 GitHub 组织或用户名；
2. `docs/index.md`、`docs/index.en.md`、`docs/flags/index.md` 等页中的 GitHub 链接同理；
3. 推送 `main` 分支后，在仓库 Settings → Pages 中选择 **GitHub Actions** 作为来源（workflow 已配置好）。

## 许可证

[CC BY-SA 4.0](LICENSE)（文档类许可；按相同方式共享，需署名）

---

## English

A community-maintained deep reference of [vLLM-Ascend](https://github.com/vllm-project/vllm-ascend) feature flags, organized as a repo-driven documentation site:

- **Data source**: `data/flags/*.yaml` — one file per flag, tracking type / default / status / legacy env var / applicable hardware
- **Auto-generated**: `scripts/generate_tables.py` renders bilingual overview tables, stubs missing detail pages, and exports a machine-readable `docs/flags.json`
- **Site**: MkDocs Material + mkdocs-static-i18n (zh/en), deployed to GitHub Pages via GitHub Actions

> This handbook is a community supplement to the [official docs](https://docs.vllm.ai/projects/ascend/en/latest/), not a replacement. When in doubt, trust the official docs — and please open an issue here.

**Contents**: [feature flags overview](docs/flags/index.md) (51 flags, all with hand-written detail pages) · [engine args](docs/engine-args/index.md) (78 `vllm serve` args with Ascend context; 20 key args with deep mechanism/interplay/tuning pages) · [version support matrix](docs/version-matrix.md) (v0.23.0 / v0.30.0 / main, verified against source) · [env-var migration table](docs/migration.md) · [environment variables](docs/env-vars.md) · [version history](docs/version-history.md) · [contributing](docs/contributing.md)

**Quick start**:

```bash
pip install -r requirements.txt
python scripts/generate_tables.py
mkdocs serve
```

**License**: [CC BY-SA 4.0](LICENSE)
