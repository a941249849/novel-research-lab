# Phase 1 智能体分工与职责划分契约 (Work Allocation)

*   **当前阶段**：`Phase 1`
*   **版本**：`v1.0.0-roles`

为了保障工程的高效推进，防止多代理系统发生指令冲突、读写覆盖及权限越界，特制定本职责划分契约。

---

## 1. 核心角色与职责分工 (Roles & Responsibilities)

本系统由三个核心智能体协作运行：

### ① Antigravity (编排者与审计智能体)
*   **定位**：总控与工程质量守护者。
*   **主要职责**：
    1.  负责驱动整个 pipeline 的执行，监控执行进度。
    2.  负责对 Codex 和 Hermes 产出的数据进行最终的合规审计与原创性、语义审计。
    3.  负责与人类用户进行最终交付物的交互和决策确认。

### ② Codex (代码编写与骨架提取智能体)
*   **定位**：数据流水线与清洗专家。
*   **主要职责**：
    1.  负责编写所有数据处理脚本（如扫描器、骨架采样提取器、清洗合并脚本）。
    2.  负责运行这些脚本，对原始文本语料执行提取，产出 `_skeleton.txt` 物理文件。

### ③ Hermes (信息抽取与状态核验智能体)
*   **定位**：NLP 结构化抽取与逻辑一致性校验专家。
*   **主要职责**：
    1.  负责调用大语言模型，读取各小说的骨架文本，抽取出其中的世界观规则、大纲走向与双轨属性值。
    2.  负责将抽取出的信息序列化为 JSON，并填入对应的 Schema 结构。
    3.  负责运行 SchemaValidator 校验逻辑，验证数据格式与逻辑完整性。

---

## 2. 任务独立性与禁止交叉红线 (Boundary Redlines)

为了防止逻辑混乱，各智能体的工作边界严禁交叉：
*   **“代码归 Codex，分析归 Hermes”**：Hermes 严禁编写任何对文件进行读写修改的脚本或工程命令，仅可通过 LLM 分析现成文件并输出 JSON 内容；Codex 严禁对抽取的机制进行主观叙事归纳。
*   **“审计归 Antigravity”**：Hermes 与 Codex 无权宣称任何产出物“已通过合规审查”，所有审查状态标记必须由 Antigravity 运行 `OriginalityAuditor` 后统一判定与签发。

---

## 3. 文件读写权限矩阵 (File Access Matrix)

| 文件路径/目录 | 拥有者 (Owner) | 写入/修改权限 | 只读权限 (Read-Only) |
| :--- | :--- | :--- | :--- |
| `novel_training_set/` | 系统底层 | **严禁任何人修改** | 所有智能体 (Antigravity/Codex/Hermes) |
| `phase0B/` | Antigravity | **禁止任何修改**（已冰封） | 所有智能体 (Antigravity/Codex/Hermes) |
| `scripts/` | Codex | Codex | Antigravity, Hermes |
| `phase1/01_skeletons/` | Codex | Codex | Hermes, Antigravity |
| `phase1/02_.../` (DNA & Ledger JSONs) | Hermes | Hermes | Antigravity, Codex |
| `phase1/03_features/` | Hermes | Hermes | Antigravity |
| `phase1/04_mechanism_library/` | Hermes | Hermes | Antigravity |
| `phase1/07_review/` | Antigravity | Antigravity | Hermes, Codex |
