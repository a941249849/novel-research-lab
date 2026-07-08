# Agent 角色契约规范书 (Role Contract)

本规范书锁定了 Novel Research Lab v1.0 团队中 4 类 AI 代理的角色定义、输入/输出格式、核心职责与行为边界，作为多代理开发时的接口调用标准。

---

## 1. Reader Agent (文本解析与特征提取)
*   **职责描述**：专门负责扫描小说数据源，自动解析其世界观、等级设定、大纲里程碑及标志性特征设定。
*   **输入契约**：
    *   `filepath`：只读的原始小说 text 文件绝对路径。
    *   `skeleton_range`：提取的骨架范围。
*   **输出契约**：
    *   原始 `Book DNA` JSON。
    *   原始 `Narrative DNA` JSON。
*   **行为边界**：
    *   **禁止**读取 `novel_training_set/` 文件夹之外的任何文件。
    *   **禁止**修改或重写小说正文。

---

## 2. Transformer Agent (机制原创脱敏)
*   **职责描述**：对 Reader 提取出的原始设定与大纲，按照 `Originality Transformer` 中定义的 `function_transform_rules` 规则进行脱敏转换，输出全新的原创设定大纲。**其核心定位是降低换皮与过度相似风险，提高原创性，但不作法律保证。**
*   **输入契约**：
    *   原始 `Book DNA` & `Narrative DNA` JSON。
    *   `originality_transformer.schema.json` 规则配置。
*   **输出契约**：
    *   原创 `Book DNA` JSON。
    *   原创 `Narrative DNA` JSON（大纲已被脱敏机制重写）。
*   **行为边界**：
    *   **必须**校验转换后的大纲不包含原著的任何敏感词。
    *   **禁止**为了追求复杂度而自动引入未注册在 JSON Schema 中的非 v1.0 字段。

---

## 3. Writer Agent (原创正文写作)
*   **职责描述**：根据 Transformer 输出的原创大纲、原创世界观背景，以及初始化后的 `State Ledger` 状态，生成具体的原创小说第一章正文。
*   **输入契约**：
    *   原创 `Book DNA` & `Narrative DNA` JSON。
    *   初始化的 `State Ledger` JSON。
*   **输出契约**：
    *   原创第一章小说正文（TXT格式，3000-5000字）。
    *   运行后的 `State Ledger` 状态（更新主角经验值、装备损耗及身份公开状态）。
*   **行为边界**：
    *   **必须**严格遵循 `Narrative DNA` 节点的 `tension`（抑扬节奏）及 `is_combat_skippable`（避战分支）限制。
    *   **必须**在正文写作中体现 `State Ledger` 双轨身份带来的信息差，如通过角色扮演维持 `public_mask`。

---

## 4. Auditor Agent (合规性与逻辑审计)
*   **职责描述**：对 Writer 生成的原创正文和大纲进行合规性、一致性及原创程度的联合审计。
*   **输入契约**：
    *   Writer 生成的原创第一章正文。
    *   原创 `Book DNA`、`Narrative DNA`、转换前后的对照表及 `Originality Transformer` 协议规则。
*   **输出契约**：
    *   符合 `audit_report.schema.json` 规范的审计报告 JSON。
*   **行为边界**：
    *   **必须**在审计报告中附加法律免责声明，明确指出“降低换皮与过度相似风险，提高原创性，但不作法律保证。”
    *   一旦检测到敏感原著词汇或严重的战力逻辑崩坏（如主角越过限制秒杀不可秒杀BOSS），必须将 `compliance_status` 判定为 `failed`。
