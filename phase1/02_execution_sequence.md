# Phase 1 阶段工程执行序列与工序规程 (Execution Sequence)

*   **当前阶段**：`Phase 1`
*   **版本**：`v1.0.0-sequence`

本文件明确了 Phase 1 阶段从“生语料”到“标准化机制库”的 6 个执行工序。每个步骤必须在达成验收条件后，方可启动下一步。

---

## 2. 6 大执行工序详解

### Step 1：锁定训练集与 Manifest 生成
*   **负责人**：Codex
*   **输入**：`novel_training_set/` 文件夹下 7 本代表作小说原文。
*   **输出**：`scripts/scan_novels.py`、`novel_manifest.csv`。
*   **动作**：运行扫描脚本，检测这 7 本书的编码（GB18030/UTF-8）、字符数、预估章节数及 SHA-256 哈希值，写入 csv。
*   **验收条件**：`novel_manifest.csv` 中完整包含 7 本代表作记录，SHA-256 均不为空，且文件行数正确。

### Step 2：全量 Skeleton 提取
*   **负责人**：Codex
*   **输入**：7 本代表作小说原文、`novel_manifest.csv`。
*   **输出**：`phase1/01_skeletons/{book_name}_skeleton.txt`。
*   **动作**：使用 `SkeletonExtractor` 脚本，抓取每本书的完整章节目录、前 15,000 字、20%/40%/60%/80% 处的剧情切片窗口（各 2,000 字）、以及结尾 10,000 字。
*   **验收条件**：7 个骨架文本文件全部生成，每个文件行数合理（采样字数符合 MVA 规范，约 3-4 万字），无乱码。

### Step 3：单书 DNA 与 Ledger 映射生成
*   **负责人**：Hermes
*   **输入**：`phase1/01_skeletons/` 下的 7 个骨架文件、`phase0B/03_json_schema_v1/`。
*   **输出**：
    *   `phase1/02_book_dna/{book_name}_dna.json`
    *   `phase1/02_narrative_dna/{book_name}_narrative.json`
    *   `phase1/02_state_ledgers/{book_name}_ledger.json`
*   **动作**：运行信息抽取 Prompt，基于大语言模型分析各书骨架，生成单书对应的设定、大纲、账本状态，并调用 `SchemaValidator` 进行校验。
*   **验收条件**：21 个 JSON 文件全部通过 Draft-07 协议校验，报错列表为空。

### Step 4：跨书特征矩阵提取
*   **负责人**：Hermes
*   **输入**：21 个单书 JSON 映射文件。
*   **输出**：`phase1/03_features/cross_book_feature_matrix.json`。
*   **动作**：对比分析 7 本代表作的核心爽点特征（如：修仙流升级节奏、退婚剧情张力、双轨实力差幅度等），形成统一的多维比对矩阵。
*   **验收条件**：矩阵 JSON 结构完整，必须包含所有 7 本代表作，且对比维度不少于 6 项。

### Step 5：机制库归类与沉淀
*   **负责人**：Hermes
*   **输入**：跨书特征矩阵、单书 JSON 资产。
*   **输出**：`phase1/04_mechanism_library/category_manifest.json` 与各分类子机制定义文件。
*   **动作**：将提炼出的特征彻底脱离书籍载体，抽象为玄幻类通用叙事机制（如“信息差压迫-释放机制”等），写入机制库。
*   **验收条件**：归档机制数 $\ge 30$ 个，机制说明必须包含：机制名称、原著对应深层叙事功能、在 v1.0 下的 Schema 映射逻辑、建议的原创转化红线。

### Step 6：Phase 1 结项评审 (Review)
*   **负责人**：Antigravity
*   **输入**：Phase 1 产出的所有骨架、JSON、机制库文件。
*   **输出**：`phase1/05_review/phase1_review_report.md`。
*   **动作**：Antigravity 对所有机制进行合规审计，检查其是否紧密贴合“中文玄幻”主轴，检查相似度预警检测表现。
*   **验收条件**：Owner 审查报告，给出 PASS 结论，冻识 Phase 1 机制库。
