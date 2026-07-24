# 《百工夜行录》正式生产开放前独立终审

你是独立文学系统与长篇生产安全审查者。请在当前共享仓库内直接读取证据，独立判断，不要复述或默认接受 Codex Sol 的结论。不得修改文件，不得生成小说正文。

## 必读证据

- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/audit-contract.v0.1.json`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.8.md`
- `projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json`
- `projects/hundred-crafts-night-procession/creation_assets/project_assets.json`
- `projects/hundred-crafts-night-procession/production_runtime/plans/volume1_outline.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/plans/volume1_production_manifest.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/initial_state.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/quality/first_window_quality_contract.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/project-reconciliation.v0.1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-001-010.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-011-020.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-021-030.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-031-040.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-041-050.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-051-060.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/story_windows/window-061-066.v1.json`
- `system/runtime/nrl_project_production.py`
- `system/runtime/nrl_production_runtime.py`
- `system/runtime/nrl_story_window.py`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_hundred_crafts_production_readiness.py`
- `tests/test_volume1_release.py`

## 必查问题

1. 66 章、7 窗口、人物弧线、百工机制、状态账本、冻结意图和跨章因果是否形成可执行且内部一致的卷一生产合同。
2. Terra 写作、Luna 观察、Sol 审稿、Antigravity 独立窗审的角色身份与执行证据是否 fail closed，是否存在自报身份、fallback 顶替、旧哈希复用或无执行证据落盘的绕过。
3. Owner Gate 是否只能开放当前 baseline 下的第 1—10 章；第 11 章及以后、连续批量、release、upload、publish 是否继续被阻断。
4. 状态结算是否拒绝缺失冻结 delta、未知资产、陈旧 before、未声明变化、非法生命周期和模型/产物哈希不一致。
5. 当前 registry 是否为空、没有正式正文，样章是否仅为 calibration evidence，不能混入正式生产。
6. Sol v0.8 的 ACCEPT 是否与当前磁盘证据一致。你必须指出任何 blocking/major，不得为了推进而降级问题。

## 输出格式

Markdown，必须包含：

- `# Verdict`：只能是 `ACCEPT`、`ACCEPT_WITH_WARNINGS` 或 `REVISE`
- `# Independent Findings`
- `# Contract And Gate Verification`
- `# Authorization Recommendation`
- `# Evidence Read`

只有没有 blocking/major 时才可 `ACCEPT` 或 `ACCEPT_WITH_WARNINGS`。即使接受，也只能建议开放正式第 1—10 章；第 11+、连续批量、release package、upload、publish 必须继续禁止。
