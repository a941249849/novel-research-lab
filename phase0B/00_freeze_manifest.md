# Phase 0B v1.0 架构冻结清单 (Freeze Manifest)

*   **架构版本**：`v1.0.0-freeze`
*   **冻结时间**：2026-07-08
*   **当前状态**：**已批准冻结 (OWNER_APPROVED_FROZEN)**

---

## 1. 冻结资产索引 (Asset Sitemap)

以下资产已全部写入工作区的 `phase0B/` 目录中，正式锁定架构标准：

| 资产文件路径 | 类型 | 描述 |
| :--- | :--- | :--- |
| **[00_freeze_manifest.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/00_freeze_manifest.md)** | Markdown | 本冻结清单文件，作为资产交付索引。 |
| **[01_architecture_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/01_architecture_v1.md)** | Markdown | v1.0 最小可行架构设计，锁定核心子系统与数据流模型。 |
| **[02_project_tree_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/02_project_tree_v1.md)** | Markdown | v1.0 目录树结构，定义源代码、脚本与数据的规范存放路径。 |
| **[03_json_schema_v1/](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/)** | 目录 | 包含 5 个核心数据结构的 JSON Schema 标准协议文件。 |
| ├─ [book_dna.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/book_dna.schema.json) | JSON | 锁定世界观与等级规则的数据格式。 |
| ├─ [narrative_dna.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/narrative_dna.schema.json) | JSON | 锁定大纲脉络与情绪节奏的数据格式。 |
| ├─ [state_ledger.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/state_ledger.schema.json) | JSON | 锁定双轨身份、装备与阵营声望的数据格式。 |
| ├─ [originality_transformer.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/originality_transformer.schema.json) | JSON | 锁定机制原创映射规则的数据格式（`function_transform_rules`）。 |
| └─ [audit_report.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/audit_report.schema.json) | JSON | 锁定原创性审计报告的数据格式。 |
| **[04_agent_role_contract.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/04_agent_role_contract.md)** | Markdown | 代理角色契约，定义 Reader, Transformer, Writer, Auditor 的权责与边界。 |
| **[05_skill_catalog_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/05_skill_catalog_v1.md)** | Markdown | v1.0 AGY SDK Skills 技能目录，定义核心功能执行工具。 |
| **[06_execution_pipeline_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/06_execution_pipeline_v1.md)** | Markdown | v1.0 执行管道，锁定多代理串联与数据流向阶段。 |
| **[07_originality_policy_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/07_originality_policy_v1.md)** | Markdown | 原创性转化合规准则，确立合格性边界，并包含必要的免责声明。 |
| **[08_demo_acceptance_criteria.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/08_demo_acceptance_criteria.md)** | Markdown | 验证性 Demo 的准入和验收标准，支持多机制输入与正文/审计报告输出。 |
| **[09_deferred_features_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/09_deferred_features_v1.md)** | Markdown | 延期功能目录，防止 v1.0 开发中发生需求蔓延。 |
| **[10_owner_review_checklist.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/10_owner_review_checklist.md)** | Markdown | 项目 Owner 最终审查校验单。 |
| **[11_owner_approval_record.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/11_owner_approval_record.md)** | Markdown | 项目 Owner 架构最终批准书。 |
 |
