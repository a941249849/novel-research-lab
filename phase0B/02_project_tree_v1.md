# Novel Research Lab v1.0 目录树规范 (Project Tree)

本规范书锁定了 Novel Research Lab v1.0 的工作区目录布局，所有后续的代码编写、大纲生成、临时数据和最终产出均必须严格遵守此树状结构。

---

## 1. 目录结构树 (Directory Tree)

```text
Novel Research Lab/
├── novel_training_set/                 # [已锁定] 原始小说文本目录 (只读)
│   ├── 《遮天》（精校版全本）作者：辰东.txt
│   ├── 蛊真人.txt
│   └── ... 其它 16 本小说 txt
├── scripts/                            # 自动化脚本目录
│   ├── scan_novels.py                  # [已完成] 扫描与清单生成脚本
│   └── extract_skeletons.py            # [已完成] 骨架提取与窗口切片脚本
├── phase0A/                            # [已完成] Phase 0A 探索与校准成果目录 (只读)
│   ├── 00_manifest/
│   │   └── novel_manifest.csv          # 18本小说扫描清单
│   ├── 01_sample_selection/
│   │   └── sample_selection.md         # 样本选择报告
│   ├── 02_reading_reports/
│   │   └── {book_title}_reading_discovery_report.md
│   ├── 03_signature_feature_matrix/
│   │   └── signature_feature_matrix.json
│   ├── 04_schema_gap/
│   │   └── schema_gap_report.md
│   ├── 05_architecture_recommendation/
│   │   └── revised_architecture_recommendation.md
│   ├── 06_freeze_readiness/
│   │   └── phase0B_freeze_readiness.md
│   └── 07_review/
│       ├── phase0A_review_summary.md
│       ├── v1_core_requirements.md
│       ├── v1_deferred_features.md
│       ├── schema_accept_reject_table.md
│       └── phase0B_entry_decision.md
├── phase0B/                            # [当前阶段] v1.0 架构冻结包目录 (本规范所处目录)
│   ├── 00_freeze_manifest.md           # 冻结清单
│   ├── 01_architecture_v1.md           # v1.0 最小可行架构设计
│   ├── 02_project_tree_v1.md           # 目录树规范
│   ├── 03_json_schema_v1/              # JSON Schema 协议定义文件夹
│   │   ├── book_dna.schema.json
│   │   ├── narrative_dna.schema.json
│   │   ├── state_ledger.schema.json
│   │   ├── originality_transformer.schema.json
│   │   └── audit_report.schema.json
│   ├── 04_agent_role_contract.md       # 代理角色契约
│   ├── 05_skill_catalog_v1.md          # 技能目录
│   ├── 06_execution_pipeline_v1.md     # 执行管道
│   ├── 07_originality_policy_v1.md     # 原创性政策与免责声明
│   ├── 08_demo_acceptance_criteria.md  # 验收 Demo 标准
│   └── 09_deferred_features_v1.md      # 延期功能目录
└── demo_run/                           # [未来开发] Phase 0B.5/Phase 1 运行及产出目录
    ├── input_mechanisms.json           # 验收输入文件（3-5个抽象叙事机制）
    ├── output_original_setting.json    # 输出：原创设定 (Book DNA)
    ├── output_chapter_1.txt            # 输出：原创第一章正文
    └── output_audit_report.json        # 输出：原创性审计报告
```

---

## 2. 目录权限与写入规则

1.  `novel_training_set/` 目录为**只读**。禁止在此目录下创建任何非 `.txt` 临时文件，严禁修改、重命名或删除原著。
2.  `phase0A/` 目录属于已审计的历史资产，处于**归档锁定**状态，除必要的问题追溯外，后续阶段不应对其进行修改。
3.  `phase0B/` 属于当前锁定的协议包。开发阶段应以此文件夹下的 JSON Schema 为最终接口进行代理间的数据绑定，禁止私自增删字段。
4.  `demo_run/` 是 Demo 的运行时目录，用于存放测试输入和输出产物。
