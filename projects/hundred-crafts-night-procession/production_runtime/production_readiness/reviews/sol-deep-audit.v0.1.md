# 《百工夜行录》正式生产前深层全方面审查 v0.1

审查日期：2026-07-19
审查范围：卷一正式生产门禁；只审查，不接受样稿为正式章节，不授权正文或发布。

## VERDICT

`REVISE`

当前不能开放正式生产。设计层已经具备可生产的核心，但项目专属 Canonical、Owner scope、66 章窗口／发布合同、章节状态结算和语义终审尚未形成同一条可执行链。现有通过项证明了样章试验有价值，不证明正式运行时已安全。

## BLOCKERS

### B-01：正式运行时仍进入《借天改命账》的 60／100 章生产路线

实测 `production-preflight --project hundred-crafts-night-procession` 为 `valid:false`：仍要求 60 章 manifest，并报出 `state_ledger_protagonist_strain`、`state_ledger_mother_life_lamp_countdown` 等旧项目账本。`volume1-release-status` 又要求 100 章及十个十章窗。两者互相也不一致，均不等于本项目 66 章。

最小可验证修复条件：

1. 项目专属 preflight 输出必须含 `project_id=hundred-crafts-night-procession`、`volume_chapter_range=[1,66]`、`valid=true`；输出全文不得出现 `borrowed-heaven`、《借天改命账》、60 章或 100 章要求。
2. release status 必须只检查 `chapter-0001` 至 `chapter-0066`，且窗口集合严格为 `001-010`、`011-020`、`021-030`、`031-040`、`041-050`、`051-060`、`061-066`。
3. 加入项目隔离回归测试：在两个项目资产同时存在时，本项目 preflight、readiness、release 三个命令读取路径必须全部位于本项目工作区或明确列入白名单的共享 schema／研究目录。

### B-02：项目 Canonical baseline 与 reconciliation 不存在，Canonical 文档彼此矛盾

项目内 `creation_assets/canonical_baseline.json`、`validation/project_reconciliation.json`、`validation/project_reconciliation_application.json` 均不存在。`production-readiness` 因 reconciliation 未接受／未应用而失败；其输出虽实际映射到项目文件，仍以旧项目路径名报告 Canonical 输入，并未把 `production_blueprint.md` 与 `volume1_outline.v1.json` 纳入锁定集合。

设计文档也未完成同一状态解释：Story Bible 仍称岭南、高原、医药顾问及卷一细纲为“阻断正文”的当前未决，生产蓝图却把前两项和顾问契约标成完成；Story Bible 说卷一越线案例仍待修改，细纲和连续性测试又已经执行了该案例。

最小可验证修复条件：

1. 建立项目专属 baseline，至少逐项锁定 audit contract、Story Bible、大纲树、生产蓝图、九类资产库、66 章细纲及项目状态，记录项目相对路径和 SHA-256；readiness 必须复算哈希而不是只验证文件存在。
2. 建立并应用项目专属 reconciliation；机器报告必须列出上述文档的状态冲突并显示全部已裁决，不能复用旧项目 verdict 或路径键。
3. `production-readiness` 的 `canonical_inputs` 必须只显示本项目路径，`project_reconciliation_accepted/applied=true`，且任一 Canonical 文件改动后 readiness 必须 fail closed。

### B-03：Owner scope 未按项目隔离，旧授权会被误认作本项目授权

`owner_gate_decisions.json` 中本项目只有非连续样章与第10—27章连续性测试授权，且明确禁止连续生产和第28章以后。没有正式第一窗授权。然而 `production-readiness` 对本项目报告 `bounded_intent_authorized=true`、`bounded_prose_authorized=true`；原因是 runtime 接受全局旧 scope `bounded_chapter_intent_v0.20`／`bounded_chapter_runtime_v0.20`，没有绑定 `project_id`、baseline 哈希或本次 mission。

最小可验证修复条件：

1. Owner gate 判定必须同时匹配项目 ID、明确章节／窗口范围、有效 mission、当前 baseline SHA-256 和禁止范围；旧项目 decision 对本项目的正向授权计数必须为零。
2. 在没有新决定时，第一章 intent/prose 两个授权检查必须均为 false；Owner 新决定最多只可授权 `chapter-0001` 至 `chapter-0010`。
3. 负向测试必须证明：篡改 project ID、baseline 哈希、过期 mission、仅给通用 scope、试图生成第11章，均被拒绝。

### B-04：66 章 story-window 合同不可表达，第一窗审查也没有挡住第11章

story-window schema 和 validator 强制恰好十章；builder 只允许 21、31……91 起窗；当前窗口数为 0。61—66 因而无法表达。validator 还把第15章以前一律要求为 `accepted_calibration`，会把本项目新写的正式章节误标为校准资产。`prior_window_review_required()` 对第20章以前直接返回 false，故第一窗 1—10 未审也不会阻断第11章。

最小可验证修复条件：

1. 窗口由项目卷 manifest 驱动，支持首窗 1—10 和尾窗 61—66；正式章节的 `source_status` 不得由固定章号推断。
2. story-window status 在开写前必须列出七个 production-ready/frozen 窗口意图，至少首窗先冻结；每窗包含起始快照、因果前置、逐章预期状态变化和窗末兑现。
3. 集成测试必须证明：未接受 1—10 窗审时第11章被阻断；接受后第11章可进入 intent；未接受 51—60 窗审时第61章被阻断；61—66 六章窗可校验、审查并进入卷级 release gate。

### B-05：章节 runtime 可以通过 Schema，却不能可靠驱动或结算九类资产

资产库有 38 项并覆盖九个 family，Schema 校验通过；但这不等于可运行：

- `expected_state_deltas` 在 chapter intent 中是必填项，却没有进入编译后的章节 context。
- writer compact context 抛弃角色目标／冲突／弧线／能力、器物成本与限制、技法前置、关系边界、伏笔窗口以及状态账 invariants，只留下名称、family、lifecycle 和少量 constraints。
- 六本状态账只有类型、更新规则和不变量，没有第一章可加载的具体初值；空 registry 也不能补出起始状态。
- observation／settlement schema 接受任意 `asset_id`、`field_path` 和 `before`；结算只比对 Luna 自己观察出的事实，不校验资产存在、旧值等于当前 Canonical 值、字段合法、lifecycle 转换或账本不变量。
- `faction_maintenance_team` 在资产库从第一章即为 `active`，大纲却到第33章才“正式组成”；这会向写手提前泄露已成立状态。

最小可验证修复条件：

1. 第一章编译包必须机器断言包含其 `expected_state_deltas`、选中资产的 family payload、相关关系边界和六本账的 Canonical 初值；prompt 裁剪不得删除硬约束。
2. 为每个可结算字段建立允许路径、值域、初值、合法转换和 owner/invariant 校验；未知资产、未知字段、stale `before`、非法 lifecycle 回退及重复兑现必须使 settlement 失败。
3. 修正维护班的初始 lifecycle，并用测试证明只有第33章的已接受 delta 才能使其进入正式成立状态。
4. 用一个故意伪造的 observation/settlement 回归包验证上述五类错误全部被拒绝。

### B-06：章节接受链没有语义终审，初审问题也不会被最终结算追踪

当前只有每逢五的章节在初稿阶段调用外部语义 reviewer；其余初审是本地字数／句式指标。修订后的 `final_audit` 总是 deterministic，只检查形式指标。settlement 校验只读取 final audit 的 blocking issue，初审 issue 不会自动带入，自动候选还固定写 `resolved_audit_ids=[]`。因此一章可能在角色、因果或文化事实仍错时被标为 `chapter_accepted`。

Antigravity 在实际代码中是 provider 失败后的替补，不是独立意见；这不能构成生产蓝图所说的独立结构与文学审查。

最小可验证修复条件：

1. `chapter_accepted` 前必须存在绑定最终 revision SHA-256 的语义 final audit；deterministic 指标只能提供证据，不能单独给出接受 verdict。
2. 初审所有 major/blocking issue 必须以稳定 issue ID 贯穿 revision、final audit、settlement；未逐项标记 resolved 且由终审确认时 acceptance 必须失败。
3. 每个正式窗口必须有绑定十章（尾窗六章）最终哈希的 Sol 窗审；至少首窗、每个机制高风险窗及卷终窗再有独立 Antigravity 意见，不能把 fallback execution 当作第二意见。
4. 文化高风险章节（卷一至少含粤剧角色／盔头、旧船体与地方口述）必须在窗合同中绑定可解析的证据卡和文化安全检查结果；source ref 无法解析时该章不得接受。

### B-07：66 章细纲存在已证实的重复兑现和未建立的因果跳步

1. 第19章连续性稿已经实际撤回“无责认定”旧申请，新申请进入行为与后果核查；第29章却再次以“撤回父亲无责认定申请”为不可逆变化。第60章又写“不再继承父亲免责目标”。同一人物转折被兑现三次。
2. 第18—19章建立父亲拆除自动代偿且知道洪灾代价；第54章旧装置却能“重新接管”，此前没有建立仍存旁路、残件、远端节点或重连主体。
3. 第10章已有五人互审，第27章已有团队决策规则，第33章才正式成组；缺少清晰的“临时协作—受限复任—组织成立”状态链。
4. 五名核心角色资产只各有一个从起点直达终局的 arc；卷一已分别兑现公开完整责任、地方证据入模、角色拒绝／卸装、期限化转舱、记录连接补偿等目标，后十四卷缺少明确的卷一中间态与残余错误。
5. 第55章完成实体高潮后，第56—65章连续落在验收措辞、账单、公开、试任、月表、地图核对、记新债和回家，制度解释与结算密度过高；若不重排，后段很容易从人物行动退化为机制说明。

最小可验证修复条件：

1. 细纲逐章增加稳定的 `requires_state_ids`、`establishes_state_ids`、`delta_type` 与 `payoff_id`；validator 必须证明所有 requires 来自初始快照或更早章节、非可重复状态只建立一次、无未声明回滚。
2. 第19章保留撤回无责目标；第29章与第60章必须改为不同且依赖第19章的新后果，三个 payoff ID 不得相同或同义映射。
3. 第54章之前必须有一个可观察章节建立“仍可接管”的物质路径及责任主体；否则第54章 validator 失败。
4. 角色资产必须区分 `volume1_terminal_state` 与 `series_target_state`，并列出卷末仍会制造选择成本的 residual conflict；两者相同则资产验证失败。
5. A6 每章标注 on-page material action 和主要 delta 类型；至少六章的主 delta 必须是 material/resource/relationship 中之一，不能全部只落在 information/document/authority。修订后再取得绑定细纲哈希的独立因果审查 `ACCEPT`。

### B-08：样稿测试的质量结论没有覆盖其自订下限，不能作为正式质量门禁证据

连续性合同规定每章 2600—3400 中文字符。用正式 runtime 的汉字计数方法复核，第11—23章及第27章分别约 2317—2582 字，14 个新生成章节全部低于 2600；其中第11—13、15—17、21—23章还触发句首重复指标。现有 validation 报告没有逐章字数或文风指标，却给出 `warnings:[]`。这说明“continuity_test_passed”只足以证明状态链试验，不足以证明 Terra/Luna/Sol 路由已控制篇幅与 AI 味。

最小可验证修复条件：

1. 正式首窗 dry run 必须输出逐章中文字符、重复模式、对话比例、抽象／感官指标及语义审查结果；任一硬下限失败时 window verdict 不得为 ACCEPT。
2. validation 报告必须保留实际测量值和正文 SHA-256，不能只记录总 verdict。
3. Terra 负责写作、Luna 负责事实抽取、Sol 负责语义裁决的职责必须分别留下执行证据；同一模型自证或 fallback 冒充独立复核均判失败。

## CANONICALIZATION_DECISION

唯一方案：**正式生产从第1章开始。**

理由：正式 registry 为空，runtime 本身要求第一章在空 registry 上初始化，后续章必须有立即前章 `chapter_accepted`；因此从第28章续写在工程上不可达。文学上，第8—27章及49—51章建立的状态来自非连续测试合同，未经历项目正式 baseline、逐章 intent、context、观察、语义终审、结算与接受链，且第19章状态已经与第29章细纲冲突。把这些文本导入会在正式生产开始前制造双重事实源。

既有第8—27、49—51章的唯一分类是：**校准证据**。它们不是正式正文，也不是待导入候选。可以用于识别有效写法、失败节奏、文化边界和状态测试用例；不得复制为正式章节、不得向 registry 补登记、不得把其哈希或叙事细节写入正式初始状态。正式第1—66章应按修复后的 Canonical 重新生产；设计层已裁决的规则可保留，样稿新增措辞与事件不自动晋升。

## VOLUME_CAUSALITY

卷一的主因果骨架成立：旧梁退构 → 风险转移到戏楼／水网 → 居民进入利害关系 → 父亲责任从私案变公共账 → 可拆节点与有限维护合同 → 全国节点显形。问题不在“没有故事”，而在状态粒度不足，使同一转折被不同章节重复命名。

必须保住的结构优势包括：第14章把救上游的代价落到下游；第17章使异议获得执行力；第26—27章拒绝个人献祭；第49—55章把报废、工期、生计、角色强制与暴雨抢修压到同一实体危机。需要修复的是第19／29／60的父亲线、54章装置重接因果、10／27／33团队成立链、五人跨卷残余弧，以及55章之后实体后果不足。

## RUNTIME_AND_GATES

| 环节 | 当前事实 | 判定 |
|---|---|---|
| 项目隔离 | workspace 与资产／registry 路径已项目化；默认项目仍是旧项目，通用 Owner scope 会串权，preflight/release 仍读旧尺度 | BLOCKER |
| Canonical baseline | 项目 baseline/reconciliation 缺失，readiness fail；Canonical 状态描述互相冲突 | BLOCKER |
| Owner scope | 样稿与连续性测试授权边界写得清楚；正式首窗没有授权，runtime 却误报已授权 | BLOCKER |
| chapter runtime | 顺序、哈希、阶段机和 accepted immutable 方向正确；context 裁剪与 settlement 校验不足 | BLOCKER |
| story windows | 当前 0 窗，只支持固定十章和旧章号策略 | BLOCKER |
| release gate | 当前硬编码 100 章；不会正确结算 66 章 | BLOCKER |
| 项目状态 | `content_authorized=false`、`ready_for_prose=false`、`publish_authorized=false` 与事实相符 | KEEP |

`project-validate` 当前也为 false，因为隔离扫描把审计提示中用于描述风险的旧项目名称当成跨项目污染。这是验证器边界错误：审计证据可以提及对照项目，Canonical／生产输入不能串入。修复后应分别扫描“可执行输入”和“只读审计证据”，不能简单删除风险证据来换绿灯。

## MODEL_TEAM_AND_QUALITY

Terra 写作、Luna 事实观察、Sol 高风险规划／审查的分工在概念上合适，Antigravity 也可作为供应商故障备用；但配置存在不等于门禁有效。当前最危险的缺口是：Luna 的输出可自洽地把错误旧值写进 settlement，Sol 不审每章最终修订，Antigravity 多数时候只是失败替补，窗口级独立审查尚未存在。

控制 AI 味不能只靠禁词和字面指标。首窗应同时检查：事件是否重复换词、人物是否轮流代表观点、工艺是否只剩解释、生活压力是否真正改变选择、结尾是否同构、角色语气是否可区分。文化控制应把可用事实与不可用符号写进项目证据卡并传入相关窗口，而不是只给“不得挪用”一句禁令。卷一涉及的药品、冷链和伤情只可作为生活后果，不给诊疗建议；只要维持该边界，医药专家签字可继续保留为卷九专属 gate。

## DEFERRED_DEBTS

以下不阻断修复后的卷一首窗：

1. 卷二至卷十五的逐章细纲、十二节点全部地域实现和三年期限的跨卷月度明细；须在各卷冻结前补齐。
2. 卷九医药顾问对具体药材、转性和公共卫生情节的逐章签字；当前仍应是卷九正文 blocker，不必前置为卷一全局 blocker。
3. 平台格式、番茄上传包、营销文案与自动发布；当前没有发布授权，本轮无需建设。
4. 样稿中的非阻断文字问题，包括冻结锚点第26章的“第十章”制作层回指；因为样稿不进入正式正文，无需为导入而返修。
5. Antigravity 的更多供应商冗余；只要正式窗已有真正独立复核，额外第三备用可后置。

## MINIMUM_REPAIR_SET

按以下顺序完成，缺一项均不得重新申请 `ACCEPT_FORMAL_PRODUCTION`：

1. 建立项目专属 baseline/reconciliation，裁决设计文档状态冲突并锁定 66 章事实源。
2. 将 preflight、readiness、Owner gate、story-window、release 全部改为项目 manifest 驱动；清除 60／100 章与旧账本串路。
3. 修订卷一细纲和角色资产：关闭19／29／60重复兑现、补54前置、明确10／27／33组织状态、拆分卷一中间态与系列终局。
4. 为九类资产补可执行初值、合法字段／转换、不变量和 lifecycle；确保完整 payload 与预期 delta 进入 writer/observer context。
5. 加固章节接受链：最终语义审查、issue 闭环、stale-before/unknown-asset 拒绝、首窗及尾窗门禁。
6. 建立七窗合同并先冻结 1—10；运行无正文 dry run，证明第11章受第一窗审查阻断、61—66可表达。
7. 重跑项目验证、production readiness、production preflight、story-window status、chapter runtime dry run、release dry run；所有输出须 `valid=true` 且绑定同一 baseline SHA-256。
8. 对修订后的 Canonical 与机器报告重新进行一次独立深审；只有新报告为 `ACCEPT_FORMAL_PRODUCTION` 后，才可请求 Owner 单独授权第1—10章。

## AUTHORIZATION_BOUNDARY

本报告不授权任何小说正文、样稿导入、registry 补登记、第28章续写、批量生产、release package、上传、发布或外部传播；也不把 audit contract 中的期望 verdict 解释为预先接受。

当前有效边界保持：`content_authorized=false`、`continuous_prose_authorized=false`、`publish_authorized=false`。修复与复审通过后，Owner 仍须提交绑定新 baseline 的独立决定；首次最多授权正式第1—10章。第11章只能在第1—10章逐章接受且窗口审查接受后另行开放。
