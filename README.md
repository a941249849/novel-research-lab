# Novel Research Lab

Novel Research Lab（NRL）是面向中文长篇网文的 **Corpus-to-Creation** 引擎。它不是通用写作面板，也不是对既有小说进行句式模仿：系统先把授权语料拆解为可追溯的叙事机制与 DNA 资产，再编译为原创项目资产、十章故事窗口、逐章上下文、正文、审查和状态结算。

## 当前状态

- 系统：支持按 `project_id` 隔离的多项目 Corpus-to-Creation 生产
- 首个项目实例：`borrowed-heaven` / `《借天改命账》`
- 长篇规格：18 卷、约 1,800 章、600–680 万中文字符
- 语料：18 本、143 个连续分块、18 本综合与跨书蒸馏均已完成哈希和覆盖验证；166 项晋级产物由独立根哈希绑定
- 创作资产：九类 Schema 与项目资产库已可运行
- 正文：第一卷 100 章均已接受，正文约 32.7 万中文字符
- 审查：每十章一个哈希绑定审查窗口；任何正文编辑都会使旧审查自动失效
- 当前入口：`volume1-release-status` 是第一卷发布事实入口
- 发布包：由已接受正文、发布编辑和独立标题资产按需生成，不作为 Git 事实源

## 固定架构

1. 受保护语料层
2. 单书拆解层
3. 跨书机制蒸馏层
4. 研究资产检索层
5. 原创项目综合层
6. 长篇创作资产系统
7. 十章故事编译与逐章规划层
8. Agent 审查与正文生产层
9. Runtime / Control Plane
10. Studio 只读视图

Codex 是唯一主生产平面：Sol 负责长线规划与高风险审校，Terra 负责正文与有界修订，Luna 负责事实观察、状态抽取和机械检查。Antigravity 仅承担独立复核与提供方故障备用。Hermes 已退出当前架构，不再拥有写作或门禁角色。Owner 保留范围授权与发布权。

## 唯一事实源

| 领域 | 路径 |
| --- | --- |
| 当前阶段与授权 | `system/mission_controller/current_phase_state.json`、`system/runtime/owner_gate_decisions.json` |
| 研究蒸馏 | `system/research_assets/deep_read/v0.18/`、`system/research_assets/promotions/`；`promotion_attestation.json` 支持不挂载原文的只读生产验证 |
| 项目注册表 | `system/projects/registry.v1.json`、`system/projects/<project_id>/project.json` |
| 新项目工作区 | `projects/<project_id>/` |
| 首项目创作资产（兼容迁移） | `system/creation_assets/project_assets.v0.2.json` |
| 长篇契约 | `system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json` |
| 十章故事窗口 | `system/production_runtime/story_windows/` |
| 章节执行状态 | `system/production_runtime/chapter_registry.v0.20.json` |
| 发布编辑 | `system/production_runtime/release_edits/` |
| 十章发布审查 | `system/production_runtime/window_reviews/` |
| 第一卷章节标题 | `system/production_runtime/chapter_titles.volume1.json` |

`phase0*`、`phase1*`、`phase2*` 和 `docs/superpowers/` 是只读历史谱系，不是活动控制面。章节 Runtime 不得读取 `novel_training_set/` 原文。

## 运行

```bash
python3 system/runtime/nrl.py projects
python3 system/runtime/nrl.py project-status --project borrowed-heaven
python3 system/runtime/nrl.py production-status --project borrowed-heaven
python3 system/runtime/nrl.py produce --until 100 --project borrowed-heaven
python3 system/runtime/nrl.py volume1-release-status --project borrowed-heaven
python3 system/runtime/nrl.py volume1-fanqie-package --project borrowed-heaven
```

创建另一本原创小说时，先建立完全隔离的项目实例；初始化不会生成正文或复用《借天改命账》的设定：

```bash
python3 system/runtime/nrl.py project-init --project-id new-book --title '《新书名》' --genre '玄幻'
python3 system/runtime/nrl.py project-validate --project new-book
python3 system/runtime/nrl.py project-status --project new-book
```

`production-status` 是日常状态入口；`produce` 会从首个未接受章节恢复，自动编译缺失的十章窗口，并在章节门禁、十章复审或外部模型失败时停止。诊断和只读控制台仍可使用：

```bash
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py deep-read-status
python3 system/runtime/nrl.py production-preflight
python3 system/runtime/nrl.py studio-serve --port 4173
```

系统只允许严格顺序生产。每章必须经过：意图、上下文编译、正文、审查、修订、事实观察、终审、状态结算、接受。每 5 章触发独立文学深审，每 10 章必须完成窗口复审；没有下一十章故事窗口时自动停止。

受保护原文只在研究重验环境挂载。晋级前用 `deep-read-attest` 重新核对原文与计划并生成哈希凭证；日常生产和 CI 只校验该凭证及 166 项已晋级产物，不要求把原文提交到 Git。

## 产物保留

章节执行中的上下文、规则栈、草稿、审查包和失败回执属于可再生工作缓存。章节接受后只长期保留意图、终稿、终稿指标、事实观察、终审、状态结算和验收记录。可先预览、再执行压缩：

```bash
python3 system/runtime/nrl.py production-compact
python3 system/runtime/nrl.py production-compact --apply
```

`system/releases/review/`、`system/releases/fanqie/`、`system/runtime/studio/`、`apps/studio/dist/`、`.nrl-work/` 和依赖目录均为可再生产物，不进入 Git。历史 `phase*` 文件只承担研究谱系，不参与日常生产。
候选项目研究可以通过研究资产目录查询，但候选条目不会自动初始化项目或授权正文：

```bash
python3 system/runtime/nrl.py research-assets --asset-type candidate_craft_research
python3 system/runtime/nrl.py research-assets --asset-type candidate_source_ecology
python3 system/runtime/nrl.py research-assets --asset-type candidate_regional_evidence
python3 system/runtime/nrl.py research-assets --category 木作与古建营造
```
