# v1.0 验证 Demo 验收标准 (Acceptance Criteria)

本文件明确了 Phase 0B 结束及 Phase 1 启动时的核心验收载体——验证 Demo (Acceptance Demo Runner) 的输入、输出与审核通过指标。

---

## 1. 验证 Demo 输入规范

验收程序运行时，必须提供一个 JSON 配置文件 `demo_run/input_mechanisms.json`，其中至少包含以下 **3-5 个抽象叙事机制**：

1.  **「双轨隐藏实力机制」**（对应《凡人》敛气术/《人道》易先生）：主角物理实力与展示实力存在人为信息差，具备动态反击伏笔。
2.  **「资源稀缺与功法绑定进化机制」**（对应《斗破》焚决吞噬）：境界晋升必须依赖具体的消耗性道具（Inventory 资产扣减），促成阶段性破境。
3.  **「大纲防暴毙之避战选择机制」**（对应《凡人》韩跑跑）：遇到超越极限的危机时，大纲自动触发规避路径而非降智强打。
4.  **「法宝使用之致命代偿机制」**（对应《诡秘》封印物负效应）：主角使用 Inventory 核心道具时，会扣减特定属性（如血量、神智）或在正文中伴随强烈的负效应描写。

---

## 2. 验证 Demo 产出标准

验收运行后，必须在 `demo_run/` 目录下生成以下 5 个符合 Schema 定义的交付文件：

### ① `demo_run/output_original_setting.json` (原创世界观与设定)
*   **格式要求**：必须完全通过 `book_dna.schema.json` 校验。
*   **内容要求**：定义原创的升级境界序列，描述全新的世界观背景，将机制合理归因于新背景，不存在原著的敏感词词根。

### ② `demo_run/output_original_outline.json` (原创小说大纲)
*   **格式要求**：必须完全通过 `narrative_dna.schema.json` 校验。
*   **内容要求**：必须包含完整的 `plot_checkpoints` 数组，每个节点须定义 `tension` 情绪值、`is_combat_skippable` 避战标识与 `evasion_path` 规避路径。

### ③ `demo_run/output_state_ledger.json` (运行后状态账本)
*   **格式要求**：必须完全通过 `state_ledger.schema.json` 校验。
*   **内容要求**：包含 `true_profile` 真实属性（含性格/动机权重、共生体列表）、`public_mask` 公开属性掩码、`inventory` 装备库存（含反噬代价描述）以及 `faction_reputation` 阵营声望表。

### ④ `demo_run/output_chapter_1.txt` (第一章原创小说正文)
*   **格式要求**：TXT 文本格式，字数必须达到 **3000-5000 字**。
*   **内容要求**：
    *   **情节逻辑**：正文必须完美展现主角利用“易容/敛气术”隐藏实力的细节（双轨掩码对比表现）。
    *   **大纲契合度**：剧情必须根据大纲的情绪抑扬状态（`tension`）推进。
    *   **避战与代价**：必须包含一段由于遭遇突发高阶强敌，主角果断“战术撤退”的避战生存抉择，或使用核心道具产生的反噬代价/资源损耗描写。

### ⑤ `demo_run/output_audit_report.json` (审计报告)
*   **格式要求**：必须完全通过 `audit_report.schema.json` 校验。
*   **内容要求**：
    *   `originality_score` 必须 $\ge 0.85$。
    *   `violation_flags` 数组必须为空。
    *   `compliance_status` 必须为 `"passed"`。
    *   `disclaimer_applied` 必须为 `true`。
    *   `consistency_status` 明确记录修为校验、道具反噬及声望状态校验的布尔值为 `true`。

