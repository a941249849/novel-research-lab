# Verdict

REVISE

# Blocker Closure

## B-01 — CLOSED

项目生产路线保持正确隔离：

- `project-production-validate`：`valid=true`
- 卷一严格为 66 章、七个窗口
- release 只检查 `chapter-0001` 至 `chapter-0066`
- 当前 registry 为空，没有历史样章进入正式生产链

## B-02 — CLOSED

当前 baseline 已完整锁定：

- audit contract
- 项目状态及三份设计文档
- 项目资产库
- 66 章 outline、manifest、initial state、标题
- 66 个 intents
- 七个 story windows
- 正式质量合同及 calibration evidence
- reconciliation 及 application

`validate_project_production()` 同时：

- 复算每个已列文件的 SHA-256
- 按固定必要集合比较 baseline 清单
- 拒绝缺项、额外路径和任一哈希漂移

实测：

- `canonical_baseline_current=true`
- `canonical_input_set_complete=true`
- `project-production-validate valid=true`

## B-03 — CLOSED

Owner 授权函数已经形成三方真实绑定：

- 当前 baseline 文件真实 SHA
- final-review-index 中的 baseline SHA
- index 指向的真实 Sol、Antigravity 文件 SHA
- Owner decision 中的三个对应 SHA

同时校验项目 ID、mission、1—10 章范围和对 11+、连续批量、publish 的禁止项。

专项测试证明任意 `"a"*64`、`"b"*64` 占位 SHA 不能授权。当前没有 final-review-index 属于允许的 bootstrap 状态，系统诚实保持：

- `dual_final_review_accepted=false`
- `bounded_intent_authorized=false`
- `bounded_prose_authorized=false`
- `ready=false`

Minor：`build_production_readiness()` 自身计算 `dual_final_review_accepted` 时只检查 index 字段，未像 Owner 授权函数一样立即复算两个真实审查文件。它目前不会导致误授权，但该诊断布尔值应复用完整三方验证逻辑。

## B-04 — CLOSED

七窗口表达和跨窗门禁保持正确：

- 七个窗口均存在，尾窗为 61—66 六章
- 第 11 章要求 1—10 Sol 窗审
- 因首窗合同要求独立审查，第 11 章还同时要求 Antigravity 窗审
- 两份窗审都绑定实际章节集合和 revision SHA
- 任一缺失、非 ACCEPT 或哈希漂移都会阻断第 11 章

## B-05 — CLOSED

settlement 已具备冻结 intent 驱动的严格校验：

- 拒绝未知资产
- 拒绝未知字段
- 拒绝 stale `before`
- 拒绝 intent 未声明的 delta
- 拒绝与冻结 intent 的 before/after 不一致
- 拒绝重复写入当前值
- lifecycle 必须严格匹配该章冻结 intent，不再使用全资产共享宽松状态表
- 只读取更早且已接受章节的 settlement

第 33 章现在明确结算：

- `faction_maintenance_team.lifecycle_state: seed → active`
- `faction_maintenance_team.faction.status`
- `ledger_team_authority.state_ledger.value`

全 manifest 只有第 33 章具有维护班 `seed→active` 合同，运行时也禁止其他章节将其激活。

19／29／60 分别结算到角色状态和责任账实体状态；41 建立远端旁路及残件，54 从该真实状态物理断开旁路，不再只是机械章节标签。

## B-06 — OPEN

final audit 的 revision 绑定和 issue 闭环已经修复：

- final audit 绑定 revision SHA 和 context SHA
- 明确列出初审全部 blocking/major issue ID
- 缺少任一 ID、final 中出现 blocking/major、或 verdict 为 `REWORK_REQUIRED` 均不能进入 settlement
- candidate 只复制 final audit 已明确确认的 `resolved_prior_issue_ids`
- acceptance 再次核对 final audit 的 revision SHA、verdict、实质问题和 execution 文件存在

但执行证据仍没有完全 fail closed：

1. `accept_chapter()` 只检查 `final_audit.execution.json` 存在，没有核验其中：

   - `chapter_id`
   - `audit_artifact_sha256`
   - provider/model 身份
   - 是否确为所接受 final audit 的执行记录

2. final semantic audit 可以由 Antigravity fallback 完成；这本身可作为 provider fallback，但不能被当成正式质量合同要求的 Sol 执行证据。

3. `dispatch_window_review()` 也允许 Antigravity fallback，而 `record_window_review()` 不要求主窗审 provider 必须是 Sol/Codex。这样同一个 Antigravity 路由理论上可以同时充当“Sol 窗审”和独立 Antigravity 窗审，独立性没有被机器证明。

这属于 major：语义内容门禁已成立，但执行者身份与独立执行证据仍可被形式文件替代。

## B-07 — CLOSED

关键因果状态已经落入可结算资产：

- 19：撤回单方无责目标
- 29：未识别受影响者进入核查和补偿范围，依赖 19
- 60：旧案转成可追索但未清偿的公共责任，依赖 29
- 41：登记远端旁路与可重接残件
- 54：物理断开该旁路并公开重接责任，依赖 41
- 33：正式建立维护班、权限及退出规则

三条父亲线变化语义、资产状态和物质行动均不同。41／54 的 before/after 形成真实连续状态，不再仅依赖 `v1.chNNN.outcome` 标签。

五名主角均区分卷一终态、全书目标与残余冲突。当前未发现新的 blocking/major 因果冲突。

## B-08 — OPEN

历史样章处理已经正确：

- 每章记录真实中文字符数和正文 SHA-256
- 明确标记 `calibration_evidence_only_not_formal_acceptance`
- 每章均为 `NOT_APPLICABLE_CALIBRATION_ONLY`
- 没有历史样章进入正式 registry
- 没有将历史质量结论提升为正式 ACCEPT

无正式正文时，首窗质量状态也诚实保持：

`contract_ready_no_formal_prose`

问题在于正式正文产生后的执行门禁没有落实质量合同声明：

1. 合同要求每章具有 `writer_execution`、`observer_execution`、`reviewer_execution`，但 `build_window_review_packet()` 实际只强制：

   - revision metrics 存在
   - final audit execution 存在
   - 中文字符数 3000—4200
   - final audit 无 blocking/major

2. runtime 没有为 writer 和 observer 持久化并验证独立 execution artifact。

3. pipeline 优先使用 writer bundle 自带的 observation；当 revision 与 draft 相同时，可完全绕过 Luna observer。这样同一写作调用可以同时提供正文和事实观察，不符合 Terra 写作、Luna 观察分离，也违反 `same_model_self_certification_allowed=false`。

4. observer 即使被调用，返回的 provider/model 只存在于函数返回值，没有写入 registry 中可供 acceptance、窗审和 release 复核的执行证据。

因此“无正文时 contract-ready”是诚实的，但生产后不能对 Terra/Luna/Sol 三方执行证据 fail closed，属于 major。

# New Findings

## blocking

无新增 blocking。

## major

1. **正式质量门禁没有执行其声明的三角色证据合同。**
   writer/observer execution 未被持久化和强制验证，writer bundled observation 可以替代 Luna 独立观察。

2. **Sol 与独立 Antigravity 窗审的执行身份未完全隔离。**
   主窗审允许 Antigravity fallback，却仍可占据 Sol 窗审位置；机器门禁没有阻止同一 provider 同时承担两份审查。

3. **final audit execution 只验存在、不验内容绑定。**
   acceptance 未复核 execution 中的 audit SHA、chapter ID、provider 和 model，不能排除占位或错配执行证据。

## minor

1. `dual_final_review_accepted` 的 readiness 诊断没有复用 Owner 授权函数的真实文件哈希验证；虽然当前不会绕过最终授权，但可能显示误导性中间状态。

2. 当前专项测试覆盖 settlement 和 baseline 修复，但没有负向测试证明：

   - 缺 writer execution 时首窗失败
   - 缺 observer execution 时首窗失败
   - bundled self-observation 不能满足 Luna 证据
   - Sol 与 Antigravity 窗审 provider 相同会失败
   - final audit execution SHA 错配会阻断 acceptance

# Authorization Recommendation

不建议 Owner 现在开放正式第 1—10 章。

应先关闭 B-06、B-08：

- 为 Terra writer、Luna observer、Sol final reviewer 分别持久化 hash-bound execution artifact；
- acceptance 与窗口质量门禁逐份复核 chapter、revision/audit SHA、provider、model 和角色；
- 正式 observation 不得由 writer bundle 自证；
- Sol 主窗审必须留下 Sol/Codex 身份证据；
- 独立 Antigravity 窗审必须是不同执行路径，不能由主窗审 fallback 冒充；
- 补齐上述负向测试。

关闭后，Owner 最多只能限定授权正式第 1—10 章。第 11+、连续批量、release package、上传及 publish 仍不得开放；第 11 章必须等待 1—10 全部接受、Sol 窗审 ACCEPT 和独立 Antigravity 窗审 ACCEPT。

# Evidence Read

- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.1.md`
- `production_runtime/production_readiness/reviews/sol-deep-audit.v0.2.md`
- `production_runtime/production_readiness/audit-contract.v0.1.json`
- `creation_assets/canonical_baseline.json`
- `creation_assets/project_assets.json`
- `validation/project_reconciliation.json`
- `validation/project_reconciliation_application.json`
- `production_runtime/plans/volume1_outline.v1.json`
- `production_runtime/plans/volume1_production_manifest.v1.json`
- `production_runtime/state/canonical_initial_state.v1.json`
- `production_runtime/chapter_titles.volume1.json`
- 66 个 `production_runtime/intents/chapter-*.json`
- 七个 `production_runtime/story_windows/window-*.v1.json`
- `production_runtime/quality/first_window_quality_contract.v1.json`
- `production_runtime/quality/calibration_quality_evidence.v1.json`
- `system/runtime/nrl_project_production.py`
- `system/runtime/nrl_production_runtime.py`
- `system/runtime/nrl_story_window.py`
- `system/runtime/nrl_volume1_release.py`
- `system/production_runtime/schemas/continuity_audit.schema.json`
- `system/production_runtime/schemas/story_window.schema.json`
- `tests/test_hundred_crafts_production_readiness.py`
- 只读 CLI：`project-production-validate`、`production-readiness`、`production-preflight`、`story-window-status`、`volume1-release-status`、`chapter-runtime-status`
- 专项测试：11 tests，全部通过
- 当前磁盘状态：无正式章节；`production-readiness ready=false`；publish 仍被阻断