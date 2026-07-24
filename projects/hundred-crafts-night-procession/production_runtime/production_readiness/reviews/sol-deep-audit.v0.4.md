# Verdict

REVISE

# Blocker Closure

## B-01 — CLOSED

项目生产链已隔离为 66 章、七个窗口；当前 registry 为空，历史样稿未进入正式链。`project-production-validate` 实测 `valid=true`，章数 66、窗口数 7。

## B-02 — CLOSED

Canonical baseline 当前完整并通过 SHA-256 复算，覆盖设计、资产、reconciliation、66 章 outline/manifest/intents、七个 story windows、标题与质量合同。实测：

- `canonical_baseline_current=true`
- `canonical_input_set_complete=true`

## B-03 — CLOSED

Owner 授权和 readiness 均复算真实 baseline、Sol review、Antigravity review 文件 SHA，不再只相信 index 字段。当前没有 final-review-index 和 Owner 正式决定，因此保持 `dual_final_review_accepted=false`、`ready=false`，属于正常 bootstrap 状态。

## B-04 — CLOSED

七个窗口及 61—66 六章尾窗表达完整。首窗 packet 会逐章验证 revision、metrics、Terra writer、Luna observer、Sol reviewer 三份执行证据，任一缺失、错配或 provider/model 错误均失败。

## B-05 — CLOSED

Settlement 已同时拒绝：

- 未知资产或字段；
- stale `before`；
- intent 未声明或非法 delta；
- before/after 不匹配；
- 遗漏冻结 intent 要求的 delta。

缺失冻结 delta 的负向测试通过。

## B-06 — OPEN

章节级接受链已经关闭 v0.3 缺口：

- revision 必须绑定 Codex `gpt-5.6-terra` writer execution；
- 复用 draft 时重新生成绑定最终 revision 的 writer execution；
- observation 必须由独立 Codex `gpt-5.6-luna` 执行；
- final audit 必须由 Codex `gpt-5.6-sol` 执行；
- acceptance 复核 chapter、role、artifact path/hash、revision hash、provider、model。

但窗口级 Sol 身份仍不能端到端 fail closed：

1. `record_window_review()` 只检查传入 JSON 自称 `review_provider=codex`、`review_model=gpt-5.6-sol`、`fallback_used=false`，没有独立、hash-bound 的 window reviewer execution artifact。[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:348)

2. 第 11 章门禁重新读取主窗审文件时，只复核 verdict、chapter IDs 和 revision hashes，没有复核 provider、model、fallback 或执行证据。[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:513)

3. 纯内存负向探针证明：把首窗文件模拟为 `review_provider=antigravity`、`fallback_used=true`，只要 verdict/章节/hash 正确，`prior_window_review_required("chapter-0011")` 返回 `false`，即第 11 章未被阻断。

因此 Antigravity 主窗审仍可通过磁盘文件替换或自报 Codex 身份占据 Sol 正式证据位置。

## B-07 — CLOSED

19／29／60、41／54、33 章关键因果状态保持分离并进入可结算资产；五名主角区分卷一终态、系列目标和残余冲突。本轮未发现新的 blocking/major 因果问题。

## B-08 — OPEN

章节级三角色执行合同、bundled observation 禁止和首窗逐章 packet 校验均已实现；14 项只读专项测试全部通过。

但窗口质量链最终仍依赖上述可自报、可替换的 Sol 主窗审文件。现有负向测试只证明 `record_window_review()` 拒绝显式 Antigravity payload，没有覆盖：

- 主窗审文件写入后 provider/model 被篡改；
- 伪造 `codex/gpt-5.6-sol` 自报身份而无真实 execution；
- 第 11 章门禁重新读取错误 provider 的窗审；
- release gate 重新读取错误 provider/model 的窗审。

所以生产后尚不能完整 fail closed。

# New Findings

## blocking

无。

## major

1. **Sol 主窗审缺少 hash-bound execution evidence。** 当前持久化文件中的 provider/model 是 payload 自报字段，不能证明真实 Codex Sol 调用。

2. **跨窗和 release 消费端没有重新验证主窗审身份。** 即使写入入口正常，后续文件替换或错配仍可放行第 11 章及卷级 release 检查。

## minor

1. 应增加“伪造 Codex Sol 自报身份”和“已落盘窗审 provider/model 被篡改”的负向测试，而不只测试显式 Antigravity 输入。

2. `test_final_reviewer_execution_must_bind_exact_audit_and_revision` 会在项目 runtime 下创建临时文件；因本轮严格只读，未执行该单项。其对应实现已静态复核；其余 14 项专项测试全部通过。

# Authorization Recommendation

不建议 Owner 现在开放正式第 1—10 章。

最小剩余修复是：

- 为 Sol 主窗审建立独立 execution artifact，绑定 window ID、审查 artifact path/hash、完整 chapter IDs、revision hash map、provider=`codex`、model=`gpt-5.6-sol`；
- `prior_window_review_required()`、story-window status 和 release gate 每次重新复核该 execution；
- 独立 Antigravity 窗审继续使用不同 artifact 和执行路径；
- 补齐上述篡改、错配和自报身份负向测试。

修复并复审通过后，Owner 最多只能限定开放正式第 1—10 章。第 11+、连续批量生产、release package、上传和 publish 仍不得开放。

# Evidence Read

- 三版 `sol-deep-audit.v0.1/v0.2/v0.3.md`
- `audit-contract.v0.1.json`
- Canonical baseline、38 项九类项目资产
- reconciliation 及 application
- 66 章 outline、manifest、titles 和 intents
- 七个 story windows
- 首窗质量合同及 calibration evidence
- [nrl_project_production.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_project_production.py)
- [nrl_production_runtime.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_production_runtime.py)
- [nrl_story_window.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_story_window.py)
- [nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py)
- [test_hundred_crafts_production_readiness.py](/Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_hundred_crafts_production_readiness.py)
- 当前只读 CLI：`project-validate`、`project-production-validate`、`production-readiness`、`production-preflight`、`story-window-status`、`volume1-release-status`、`chapter-runtime-status`
- 专项只读测试：14 项通过
- 纯内存负向探针：错误 Antigravity 主窗审未阻断第 11 章
- 当前状态：无正式正文、无 final-review-index、无 Owner 正式授权；readiness 和 publish 正确保持阻断
