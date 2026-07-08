# Phase 1D: Execution Plan

本文件规定了全训练集 18 本书多维度剖析与经验蒸馏的**最小可行执行计划**。

---

## 1. 分批执行路线 (Batch Schedule)

深读剖析工作分为 **3 批** 逐步推进：

### 批次 1 (Batch 1)：核心代表作补齐与方法论对齐
*   **处理书目**：7 本 Core7 作品（《遮天》、《诡秘之主》、《斗破苍穹》、《蛊真人》、《人道至尊》、《凡人修仙传》、《求魔》）+ 1 本高契合度经典《仙逆》。
*   **处理重点**：
    *   **Core7 直接映射**：7 本 Core7 作品的 BookDNA、NarrativeDNA 及 Ledger 正式 JSON 已在 Phase 1C 冻结，**直接导入其机制定义，绝不进行二次提取**，仅补充其余的 16 维文学/市场规律深读报告。
    *   对《仙逆》进行完整深读提取，校验方法论一致性。
*   **产出**：8 份单书深读报告，补齐《仙逆》正式 DNA JSON 并通过 Schema 校验。

### 批次 2 (Batch 2)：第二梯队深读
*   **处理书目**：5 本书（《一念永恒》、《完美世界》、《将夜》、《武动乾坤》、《大主宰》）。
*   **处理重点**：补齐这 5 本书的 16 维深读报告，同时使用 Codex 自动化脚本提取/补齐其正式 BookDNA, NarrativeDNA 与 Ledger JSON 库。
*   **产出**：5 份单书深读报告，5 套正式 DNA/Ledger JSON（存入 `phase1/02_*` 正式运行库）。

### 批次 3 (Batch 3)：第三梯队深读
*   **处理书目**：5 本书（《永生》、《牧神记》、《雪中悍刀行》、《不死不灭》、《圣墟》）。
*   **处理重点**：同上，全面结清 18 本全训练集的底层抽取与剖析。
*   **产出**：5 份单书深读报告，5 套正式 DNA/Ledger JSON（存入 `phase1/02_*` 正式运行库）。

---

## 2. 补齐与复用机制 (Reuse & Stub Upgrade Mechanics)

*   **11 本 Stub 升级规范**：
    1.  Codex 调度读取 `phase1/01_skeletons/` 对应的 stub 骨架切片文本。
    2.  根据 [per_book_deep_reading_framework.md](file:///Users/liuneng/Documents/Novel%20Research%20Lab/phase1D/per_book_deep_reading_framework.md) 生成单书深读报告。
    3.  自动生成通过 Draft-07 验证的标准 DNA JSON 文件，并存入正式运行目录，将 stub 状态彻底转为正式 Promoted 状态。
*   **数据归宿**：
    *   单书深读报告归档至 `phase1D/01_book_reports/`。
    *   正式 JSON 数据进入 `phase1/02_book_dna/`, `phase1/02_narrative_dna/`, `phase1/02_state_ledgers/`。

---

## 3. 防范文档爆炸策略 (Anti-Document Explosion)

为防止生成大量冗余大文件，采取以下约束：
1.  **单书报告字数硬性上限**：每个 md 报告必须紧扣 16 个维度输出，总字数严禁超过 1000 字。
2.  **跨书规律高浓度抽象**：横向提炼仅产出唯一一份《跨书蒸馏经验白皮书》，合并记录 7 类模型，字数控制在 3000 字以内，不准拆成十几个零碎的小文件。

---

## 4. 阶段转入与 Hermes 后续调用 (Transition to Grand Synthesis)

1.  **立项基线锁定**：当 Batch 3 校验 PASS 且《跨书蒸馏经验白皮书》锁定后，Phase 1D 宣告正式闭环结项。
2.  **Grand Synthesis 开启**：将白皮书作为顶级提示上下文，正式激活 **Hermes Grand Synthesis Prompt**。由 Hermes 提供 10 个高概念方向、5 个母题组合，并最终由 Owner 选定唯一原创项目，进入原创大纲和原创 Ledgers 的具体细化。

---

## 5. Review Summary

*   **Review Metadata**：
    *   phase: Phase 1D
    *   task_name: Full Corpus Distillation Mission Planning Review
    *   status: PASS
    *   reviewer: Antigravity
    *   date: 2026-07-08
*   **Review Findings**：
    *   **架构一致性**：本执行计划重新聚焦于“从全训练集吸取长篇网文生命力与规律”的 NRL 核心目标，解决了前期原创生成狭窄化、拼凑感的问题。
    *   **计划可行性**：分 3 批推进的路线极为清晰。通过复用 Core7 数据和严格控制单书报告字数，有效防范了文档爆炸，维持了系统的轻量性。
    *   **红线控制**：本计划未调用 Hermes，没有生成任何原创正文或候选设定，未对 phase0B 的 JSON Schema 进行任何字段改动，边界绝对洁净。
*   **Verdict**：**PASS (通过，可提交 Owner 审阅)**。
