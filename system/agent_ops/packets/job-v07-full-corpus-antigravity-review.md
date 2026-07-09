# NRL Antigravity Full Corpus Review Packet v0.7

## Job

- job_id: job-v07-full-corpus-antigravity-review
- contract_version: 0.7
- architecture_version: 0.4
- review_scope: full_remaining_corpus
- owner_agent: antigravity
- expected_output_path: system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md

## Purpose

Run a full-corpus literary and structural review for Novel Research Lab after the v0.4 architecture freeze.
The output must be structured for Codex ingestion, not written as a freeform essay.

## Architecture Baseline

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

## Required Asset Families

- `characters`
- `npcs`
- `factions`
- `artifacts`
- `techniques`
- `naming`
- `emotional_bonds`
- `foreshadowing`
- `state_ledger`

## Required Markdown Headings

- `## Job ID`
- `## Scope`
- `## Corpus Coverage`
- `## Cross-Book Mechanisms`
- `## Creation Asset Evidence`
- `## Originality Risk`
- `## Recommended Next Ingestion`
- `## JSON Manifest`

## JSON Manifest Contract

Return a fenced JSON block under `## JSON Manifest` with:

- job_id
- contract_version
- review_scope
- architecture_version
- corpus_policy
- book_reviews
- cross_book_mechanisms
- asset_family_evidence
- originality_risks
- recommended_next_ingestion

## Forbidden Actions

- Do not write novel prose.
- Do not produce Chapter 1.
- Do not generate final character sheets, final naming dictionaries, final technique trees, or final outline trees.
- Do not claim Hermes execution.
- Do not quote raw source prose.
- Do not include `novel_training_set/` paths in the returned artifact.

## Return Instruction

Save the completed review to:

```text
system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md
```
