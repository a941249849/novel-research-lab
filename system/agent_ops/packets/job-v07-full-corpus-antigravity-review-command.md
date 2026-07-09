# 交给 Antigravity 的命令包：NRL 全量小说集重读 v0.7

你现在在本机共享项目目录 `Novel Research Lab` 中工作。请执行一次中文玄幻小说全量重读与结构化审查，目标不是写正文，而是为 Novel Research Lab 的 Corpus-to-Creation 系统补全可摄取的研究资产。

## 固定系统身份

- 系统名：Novel Research Lab
- 当前原创项目：《借天改命账》
- 架构基线：v0.4 十层架构
- 当前运行模式：SYSTEM_HARDENING
- 内容推进状态：FROZEN_AT_OWNER_GATE
- Hermes：paused_not_removed，不要调用，不要代替 Hermes 写作
- Codex：本地 runtime / 工程 / 校验 / 编排
- Antigravity：人工外部文学审查 / 全量小说集重读 / 长篇生命力评估

## v0.4 十层架构

1. corpus_layer / 语料层
2. single_book_decomposition / 单书拆解层
3. cross_book_distillation / 跨书蒸馏层
4. research_asset_engine / 研究资产引擎
5. original_project_synthesis / 原创项目综合层
6. long_form_creation_asset_os / 长篇创作资产系统
7. planning_pipeline / 规划管线层
8. agent_review_and_production / Agent 审查与生产层
9. runtime_control_plane / Runtime / Control Plane 层
10. studio_cockpit / Studio 驾驶舱层

## 你的任务

请基于本机项目中已有的小说集与 Phase 1 结构化资产，做全量重读、重分析、重规划。输出必须服务于这条链路：

小说集阅读拆解 -> 单书 DNA -> 跨书机制蒸馏 -> 创作母库 -> 新书生成

你需要重点提炼：

- 长篇追更机制
- 升级与压力循环
- 人物成长与关系推进
- NPC / 群像 / 小人物可复用结构
- 势力扩张、利益冲突和裂缝
- 道具、招式、境界、代价、反制
- 命名体系和避免撞名的规则
- 情感羁绊、牺牲、背叛、偿还
- 伏笔、误导、揭示、回收
- 状态账本需要记录的变量

## 九类创作资产必须全部覆盖

- `characters`
- `npcs`
- `factions`
- `artifacts`
- `techniques`
- `naming`
- `emotional_bonds`
- `foreshadowing`
- `state_ledger`

如果某一类证据不足，请标记为 `missing` 并说明原因，不要编造。

## 输出边界

禁止：

- 写小说正文
- 写第一章
- 写章节大纲
- 生成最终人物卡
- 生成最终招式树
- 生成最终命名词典
- 声称 Hermes 已经运行或完成写作
- 复制或引用原文大段内容

允许：

- 抽象机制
- 结构化证据
- 风险判断
- 可原创迁移建议
- 缺口说明
- 后续 Codex 摄取建议

## 必须输出的 Markdown 标题

## Job ID
## Scope
## Corpus Coverage
## Cross-Book Mechanisms
## Creation Asset Evidence
## Originality Risk
## Recommended Next Ingestion
## JSON Manifest

## JSON Manifest 要求

在 `## JSON Manifest` 下输出一个 fenced `json` 代码块，字段必须包含：

```json
{
  "job_id": "job-v07-full-corpus-antigravity-review",
  "contract_version": "0.7",
  "review_scope": "full_remaining_corpus",
  "architecture_version": "0.4",
  "corpus_policy": {
    "raw_prose_quoted": false,
    "abstract_mechanisms_only": true
  },
  "book_reviews": [],
  "cross_book_mechanisms": [],
  "asset_family_evidence": {
    "characters": {},
    "npcs": {},
    "factions": {},
    "artifacts": {},
    "techniques": {},
    "naming": {},
    "emotional_bonds": {},
    "foreshadowing": {},
    "state_ledger": {}
  },
  "originality_risks": [],
  "recommended_next_ingestion": {}
}
```

请把最终结果保存到：

```text
system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md
```

注意：这不是作文任务，不是章节任务，不是 Hermes 写作任务。你的产物必须能被 Codex 校验和摄取。
