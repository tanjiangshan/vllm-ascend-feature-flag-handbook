# AGENTS.md

vLLM-Ascend 特性开关手册（社区文档站）。本文件面向代码代理/贡献者，说明仓库结构、构建方式与约定。

## 项目定位

- 社区维护的 vLLM-Ascend 特性开关深度参考，**补充而非替代**[官方文档](https://docs.vllm.ai/projects/ascend/en/latest/)；冲突时以官方为准。
- 内容数据源是 `data/flags/*.yaml`（每个开关一个文件），文档站由脚本从 YAML 自动生成。

## 目录结构

```
data/flags/                # 单一事实来源：52 个开关的 YAML
scripts/generate_tables.py # 校验 YAML → 生成总览表/版本矩阵/flags.json
docs/                      # MkDocs 文档源（中文 *.md / 英文 *.en.md 成对）
docs/flags/                # 每个开关一个详情页（全部手写，不再生成占位页）
docs/flags.json            # 机器可读导出（自动生成，勿手改）
mkdocs.yml                 # MkDocs Material + mkdocs-static-i18n（zh 默认，en 次语言）
.github/workflows/         # ci.yml（PR 校验）+ deploy.yml（main 分支发布 Pages）
```

## 构建与验证

```bash
pip install -r requirements.txt
python scripts/generate_tables.py   # 校验 + 生成；任何 YAML 错误都会以非零码退出
mkdocs build --strict               # 全站构建，warning 即失败
mkdocs serve                        # 本地预览
```

CI 会先跑生成脚本，再检查 `git diff --exit-code -- docs/includes docs/flags.json`（生成物必须随 PR 提交），最后 `mkdocs build --strict`。

## YAML 数据约定（data/flags/*.yaml）

必填字段：`key`、`type`（bool/int/float/str/dict/list）、`default`、`status`（active/deprecated/removed/planned）、`version_support`（恰好包含 `v0.23.0`/`v0.30.0`/`main` 三个布尔键）、`desc.zh` + `desc.en`。

常用可选字段：`legacy_env`、`hardware`（A1–A5 列表）、`models`、`requires`、`conflicts`、`values`、`version_note`（中英双语）、`source`。

`version_support` 的核验方式：比对对应 tag 的 `vllm_ascend/envs.py` 与 `vllm_ascend/ascend_config.py`，源码拆分无法确认的以官方配置文档交叉验证。**禁止未经源码核验填写版本信息**；核验不了就提 issue 求助。

## 零编造铁律

1. **每个开关的 `key` 必须能在源码或官方文档中找到**（`ascend_config.py`、`envs.py` 或 docs.vllm.ai 配置页），找不到就不得收录。
2. **`default` 必须与源码或官方文档表格一致**；文档写 `false`/`true`（小写）时，本站渲染也用同款小写。
3. **只有环境变量形态的配置不设 `key`**（如 `VLLM_ASCEND_ENABLE_BATCH_MEMCPY`），在 `docs/env-vars.md` 介绍即可，不进开关数据库——宁可少收录，不可造键名。
4. 新增开关时的自查脚本（比对本地留存的 release 源码与官方文档）应随 PR 附上输出；核验材料统一放在 `/tmp/opencode/ver-check/`（CI 中可重新抓取）。

## 内容准则

1. 默认值/状态/版本必须有据可查（官方文档、release tag 源码），YAML `source` 字段注明出处。
2. 破坏精度、仅限分析、有内存开销的开关，详情页必须用 `!!! warning` / `!!! danger` 标注。
3. 中英双语：YAML `desc` 双语必填；正文页面可先中文，欢迎补英文。
4. 详情页之间用「相关开关」小节互链，保持导航闭环。

## 发布 checklist（仓库所有者）

1. `git init` + 首次推送 main 分支；仓库 Settings → Pages 选 **GitHub Actions**。
2. 新版本发布后在 `data/flags/*.yaml` 更新 `version_support` 并复核版本矩阵。

## 已知注意事项

- Material 主题 2027-05 停止维护，后继者为 Zensical；迁移前维持现状即可。
- `deploy.yml` 使用 `mkdocs gh-deploy --force` 推送 gh-pages 分支，需 `contents: write` 权限（已配置）。
- 本地 `.venv/` 为 Python 3.14 + get-pip 引导的虚拟环境，已 gitignore。
