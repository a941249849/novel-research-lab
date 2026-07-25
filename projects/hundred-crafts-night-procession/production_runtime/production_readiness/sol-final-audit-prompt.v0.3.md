# 《百工夜行录》正式生产前最终终审 v0.3

你是 Novel Research Lab 的 Sol 最终独立审查者。只读审查，不生成正文，不修改文件。

先读取：

- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.1.md`
- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.2.md`
- `production_runtime/production_readiness/audit-contract.v0.1.json`

以上路径均位于 `projects/hundred-crafts-night-procession/`。然后完整核对当前磁盘上的：

- `creation_assets/canonical_baseline.json`
- `creation_assets/project_assets.json`
- `validation/project_reconciliation.json`
- `validation/project_reconciliation_application.json`
- `production_runtime/plans/volume1_outline.v1.json`
- `production_runtime/plans/volume1_production_manifest.v1.json`
- `production_runtime/state/canonical_initial_state.v1.json`
- `production_runtime/chapter_titles.volume1.json`
- `production_runtime/intents/`
- `production_runtime/story_windows/`
- `production_runtime/quality/`
- `system/runtime/nrl_project_production.py`
- `system/runtime/nrl_production_runtime.py`
- `system/runtime/nrl_story_window.py`
- `system/runtime/nrl_volume1_release.py`
- `system/production_runtime/schemas/continuity_audit.schema.json`
- `system/production_runtime/schemas/story_window.schema.json`
- `tests/test_hundred_crafts_production_readiness.py`

重点复核 v0.2 尚未关闭的 B-02、B-03、B-05、B-06、B-07、B-08：

1. baseline 必须完整锁定 audit contract、项目状态、设计、资产、细纲、manifest、初始状态、标题、66 intents、七窗口、质量合同和 reconciliation；validator 必须拒绝清单缺项和任一漂移。
2. Owner review SHA 必须与真实 Sol/Antigravity 文件、final-review-index 和当前 baseline 三方一致；任意占位 SHA 必须失败。
3. 第 33 章必须明确结算 `faction_maintenance_team lifecycle_state seed→active`，且只有该章允许；19/29/60 与 41/54 必须落在实际可结算资产状态，不只是机械章节标签。
4. settlement 必须拒绝未知资产、未知字段、stale before、intent 未声明 delta、重复兑现和不符合冻结 intent 的 lifecycle；不得使用全资产宽松状态表。
5. final audit 必须绑定 revision，并显式列出已关闭的初审 blocking/major issue ID；final 中任何 blocking/major 都必须阻断；candidate 不得自动声称解决；acceptance 必须复核语义终审与执行证据。
6. 首窗正式质量合同必须在没有正式正文时诚实保持 contract-ready，不伪造通过；一旦有正文，3000-4200 汉字、指标、Terra/Luna/Sol 执行证据、Sol 窗审与独立 Antigravity 窗审必须 fail closed。
7. 历史样章只可作为带真实字符数和 SHA 的 calibration evidence，不得成为正式质量 ACCEPT。
8. 第 1-10 章之外、连续批量和 publish 必须保持禁止；第 11 章必须同时等待 1-10 Sol 窗审和独立 Antigravity 窗审。

执行必要的只读 CLI 和测试。不要把“尚未有正文所以没有正式质量报告”本身当 blocker；应判断正式质量合同是否能在生产后 fail closed。当前终审报告本身尚未被 index 收录是正常的 bootstrap 状态，不得因此单独判 REVISE；应审查 index 和 Owner 绑定代码是否能在报告生成后可靠验证真实哈希。

输出 Markdown，固定结构：

- `# Verdict`，单独一行 `ACCEPT` 或 `REVISE`
- `# Blocker Closure`，B-01 至 B-08 逐项 CLOSED/OPEN
- `# New Findings`，blocking/major/minor
- `# Authorization Recommendation`
- `# Evidence Read`

任何仍存在的 blocking 或 major 必须导致 REVISE。只有全部关闭时，才可建议 Owner 将正式首窗口限定开放为第 1-10 章；第 11+、连续批量和 publish 仍不得开放。
