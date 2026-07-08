# 01：原始愿景与当前 v1.0 架构对照映射表 (Current v1.0 Mapping)

*   **当前阶段**：`Phase 0C`
*   **对比版本**：`Original Vision vs Phase 0B/Phase 1`

---

## 1. 愿景对照矩阵 (Reconciliation Matrix)

以下将原始构想中的集大成能力，与当前已冻结的 v1.0 MVA 规范及 Phase 1 交接规划进行逐项对账：

| 原始系统能力 | 当前是否覆盖 | 当前覆盖文件 | 覆盖程度 | 是否进入 v1 工程实现 | 规划归属 / 备注 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Story Bible (故事圣经)** | 部分覆盖 | [book_dna.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/book_dna.schema.json) | 部分覆盖 | **是** | v1 简化为 Book DNA 世界观大设定，暂不支持树状百科。 |
| **Character Bible (人物志)** | 部分覆盖 | [state_ledger.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/state_ledger.schema.json) | 部分覆盖 | **是** | v1 简化为 State Ledger 中的 True Profile 实体，不支持马甲链。 |
| **World Bible (世界设定)** | 部分覆盖 | [book_dna.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/book_dna.schema.json) | 部分覆盖 | **是** | 包含在 Book DNA 的 `world_lore` 中，锁定升级境界序列。 |
| **Faction System (阵营)** | 部分覆盖 | [state_ledger.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/state_ledger.schema.json) | 部分覆盖 | **是** | v1 仅通过 `faction_reputation` 数字哈希表示，无阵营动态冲突。 |
| **Power System (战力系统)** | 部分覆盖 | [book_dna.schema.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/03_json_schema_v1/book_dna.schema.json) | 部分覆盖 | **是** | v1 仅包含境界数组与数值战力属性，无级联崩溃防御模型。 |
| **Long-term Memory (记忆)** | 未覆盖 | [09_deferred_features_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/09_deferred_features_v1.md) | 未覆盖 | **否** | **延期到 v2**。v1 使用 Context 强灌 4 万字骨架，不建向量库。 |
| **Foreshadowing Ledger (伏笔)**| 未覆盖 | [09_deferred_features_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/09_deferred_features_v1.md) | 未覆盖 | **否** | **延期到 v1.5**。v1 只验证大纲避战与法宝代价，不追踪长线伏笔。 |
| **Chapter Gen Loop (生成环)** | 部分覆盖 | [05_skill_catalog_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/05_skill_catalog_v1.md) | 部分覆盖 | **是** | v1 仅支持生成第一章正文，无大长篇多章节状态轮转。 |
| **Revision Loop (修改环路)** | 未覆盖 | [09_deferred_features_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/09_deferred_features_v1.md) | 未覆盖 | **否** | **延期到 v1.5**。v1 依靠 Prompt 一次性出正文，不支持多轮抛光。 |
| **Continuity Checker (连贯性)**| 部分覆盖 | [05_skill_catalog_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/05_skill_catalog_v1.md) | 部分覆盖 | **是** | v1 通过 `DoubleTrackLedgerValidator` 静态校验状态差值是否吻合。 |
| **Style Control (风格控制)** | 部分覆盖 | [07_originality_policy_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/07_originality_policy_v1.md) | 部分覆盖 | **是** | v1 仅通过命名限制与禁止词根过滤，无自适应微调文风模型。 |
| **Agent Orchestration (编排)**| 部分覆盖 | [06_execution_pipeline_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/06_execution_pipeline_v1.md) | 部分覆盖 | **是** | v1 为单线程线性管道流程，无复杂异步编排总线（MQ）。 |
| **Human Review Gate (人工审)** | 部分覆盖 | [08_demo_acceptance_criteria.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/08_demo_acceptance_criteria.md) | 部分覆盖 | **是** | 包含在阶段结项 Review 流程中，采用中断等待批准方式。 |
| **Codex Pipeline (代码流水)** | 部分覆盖 | [06_execution_pipeline_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/06_execution_pipeline_v1.md) | 部分覆盖 | **是** | v1 包含骨架抽取和扫描脚本的规划，正待工程化落地。 |
| **Hermes Creative (创作层)** | 部分覆盖 | [05_skill_catalog_v1.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase0B/05_skill_catalog_v1.md) | 部分覆盖 | **是** | v1 提供大纲与第一章正文的生成接口，仅处理小章节片段。 |
