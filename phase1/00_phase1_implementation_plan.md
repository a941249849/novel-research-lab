# Phase 1：全量语料分析与机制库建设实施方案 (Implementation Plan)

*   **当前阶段**：`Phase 1`
*   **版本**：`v1.0.0-plan`

---

## 1. Phase 1 核心目标 (Goals)

Phase 1 聚焦于将 Phase 0B 冻结的“扫描-提取-验证-审计”工具链在全量本地小说语料库上工程化落地，并构建出一个系统化、结构化的**中文玄幻叙事机制库**。
具体目标包括：
1.  **工程化扫描提取**：编写并执行工业级的数据提取脚本，对 7 本核心小说代表作进行全量骨架切片采样。
2.  **结构化数据分析**：为 7 本书生成符合 `book_dna`、`narrative_dna` 与 `state_ledger` 规范的标准 JSON 映射，填充真实的元数据与机制表现。
3.  **叙事机制库沉淀**：归类并归纳至少 30 个中文玄幻小说的经典叙事机制（如：退婚流、戒指老爷爷、敛气扮猪吃虎、血脉觉醒、天道反噬等），为后续 Phase 2 的原创转化与大纲生成提供弹药。

---

## 2. 输入与输出文件定义 (Inputs & Outputs)

### 输入文件 (Inputs)
*   **原始小说文本**：`novel_training_set/` 下的所有原始经典小说 txt 语料（只读，严禁修改）。
*   **元数据清单**：`scripts/scan_novels.py` 扫描生成的 `novel_manifest.csv`。
*   **架构规范协议**：`phase0B/` 下的所有已冻结架构与 Schema 文件。

### 输出文件 (Outputs)
*   **全量切片骨架**：`phase1/01_skeletons/{book_name}_skeleton.txt`
*   **单书机制映射**：
    *   `phase1/02_book_dna/{book_name}_dna.json`
    *   `phase1/02_narrative_dna/{book_name}_narrative.json`
    *   `phase1/02_state_ledgers/{book_name}_ledger.json`
*   **跨书特征矩阵**：`phase1/03_features/cross_book_feature_matrix.json`（总结共性特征）
*   **玄幻叙事机制库**：`phase1/04_mechanism_library/category_manifest.json`（按流派、功能对机制分类归档）

---

## 3. 阶段边界与非目标 (Boundaries & Exclusions)

### 阶段边界 (What We Do)
*   全量扫描元数据与提取章节切片骨架。
*   利用大语言模型提取代表作中的叙事机制并生成对应 Schema 数据。
*   对提炼出的机制进行玄幻领域的分类与解耦定义。

### 非目标 (What We Do NOT Do)
*   **不做模型训练**：严禁在 Phase 1 阶段训练任何神经网络大模型。
*   **不做原创大纲与正文生成**：本阶段只提炼原著，不进行新书的原创大纲设计与第一章以后的正文创作。
*   **不修改冻结协议**：严禁随意调整 Schema，即使数据抽取中遇到格式矛盾，也必须通过外层数据清洗解决，保持 Schema 冰封。

---

## 4. 完成标准 (Completion Criteria)

当以下条件同时满足时，Phase 1 宣告结束并可申请进入 Phase 1 Review：
1.  `novel_manifest.csv` 中所有 7 本代表作均成功生成对应的骨架切片，且无编码报错。
2.  为 7 本小说生成的 21 个 JSON 文件（Book DNA、Narrative DNA、State Ledger 各 7 个）全部通过 `jsonschema` 校验器校验，校验通过率为 **100%**。
3.  整理归档的中文玄幻机制库包含至少 **5 个大分类**，且包含不少于 **30 个** 经典玄幻具体机制定义。
