# Schema 字段与模型筛选判定表 (Triage Matrix)

本表对 [schema_gap_report.md](../04_schema_gap/schema_gap_report.md) 中提出的所有新增字段与子系统进行评估分类。三类判定标准：
- **Accept for v1.0**：核心闭环必须，直接入库。
- **Simplify for v1.0**：机制需要，但裁剪为最简单的静态字段或文本描述。
- **Defer to v1.5 / v2.0**：过度设计或成本过高，延期处理。

---

| 序号 | 提案字段/系统 (Proposed Feature) | 归属模块 | v1.0 判定结论 | v1.0 简化实现方案与决策理由 |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **资质负值与阻力系数**<br/>(Aptitude Negativity) | Book DNA | **Simplify for v1.0** | 仅在角色属性中保留一个静态浮点数 `aptitude_multiplier`（如 0.2），在计算升级消耗时做简单乘算，避免复杂的资质演化树。 |
| 2 | **跨图战力折算系数**<br/>(Map Scale Coefficient) | Book DNA | **Defer to v1.5** | v1.0 采用直接换图机制，战力数据通过新地图重新初始化，无需在底层设计动态换算公式。 |
| 3 | **零和总量特性守恒**<br/>(Closed-Loop Conservation) | Book DNA | **Simplify for v1.0** | 简化为在超凡途径配置中添加静态标志位 `is_capped` 与最大槽位数限制，由大纲生成模块读取进行单向排重校验，不运行复杂的守恒状态机。 |
| 4 | **编译型超凡逻辑表征**<br/>(Compiler Power Schema) | Book DNA | **Defer to v2.0** | v1.0 将技能统一建模为静态配置字（技能名、效果描述、前置消耗），杜绝面向对象/编译化的技能代码模拟。 |
| 5 | **非线性历史纪元账本**<br/>(Epoch Causal Ledger) | Book DNA | **Defer to v1.5** | 历史因果统一写入地图和世界的 `lore_description`（纯文本形式），作为大纲生成的上下文背景，不建立时间轴数据追踪。 |
| 6 | **情绪负债与偿还账本**<br/>(Emotional Debt Ledger) | Narrative DNA | **Simplify for v1.0** | 仅在剧情大纲节点中保留一个静态整型字段 `tension`（范围 -10 到 +10），代表此节点的“打压值”或“爽快度”，用简单的滑窗加和评估抑扬节奏。 |
| 7 | **避战与规避节点**<br/>(Evasion Nodes) | Narrative DNA | **Accept for v1.0** | **必须保留**。在大纲节点中增加 `is_combat_skippable` (可避战) 与 `evasion_path` (规避路径)，是防止“韩跑跑”流派变弱智强拆必不可少的结构特征。 |
| 8 | **叙事胶囊与地图强解耦**<br/>(Decoupled Map Transition) | Narrative DNA | **Simplify for v1.0** | 换地图时，直接将旧地图的所有 NPC 与势力状态标记为 `status: archived` (归档)，使其在主运行队列中挂起，不使用复杂的“胶囊类”打包封装。 |
| 9 | **重生时间线 DAG 分叉引擎**<br/>(Timeline-Forking Engine) | Narrative DNA | **Defer to v2.0** | 严禁建立分叉时间线。v1.0 主角重生仅作为角色背景属性（`is_reincarnated = true`），记忆和剧情推进直接由大纲写死。 |
| 10 | **第三方震惊反应指数**<br/>(Bystander Reaction Index) | Narrative DNA | **Defer to v1.5** | 旁观者的震惊描写直接写进正文生成的 Prompt 指令模板中（如“侧面烘托高潮”），不在数据表层进行数值量化跟踪。 |
| 11 | **跨时空因果回响线**<br/>(Karmic/Echo Line) | Narrative DNA | **Defer to v2.0** | 因果羁绊与“相似的花”归入角色的静态关系描述段落中，不建立专门的跨时空因果溯源计算逻辑。 |
| 12 | **双轨信息掩码账本**<br/>(Dual-Track Information) | State Ledger | **Accept for v1.0** | **必须保留**。这是扮猪吃虎流网文的精髓。State Ledger 必须拆分为 `true_profile`（真属性）与 `public_mask`（公开易容/掩码属性），两者差值直接作为触发爽点的系统触发器。 |
| 13 | **共生意识体分类账**<br/>(Symbiotic Actor Ledger) | State Ledger | **Simplify for v1.0** | 主角实体下挂载一个特殊的 `symbiotic_entities` 静态数组（包含名字和提供知识分类），共生体不作为拥有独立时空坐标的 Agent 运作。 |
| 14 | **多马甲因果防火墙**<br/>(Multi-Persona Firewall) | State Ledger | **Defer to v1.5** | 马甲的切换直接作为剧情事件驱动，不在底层数据结构层做因果阻断和多账号数据隔离。 |
| 15 | **效用决策人格矩阵**<br/>(Agent Decision Matrix) | State Ledger | **Simplify for v1.0** | 仅保留两个基本态度参数：`moral_threshold`（道德下限阈值，0-100）和 `utility_priority`（利益优先度权重，0.0-1.0），由 LLM 在做剧情选择时读取，不进行真正的纳什均衡公式推演。 |
| 16 | **动态法理/规则覆写图层**<br/>(Dynamic Domain Overlay) | State Ledger | **Defer to v2.0** | 局部规则压制（如禁区压制）简化为地图节点的静态描述，不进行运行时公式重载。 |
| 17 | **主客观认知真实度偏差**<br/>(Reality Horizon Tracker) | State Ledger | **Defer to v2.0** | 幻境、梦境和夺舍嵌套直接当作剧情任务处理，不在系统底层开辟认知维度分账。 |
| 18 | **封印物负效应代价判定**<br/>(Negative Trigger Stack) | State Ledger | **Simplify for v1.0** | 道具属性中增加 `backlash_description`（反噬代价描述）和 `trigger_condition`（触发文本），大纲生成时直接传递给模型作为负面限制。 |
| 19 | **极道武器实体化代理**<br/>(Sentient Weapon NPC) | State Ledger | **Defer to v1.5** | 法宝神兵依然分类在静态道具（Inventory），其觉醒与特殊感情直接写在道具描述字段内。 |
