# Verdict

REVISE

# Blocker Closure

## B-01 — CLOSED

本项目的 66 章生产路线已完成运行时隔离。

证据：

- `project-production-validate` 实测返回 `project_id=hundred-crafts-night-procession`、`chapter_count=66`、`window_count=7`、`valid=true`。
- `volume1-release-status` 只检查 `chapter-0001` 至 `chapter-0066`，窗口严格为 `001-010`、`011-020`、`021-030`、`031-040`、`041-050`、`051-060`、`061-066`。
- 章数和窗口由项目细纲动态派生：[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:51)、[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:62)。
- release 使用动态章集合和窗口集合：[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:22)。
- 旧项目仍保留兼容常量和分支，但显式选择本项目时没有进入当前输出或资产读取链。当前未发现《借天改命账》的 100 章、旧账本或旧 Owner scope 对本项目形成正向授权或状态输入。

## B-02 — OPEN

Canonical baseline 已建立并能检测所列文件的哈希漂移，但没有满足上一版修复合同。

Blocking evidence：

- baseline 的生成白名单没有包括 `audit-contract.v0.1.json`：[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:18)。
- 当前 baseline 因而没有锁定本次正式生产政策本身，尤其是首窗范围、样章分类及 publish 禁令。
- reconciliation 只是四条概括性 `resolved`，没有逐项记录原 Story Bible／蓝图冲突、裁决值、来源和应用目标：[project_reconciliation.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/validation/project_reconciliation.json:6)。
- reconciliation application 只绑定资产库和 manifest 两个哈希，没有绑定设计文档、初始状态、窗口、intent 或 audit contract：[project_reconciliation_application.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/validation/project_reconciliation_application.json:4)。
- validator 会复算 baseline 已列文件的哈希，但不会验证必要 Canonical 文件是否完整列入：[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:416)。

因此 `canonical_baseline_current=true` 只表示“现有清单没有漂移”，不表示“应锁定的事实源完整”。

## B-03 — OPEN

旧通用 scope 已不能直接授权本项目，章节范围也被限制为 1—10；但 review 绑定仍可伪造，尚未形成可靠 Owner 授权链。

Blocking evidence：

- 项目 ID、baseline、mission、禁止 11+／批量／publish 的校验存在：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:2203)。
- 但是 `bound_sol_review_sha256` 和 `bound_antigravity_review_sha256` 只检查非空，不验证是否对应真实文件，也不与 `final-review-index` 中的审查哈希交叉匹配：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:2231)。
- 现有测试明确用 `"a"*64` 和 `"b"*64` 即可使单项授权函数返回 true，证明该绑定目前只是占位字符串：[test_hundred_crafts_production_readiness.py](/Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_hundred_crafts_production_readiness.py:86)。
- 当前磁盘没有 `final-review-index.v0.1.json`，所以整体 readiness 正确保持 `dual_final_review_accepted=false`、两个 bounded authorization 均为 false。

需要把 Owner decision 中的审查哈希解析并验证为本次真实 Sol／Antigravity 报告，而不能只依赖旁路的布尔 readiness 检查。

## B-04 — CLOSED

66 章窗口表达、第 11 章门禁及尾窗均已修复。

证据：

- `story-window-status` 实测七窗全部 `valid=true`，末窗 `061-066` 为六章。
- validator 允许 1—10 章连续窗口，并只允许卷末窗口短于十章：[nrl_story_window.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_story_window.py:90)。
- 本项目窗口统一要求 `source_status=formal_plan`，不再按固定章号误标 calibration：[nrl_story_window.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_story_window.py:162)。
- `prior_window_review_required("chapter-0011")` 实测为 true；门禁从本项目第 10 章后启动：[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:375)。
- release 会校验窗口 verdict、章集合及最终 revision 哈希：[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:450)。

## B-05 — OPEN

九类资产 payload 和 canonical initial state 已接入 context；未知资产、未知字段及 stale before 也会被拒绝。但状态结算合同仍不完整，维护班关键状态没有被真实 delta 驱动。

Blocking evidence：

- 资产库当前有 38 项、完整覆盖九个 family；五名主角和六本 ledger 均存在。
- 编译后的 writer context 保留完整选中资产 payload、`expected_state_deltas` 和 rolling state：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:807)。
- settlement 已拒绝未知资产、未登记字段和 stale before：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:184)。
- lifecycle 规则仍是全资产共享的宽松三态表，允许任意资产 `seed→resolved`，没有资产级 value domain、owner 或 invariant 校验：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:196)。
- 第 33 章虽然叙事上要求维护班正式成立，但其唯一 `expected_state_delta` 写入的是 `char_lin_dai.character.current_state`，不是 `faction_maintenance_team.lifecycle_state: seed→active`：[volume1_production_manifest.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/plans/volume1_production_manifest.v1.json:997)。
- 初始状态正确把维护班记为 `seed`，但缺少一条必须在第 33 章兑现的 faction lifecycle delta：[canonical_initial_state.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/state/canonical_initial_state.v1.json)。
- 没有覆盖未知资产、未知字段、stale before、非法生命周期和重复兑现五类伪造 settlement 的完整负向测试。

因此维护班可能在正文中“成立”，角色状态发生变化，而 faction 的 Canonical 状态仍保持 seed，构成真实状态漂移。

## B-06 — OPEN

项目分支现在会为最终修订调用外部语义 audit，这是实质进展；但 issue 闭环和独立性仍不满足接受条件。

Blocking evidence：

- 正式项目 final audit 会调用外部 reviewer，而不是 deterministic final audit：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:2088)。
- 但 settlement 只阻止 final audit 中未解决的 `blocking` issue；`major` 可以未解决而通过：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:139)。
- settlement candidate 会把初审所有 blocking／major issue 自动写入 `resolved_audit_ids`，条件仅是 final verdict 为 ACCEPT 或 ACCEPT_WITH_WARNINGS；没有逐 issue 的终审确认映射：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:2025)。
- `accept_chapter()` 最终只验证 stage、revision、settlement 及 revision 哈希，没有再次验证 final audit 类型、执行证据或 unresolved major：[nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py:2112)。
- Codex 审查失败后 Antigravity 仍作为 fallback provider 使用，不能同时构成第二份独立意见。
- 当前没有绑定新 baseline 的最终双审 index；旧 Antigravity 文件只接受 controlled sample test，并非正式生产终审：[preprose_independent_review.v0.1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/validation/preprose_independent_review.v0.1.json:5)。
- 七个窗口中未见可解析的文化证据卡引用或文化安全结果绑定。

## B-07 — OPEN

19／29／60 和 41／54 的文字因果已明显修复，五名主角也都有卷一终态、全书终态及卷后残余矛盾；但机器因果合同仍过于形式化，尚无绑定修订后细纲哈希的独立因果 ACCEPT。

证据：

- 第 19 章撤回单方无责目标；第 29 章纳入未识别受影响者；第 60 章把私名争议转为可追索公共责任，三项语义不同。
- 第 29 章显式依赖 `v1.ch019.outcome`，第 60 章显式依赖 `v1.ch029.outcome`。
- 第 41 章建立远端旁路与残件，第 54 章显式依赖 `v1.ch041.outcome` 并物理断开旁路。
- 五名角色资产的三个终态字段完整且卷一／全书终态不同。
- 但 `payoff_id` 是按章号机械生成，validator 只检查字符串唯一，不能识别同义重复兑现：[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:169)、[nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py:381)。
- 每章通常只把第一项资产写成单一 expected delta。第 41／54 章的旁路物质状态均落入 `char_zhou_li.character.current_state`，没有登记为 artifact／foreshadowing 的可结算状态；第 33 章组织成立也存在同样错位。
- 当前不存在绑定修订后 outline／manifest 哈希的独立因果审查 ACCEPT。

所以文学计划层的重复问题基本关闭，但可执行依赖仍可能只在字符串上成立。

## B-08 — OPEN

样章已严格隔离，正式 registry 为空且 manifest 明确从第 1 章开始；但上一版要求的质量证据没有完成。

Major evidence：

- `chapter_registry.v0.20.json` 当前 `chapters=[]`。
- manifest 明确 `formal_production_starts_at=chapter-0001`、`controlled_samples=calibration_evidence_only`、`sample_import_allowed=false`：[volume1_production_manifest.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/plans/volume1_production_manifest.v1.json:7)。
- `continuity_validation.v0.1.json` 仍只给总 verdict 和 `warnings:[]`，没有逐章实际字符数、正文哈希、重复模式、对话比例、抽象／感官指标及语义终审结果。
- 现有 readiness 测试只检查样章不进入 registry，没有覆盖上一版规定的正式首窗质量报告：[test_hundred_crafts_production_readiness.py](/Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_hundred_crafts_production_readiness.py:138)。
- 尚无首窗 1—10 dry-run 质量证据，也没有 Terra／Luna／Sol 分工的逐章执行证明。

# New Findings

## blocking

1. **第 33 章组织成立没有写入组织资产。**
   manifest 和 intent 把“维护班正式成立”结算到林岱的角色状态，而不是维护班的 `faction.status`／`lifecycle_state`。这会造成正文事实、角色状态和 faction Canonical 状态分裂。

2. **Owner review 哈希可以是任意非空字符串。**
   授权函数没有验证两个 review SHA 对应真实审查文件，也没有与 final review index 交叉核对，存在未来误授权路径。

## major

1. **标题和 intent 虽然当前完整且由同一 builder 生成，但没有被 baseline 锁定。**
   baseline 不包含 `chapter_titles.volume1.json` 和 66 个 intent；validator 只做 intent schema 校验，没有逐章比较 outline、manifest、窗口、title registry 与 intent 的标题、资产和 expected delta 是否仍同源。后续手改 intent 可以不触发 baseline drift。

2. **因果状态过度压缩到每章一个“第一资产”字段。**
   这使多资产事件的真实依赖退化为章节 outcome 标签，无法可靠阻止组织、器物、账本或伏笔状态静默不结算。

3. **测试本身包含写盘 preparation。**
   `test_prepare_builds_66_chapters_and_seven_windows` 会重新生成 manifest、initial state、窗口、intent、reconciliation 和 baseline。终审环境不应把该测试当纯验证测试，也不应在未经确认的 dirty worktree 上直接运行。

## minor

- `nrl_volume1_release.py` 仍以旧项目字符串构造兼容路径常量，但 `runtime_path()` 在本项目 CLI 下映射到了正确项目 release root；当前未形成实际污染，建议后续移除以降低误读和回归风险。
- `audit-contract.v0.1.json` 的 `status` 仍为 `audit_in_progress`，符合本次尚未接受的事实，但不能在最终修复完成前改成预先接受。

# Authorization Recommendation

不建议授权首个正式窗口。

当前必须继续保持：

- 第 1—10 章正式正文：禁止；
- 第 11 章及以后：禁止；
- 连续或批量生产：禁止；
- 样章导入正式 registry：禁止；
- release package、上传和 publish：禁止。

只有 B-02、B-03、B-05、B-06、B-07、B-08 全部关闭，新增 blocking／major 全部解决，并取得绑定同一完整 baseline 的 Sol 与独立 Antigravity 最终 ACCEPT 后，才可请求 Owner 单独授权正式第 1—10 章。即使届时授权首窗，第 11 章仍必须等待第 1—10 章逐章接受及窗口审查 ACCEPT；11+、连续批量与发布仍须继续禁止。

# Evidence Read

- [audit-contract.v0.1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/production_readiness/audit-contract.v0.1.json)
- [sol-deep-audit.v0.1.md](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.1.md)
- [story_bible.md](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/design/story_bible.md)
- [outline_tree.md](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/design/outline_tree.md)
- [production_blueprint.md](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/design/production_blueprint.md)
- [project_assets.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/creation_assets/project_assets.json)
- [canonical_baseline.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json)
- [volume1_outline.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/plans/volume1_outline.v1.json)
- [volume1_production_manifest.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/plans/volume1_production_manifest.v1.json)
- [canonical_initial_state.v1.json](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/state/canonical_initial_state.v1.json)
- 七个 `production_runtime/story_windows/window-*.v1.json`
- 66 个 `production_runtime/intents/chapter-*.json`
- [nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py)
- [nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py)
- [nrl_story_window.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_story_window.py)
- [nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py)
- [test_hundred_crafts_production_readiness.py](/Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_hundred_crafts_production_readiness.py)
- `validation/project_reconciliation.json`
- `validation/project_reconciliation_application.json`
- `validation/preprose_independent_review.v0.1.json`
- `validation/continuity_validation.v0.1.json`
- 当前只读 CLI 输出：`project-validate`、`project-production-validate`、`production-readiness`、`production-preflight`、`story-window-status`、`volume1-release-status`、`chapter-runtime-status`
- 未运行完整测试套件：指定测试包含 `project-production-prepare` 写盘行为，与本次“只审查、不修改文件”约束冲突。