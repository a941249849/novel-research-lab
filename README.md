# Novel Research Lab

Novel Research Lab（NRL）是面向中文长篇网文的 **Corpus-to-Creation** 引擎。它不是通用写作面板，也不是对既有小说进行句式模仿：系统先把授权语料拆解为可追溯的叙事机制与 DNA 资产，再编译为原创项目资产、十章故事窗口、逐章上下文、正文、审查和状态结算。

## 当前状态

- 项目：`《借天改命账》`
- 长篇规格：18 卷、约 1,800 章、600–680 万中文字符
- 语料：18 本、143 个连续分块、18 本综合与跨书蒸馏均已完成哈希和覆盖验证
- 创作资产：九类 Schema 与项目资产库已可运行
- 正文：第 1–20 章已接受；`011–020` 窗口独立复审为 `ACCEPT`
- 当前入口：编译 `021–030` 故事窗口后，从第 21 章恢复受控生产
- 发布状态：禁止发布，直至第一卷完成整卷复审并通过 Owner Gate

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

Codex 是工程主控、故事编译器、正文写手、事实观察器和状态结算器。Antigravity 仅承担关键节点的独立文学审查。Hermes 是可选文学增强器，不是生产链依赖。Owner 保留范围授权与发布权。

## 唯一事实源

| 领域 | 路径 |
| --- | --- |
| 当前阶段与授权 | `system/mission_controller/current_phase_state.json`、`system/runtime/owner_gate_decisions.json` |
| 研究蒸馏 | `system/research_assets/deep_read/v0.18/`、`system/research_assets/promotions/` |
| 项目创作资产 | `system/creation_assets/project_assets.v0.2.json` |
| 长篇契约 | `system/production_runtime/plans/borrowed_heaven_longform_contract.v0.1.json` |
| 十章故事窗口 | `system/production_runtime/story_windows/` |
| 章节执行状态 | `system/production_runtime/chapter_registry.v0.20.json` |

`phase0*`、`phase1*`、`phase2*` 和 `docs/superpowers/` 是只读历史谱系，不是活动控制面。章节 Runtime 不得读取 `novel_training_set/` 原文。

## 运行

```bash
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py story-window-status
python3 system/runtime/nrl.py production-preflight
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py chapter-runtime-status
python3 system/runtime/nrl.py studio-serve --port 4173
```

受控生产单章：

```bash
python3 system/runtime/nrl.py story-window-build --start 21
python3 system/runtime/nrl.py chapter-run \
  --intent-file system/production_runtime/intents/longform_volume1_v025/chapter-0021.v0.25.json
```

系统只允许严格顺序生产。每章必须经过：意图、上下文编译、正文、审查、修订、事实观察、终审、状态结算、接受。每 5 章触发独立文学深审，每 10 章必须完成窗口复审；没有下一十章故事窗口时自动停止。
