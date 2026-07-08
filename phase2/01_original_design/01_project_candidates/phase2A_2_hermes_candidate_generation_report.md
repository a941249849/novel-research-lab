# Phase 2A-2 Hermes Candidate Generation Report

- generated_at: 2026-07-08T07:33:26
- executor: Hermes
- phase: Phase 2A-2 — Controlled Original Project Candidate Generation
- status: completed_controlled_candidates

## 本次任务做了什么

在 Owner 已批准 Phase 2A-2 的授权范围内，基于 Core7 正式机制库与 Phase 2A 受控设计文件，生成 exactly 3 个原创项目候选，并写入：

- `phase2/01_original_design/01_project_candidates/project_candidate_01.yaml`
- `phase2/01_original_design/01_project_candidates/project_candidate_02.yaml`
- `phase2/01_original_design/01_project_candidates/project_candidate_03.yaml`
- `phase2/01_original_design/01_project_candidates/phase2A_2_hermes_candidate_generation_report.md`

## 读取了哪些允许文件
- `system_master_spec_v0.1.md`
- `phase1/05_review/phase1C_owner_acceptance_package.md`
- `phase1/05_review/phase1C_owner_acceptance_record.md`
- `phase1/04_mechanism_library/core7_mechanism_inventory.json`
- `phase1/04_mechanism_library/category_manifest.json`
- `phase1/03_features/cross_book_feature_notes.md`
- `phase2/00_entry/phase2A_entry_plan.md`
- `phase2/00_entry/phase2A_input_assets.md`
- `phase2/00_entry/phase2A_tool_roles.md`
- `phase2/00_entry/phase2A_red_lines.md`
- `phase2/05_review/phase2A_antigravity_planning_review.md`
- `phase2/01_original_design/00_design_brief/phase2A_controlled_original_design_brief.md`
- `phase2/01_original_design/00_design_brief/mechanism_recipe_selection_policy.md`
- `phase2/01_original_design/00_design_brief/original_project_option_template.md`
- `phase2/01_original_design/00_design_brief/hermes_controlled_prompt_draft.md`
- `phase2/01_original_design/00_design_brief/phase2A_design_validation_checklist.md`
- `phase2/05_review/phase2A_1_controlled_design_brief_report.md`
- `phase2/05_review/phase2A_1_antigravity_design_brief_review.md`
- `phase1/02_book_dna/遮天_dna.json`
- `phase1/02_narrative_dna/遮天_narrative.json`
- `phase1/02_state_ledgers/遮天_ledger.json`
- `phase1/02_book_dna/蛊真人_dna.json`
- `phase1/02_narrative_dna/蛊真人_narrative.json`
- `phase1/02_state_ledgers/蛊真人_ledger.json`
- `phase1/02_book_dna/人道至尊_dna.json`
- `phase1/02_narrative_dna/人道至尊_narrative.json`
- `phase1/02_state_ledgers/人道至尊_ledger.json`
- `phase1/02_book_dna/凡人修仙传_dna.json`
- `phase1/02_narrative_dna/凡人修仙传_narrative.json`
- `phase1/02_state_ledgers/凡人修仙传_ledger.json`
- `phase1/02_book_dna/斗破苍穹_dna.json`
- `phase1/02_narrative_dna/斗破苍穹_narrative.json`
- `phase1/02_state_ledgers/斗破苍穹_ledger.json`
- `phase1/02_book_dna/诡秘之主_dna.json`
- `phase1/02_narrative_dna/诡秘之主_narrative.json`
- `phase1/02_state_ledgers/诡秘之主_ledger.json`
- `phase1/02_book_dna/求魔_dna.json`
- `phase1/02_narrative_dna/求魔_narrative.json`
- `phase1/02_state_ledgers/求魔_ledger.json`

## 没有读取哪些禁止文件

- 未读取 `novel_training_set/`
- 未读取任何原著全文
- 未读取 11 本未 promoted 的 stub 作为正式机制来源
- 未读取未经 Owner 批准的新外部资料
- 未读取任何用于模仿原文风格的文本

## 生成的 3 个候选

1. `project_candidate_01.yaml` — 《潮汐税簿》
2. `project_candidate_02.yaml` — 《无声巡夜社》
3. `project_candidate_03.yaml` — 《群岛无名碑》

## 每个候选选择的 mechanism_id

### Candidate 01 — 《潮汐税簿》
- main: GMZZ-M3, RDZZ-M3, GZR-M2
- auxiliary: FRXXZ-M2, ZT-M2, GMZZ-M4
- constraint: GZR-M4, FRXXZ-M4

### Candidate 02 — 《无声巡夜社》
- main: GMZZ-M1, GMZZ-M2, DPCQ-M4
- auxiliary: FRXXZ-M3, QM-M3, GZR-M3
- constraint: GMZZ-M3, DPCQ-M2

### Candidate 03 — 《群岛无名碑》
- main: QM-M2, RDZZ-M1, ZT-M4
- auxiliary: RDZZ-M2, FRXXZ-M1, DPCQ-M2
- constraint: GZR-M5, QM-M5

## 明确边界结果

- 是否生成正文：否
- 是否写第一章：否
- 是否写具体场景：否
- 是否写对话：否
- 是否写文风样章：否
- 是否启动 18 本全量：否
- 是否读取 `novel_training_set`：否
- 是否使用 11 本 stub：否

## 自检结果

```json
[
  {
    "candidate": "project_candidate_01.yaml",
    "total_mechanisms": 8,
    "main": 3,
    "auxiliary": 3,
    "constraint": 2,
    "source_books": {
      "诡秘之主": 2,
      "人道至尊": 1,
      "蛊真人": 2,
      "凡人修仙传": 2,
      "遮天": 1
    },
    "passes": true
  },
  {
    "candidate": "project_candidate_02.yaml",
    "total_mechanisms": 8,
    "main": 3,
    "auxiliary": 3,
    "constraint": 2,
    "source_books": {
      "诡秘之主": 3,
      "斗破苍穹": 2,
      "凡人修仙传": 1,
      "求魔": 1,
      "蛊真人": 1
    },
    "passes": true
  },
  {
    "candidate": "project_candidate_03.yaml",
    "total_mechanisms": 8,
    "main": 3,
    "auxiliary": 3,
    "constraint": 2,
    "source_books": {
      "求魔": 2,
      "人道至尊": 2,
      "遮天": 1,
      "凡人修仙传": 1,
      "斗破苍穹": 1,
      "蛊真人": 1
    },
    "passes": true
  }
]
```

自检结论：3 个候选均满足机制数量 5-9、main 2-3、auxiliary 2-4、constraint 1-2、至少来自 3 本不同 Core7 作品、同一本来源书不超过 3 个机制的要求。每个候选均在 `mechanism_combination_logic` 中记录五层原创转化：外观替换、因果替换、代价替换、社会结构替换、情绪反馈替换。

## 下一步建议

Codex validation + Antigravity originality review。
