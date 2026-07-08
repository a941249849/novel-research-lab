# Novel Research Lab v1.0 Agent 技能目录 (Skill Catalog)

本目录定义了 v1.0 开发阶段中，为实现“读-转-写”闭环而必须封装在 Agent SDK 中的核心 Skills。所有技能必须通过输入-输出接口与系统 JSON Schema 严格挂钩。

---

## 1. `NovelMetadataScanner` (元数据扫描技能)
*   **用途**：扫描小说文件，自动生成 CSV 清单元数据。
*   **实现逻辑**：
    1.  遍历指定目录下的 `.txt` 文件。
    2.  读取前 10KB 字符，利用 `try-except` 捕获依次检测 `utf-8`、`gb18030` 和 `big5` 编码。
    3.  计算文件的 SHA-256。
    4.  提取作者和标题，并将信息整理为 Manifest 行记录写入。
*   **接口规范**：
    *   *输入*：小说原始文件。
    *   *输出*：符合 `novel_manifest.csv` 格式的字典。

## 2. `SkeletonExtractor` (骨架切片提取技能)
*   **用途**：以极小上下文开销获取大长篇小说的主干与文笔特征。
*   **实现逻辑**：
    1.  检测并读取整本小说文本。
    2.  利用章节正则匹配抓取完整的章节目录表。
    3.  抽取开头 15,000 字（获取开局 Hook 模式）。
    4.  以 20%、40%、60%、80% 为中点，向前向后各抽取 2,000 字，形成 4 个剧情中段采样窗口。
    5.  抽取结尾 10,000 字（获取高潮/收尾写法）。
*   **接口规范**：
    *   *输入*：小说原始文件、目标输出路径。
    *   *输出*：骨架文本文件。

## 3. `OriginalityTransformer` (机制原创转化技能)
*   **用途**：执行五步原创转化工作流，脱敏经典设定。
*   **实现逻辑**：
    1.  接收原始设定 JSON。
    2.  读取 `originality_transformer.schema.json` 中配置的机制转化映射表。
    3.  执行功能替代计算，重新赋予世界观因果，并匹配 `naming_constraints` 重构命名体系。
    4.  输出脱敏后的原创设定。
*   **接口规范**：
    *   *输入*：原始 DNA、转换配置 JSON。
    *   *输出*：原创 DNA JSON。

## 4. `DoubleTrackLedgerValidator` (双轨账本校验技能)
*   **用途**：在大纲生成和正文书写中，校验双轨身份（True 与 Public Mask）及法宝负效应的逻辑完整性。
*   **实现逻辑**：
    1.  核对 `State Ledger` 中 True View 与 Public Mask 是否符合差值策略。
    2.  监控大纲事件，一旦主角使用特定武器（Inventory 带有 `backlash_description`），在大纲或正文中必须包含气血扣减或副作用的表现描写。
*   **接口规范**：
    *   *输入*：生成的正文或大纲、当前的 `State Ledger`。
    *   *输出*：布尔值（是否通过校验）、冲突详细描述。

## 5. `OriginalityAuditor` (原创性与敏感词审计技能)
*   **用途**：执行最终审计，保障原创性，**降低换皮与过度相似风险，提高原创性，但不作法律保证**。
*   **实现逻辑**：
    1.  比对敏感原词库（如经典功法名、人物名、特定专有名词），进行字面及近义词正则匹配。
    2.  匹配 `forbidden_similarity_patterns`，检查原创大纲的组合是否过于靠近原著。
    3.  输出审计报告 JSON。
*   **接口规范**：
    *   *输入*：原创正文、转换对照关系。
    *   *输出*：符合 `audit_report.schema.json` 规范的 JSON 数据。

## 6. `SchemaValidator` (协议结构校验技能)
*   **用途**：校验各阶段生成的 JSON 文件（Book DNA、Narrative DNA、State Ledger、Originality Transformer、Audit Report）是否完全符合对应的 JSON Schema 协议定义。
*   **实现逻辑**：
    1.  读入目标 JSON 文件。
    2.  载入对应的 `.schema.json` 文件。
    3.  使用标准的 JSON Schema 校验器（如 Python 的 `jsonschema` 库）进行格式与约束校验。
*   **接口规范**：
    *   *输入*：待校验 JSON 内容、Schema 协议文件路径。
    *   *输出*：布尔值（是否合规）、错误字段及具体原因列表。

## 7. `ChapterDraftGenerator` (第一章正文生成技能)
*   **用途**：根据脱敏转化后的原创世界设定（Book DNA）、大纲与情绪参数（Narrative DNA）及初始状态（State Ledger），生成 3000-5000 字的第一章原创小说正文。
*   **实现逻辑**：
    1.  读取原创 Book DNA、Narrative DNA 和 State Ledger 数据。
    2.  组织正文写作 Prompt，锁定字数区间（3000-5000字）。
    3.  引导模型在情节中合理织入双轨实力隐藏、避战逃跑或法宝使用代价等机制动作。
    4.  生成正文并输出。
*   **接口规范**：
    *   *输入*：原创 Book DNA JSON、原创 Narrative DNA JSON、当前 State Ledger JSON。
    *   *输出*：小说正文 TXT、更新后的 State Ledger JSON。
