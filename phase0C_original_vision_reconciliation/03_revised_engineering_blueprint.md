# 03：Novel Research Lab 系统重构工程蓝图 (Revised Engineering Blueprint)

*   **当前阶段**：`Phase 0C`
*   **架构定义**：工业级多智能体小说创作与研究框架蓝图

为了实现小说研究与创作的工程级落地，本蓝图确立了系统的 9 层重构架构设计，支持从底层语料分析到上层正文创作的多智能体编排。

---

## 1. 系统架构分层蓝图 (Mermaid Map)

```mermaid
graph TD
    subgraph ResearchLayer ["1. 研究层 (Research Layer)"]
        A1["原始语料库 (novel_training_set)"] --> A2["扫描器 (NovelMetadataScanner)"]
        A2 --> A3["清单列表 (novel_manifest.csv)"]
        A1 --> A4["采样器 (SkeletonExtractor)"]
        A4 --> A5["切片骨架 (skeletons)"]
    end

    subgraph KBLayer ["2. 知识库层 (Knowledge Base Layer)"]
        B1["故事圣经 (Story Bible)"]
        B2["人物志 (Character Bible)"]
        B3["世界观设定 (World Bible)"]
        B4["阵营拓扑 (Faction Topology)"]
    end
    A5 --> KBLayer

    subgraph LibLayer ["3. 机制库层 (Mechanism Library Layer)"]
        C1["跨书特征矩阵"] --> C2["机制分类索引 (category_manifest.json)"]
        C2 --> C3["抽象玄幻机制包 (30+ Mechanisms)"]
    end
    KBLayer --> LibLayer

    subgraph PlanLayer ["4. 规划层 (Planning Layer)"]
        D1["叙事大纲生成 (Outline Generator)"]
        D2["大纲细化器 (Plot Scheduler)"]
        D3["情绪/张力曲线控制器"]
    end
    LibLayer --> PlanLayer

    subgraph StateLayer ["5. 状态跟踪层 (State Tracking Layer)"]
        E1["双轨身份掩码器 (Mask/True)"]
        E2["装备资产寄存 (Inventory)"]
        E3["声望变化记账 (Ledger Ledger)"]
        E4["账本一致性校验 (Validator)"]
    end
    PlanLayer --> StateLayer
    StateLayer --> E4

    subgraph WriteLayer ["6. 创作层 (Writing Layer)"]
        F1["正文生成器 (ChapterDraftGenerator)"]
        F2["风格控制器 (Style Manager)"]
        F3["修改润色环路 (Revision Loop)"]
    end
    StateLayer --> F1
    F1 --> F3

    subgraph AuditLayer ["7. 审计层 (Audit Layer)"]
        G1["敏感词/查重红线过滤 (LCS)"]
        G2["原创映射一致性审计"]
        G3["审计报告出具 (OriginalityAuditor)"]
    end
    F3 --> G1
    G1 --> G3

    subgraph OrchLayer ["8. 编排工具层 (Tool Orchestration Layer)"]
        H1["本地控制台 CLI"]
        H2["异步流水线调度器 (Pipeline)"]
        H3["人工审查网关 (Human-in-the-Loop)"]
    end
    H1 --> H2
    H2 --> H3

    subgraph FileLayer ["9. 物理存储层 (File/Directory Layer)"]
        I1["JSON Schema 协议"]
        I2["本地增量文件数据库"]
    end
```

---

## 2. 架构层级深度定义

### 1. 研究层 (Research Layer)
*   **职能**：实现生文本的结构化转化。包含元数据扫描模块与骨架切片工具，负责将数十万字的小说切片输出为便于大模型消费的骨架。

### 2. 知识库层 (Knowledge Base Layer)
*   **职能**：持久化设定存储。通过 Book DNA 驱动，分类保存故事圣经（Story）、人物属性关系（Character）、地理物理法则（World）与势力声望地图（Faction）。

### 3. 机制库层 (Mechanism Library Layer)
*   **职能**：叙事资产中心。承载跨书特征矩阵与脱敏后的通用抽象机制定义（30个以上），向大纲生成提供规则包。

### 4. 规划层 (Planning Layer)
*   **职能**：大纲与细纲生成。根据输入的抽象机制配方，规划小说总情绪起伏（Tension）与每个情节节点（Narrative DNA）的避战/逃跑属性。

### 5. 状态跟踪层 (State Tracking Layer)
*   **职能**：内存一致性控制。由 State Ledger 驱动，维护 True Profile、Public Mask、Inventory 三个属性表，确保法宝消耗与战力境界变化完全匹配。

### 6. 创作层 (Writing Layer)
*   **职能**：正文生成。由 `ChapterDraftGenerator` 和风格修饰模块驱动，结合上层规划和状态，产出 3000-5000 字正文，通过 Draft-Critic 环路多轮修改。

### 7. 审计层 (Audit Layer)
*   **职能**：合规性判定。由 `OriginalityAuditor` 驱动，比对敏感词库、禁止相似列表，进行 LCS 相似度预警计算，生成标准的审计报告。

### 8. 编排工具层 (Tool Orchestration Layer)
*   **职能**：进程驱动与通信总线。提供命令行 CLI 接口，调度 reader $\rightarrow$ writer 进程，并在重要状态转换点挂起，等待人工签字审批。

### 9. 物理存储层 (File/Directory Layer)
*   **职能**：底层物理读写。定义 `phase0B/03_json_schema_v1/` 等标准接口目录，并使用 Git 对生成的 JSON 数据资产做版本追踪。
