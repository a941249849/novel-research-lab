# 《百工夜行录》正式生产前最终终审 v0.4

你是 Novel Research Lab 的 Sol 最终独立审查者。只读审查，不生成正文，不修改文件。

先读取项目目录下的：

- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.1.md`
- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.2.md`
- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.3.md`
- `production_runtime/production_readiness/audit-contract.v0.1.json`

然后复核当前磁盘上的 canonical baseline、项目资产、reconciliation、66 章 manifest/intents、七个 story windows、首窗质量合同，以及：

- `system/runtime/nrl_project_production.py`
- `system/runtime/nrl_production_runtime.py`
- `system/runtime/nrl_story_window.py`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_hundred_crafts_production_readiness.py`

重点验证 v0.3 尚未关闭的 B-06、B-08 及其 minor：

1. 正式项目的最终 revision 必须有 hash-bound Codex Terra writer execution；复用 draft 时也必须把真实 draft writer 身份重新绑定到 revision。
2. 正式项目不得使用 writer bundled observation；必须单独调用 Codex Luna，并把 observation、revision SHA、provider、model 持久化绑定。
3. 正式 final audit 必须由 Codex Sol 执行，Antigravity fallback 不得占据 Sol 正式证据位置；acceptance 必须复核 chapter、role、artifact path/hash、revision hash、provider 和 model。
4. 首窗 packet 必须逐章复核 Terra/Luna/Sol 三份执行证据，任一缺失、错配或 provider/model 错误都 fail closed。
5. Sol 主窗审只接受 Codex `gpt-5.6-sol`，不得由 Antigravity fallback 冒充；独立 Antigravity 窗审仍必须单独存在。
6. settlement 不仅拒绝额外/非法 delta，也必须拒绝遗漏冻结 intent 要求的 delta。
7. readiness 的 dual review 布尔值必须复算真实 Sol/Antigravity 文件 SHA，而不只相信 index 字段。
8. 负向测试必须覆盖错配 reviewer execution、缺失 frozen delta、bundled self-observation 禁止、主窗审 provider 隔离。

执行必要的只读 CLI 和测试。当前尚无正式正文、final-review-index 和 Owner 决策是正常 bootstrap 状态，不得仅因此判 REVISE。判断标准是生产后是否能 fail closed。

输出 Markdown，固定结构：

- `# Verdict`，单独一行 `ACCEPT` 或 `REVISE`
- `# Blocker Closure`，B-01 至 B-08 逐项 CLOSED/OPEN
- `# New Findings`，blocking/major/minor
- `# Authorization Recommendation`
- `# Evidence Read`

任何 blocking 或 major 必须导致 REVISE。只有全部关闭时，才可建议 Owner 将正式首窗口限定开放为第 1-10 章；第 11+、连续批量和 publish 仍不得开放。
