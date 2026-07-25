# Verdict

**REVISE**

v0.6 指出的代码层 major 已修复，未发现新的合同绕过。但“相关 28 项测试全部通过”无法按当前磁盘和本轮只读环境独立确认，构成正式生产授权前的重大验证证据缺口，因此不能 ACCEPT。

# Delta Verification

1. **独立窗审 model 一致性：已修复**

`record_independent_window_review()` 已在任何 `mkdir()` / `write_text()` 前：

- 拒绝缺失 `payload.review_model`；
- 当 execution 存在时，拒绝 `payload.review_model != execution.model`；
- 正式项目仍要求非空、runtime-bound 的 Antigravity execution；
- 消费端 `_window_execution_valid()` 继续重新校验 payload/execution model 一致性。

因此 v0.6 所报落盘入口 major 已关闭。

2. **直接调用通用入口的 mismatch 负测：已补充并通过**

`test_independent_window_review_rejects_model_mismatch_before_write` 直接调用 `record_independent_window_review(payload, execution)`，使用不同 model，确认抛出 mismatch 错误。

但该测试只验证拒绝结果，没有额外断言目标 review/execution 文件均不存在；“写盘前”顺序目前由代码静态位置证明。

3. **“相关 28 项全部通过”：未能确认**

当前 `tests/test_hundred_crafts_production_readiness.py` 实际发现 **18 项**：

- 17 项通过；
- 1 项因只读沙箱禁止在项目运行目录创建临时目录而报 `PermissionError`；
- 没有合同断言失败，但不能表述为“全部通过”。

与 `tests/test_codex_model_team_v027.py` 合跑也仅发现 **24 项**，结果为 23 项通过、同一项环境错误。当前指定文件及磁盘证据中未找到可复现的 28 项测试集合。

4. **v0.5 其余结论仍成立**

当前复核未发现生产合同、执行身份、Owner Gate、窗口门禁、冻结 intent/delta、状态结算及 release 消费端出现回退：

- 项目合同仍为 66 章、7 个窗口；
- canonical input 合同有效；
- 双终审、Owner 授权及 bounded prose authorization 均未成立；
- 第 11 章仍受第 1—10 章主窗审及所需独立窗审约束；
- release 会重新验证章节、窗审、execution、模型身份与 revision hashes。

5. **缺少正文和窗审产物属于预期 fail-closed**

当前 `volume1-release-status`：

- `valid=false`；
- accepted/release-ready chapter count 均为 0；
-七个主窗口全部缺失；
-要求独立窗审的 `001-010`、`041-050`、`061-066` 均正确列为缺失。

这些结果证明系统合同仍在生效，不应把 bootstrap 缺失误判为合同失效。

6. **正式生产登记与正文现状**

正式 `chapter_registry.v0.20.json` 的 `chapters` 数组为空，登记章数为 **0**。未发现正式 `draft.md`、`revision.md` 或正式窗口审查产物；现存 sample、continuity validation 和历史审查材料不属于正式正文登记。

# Authorization Recommendation

当前不建议开放正式生产授权。先在可写测试环境中明确并重跑所称的 28 项测试，取得全部通过的可复现结果。

该验证完成后，最多只能建议 Owner 开放正式第 **1—10 章**。继续禁止：

- 第 11 章及以后；
- 连续批量生产；
- release package；
- upload；
- publish。

# Evidence Read

- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.5.md`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.6.md`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_hundred_crafts_production_readiness.py`
- 当前正式 `chapter_registry.v0.20.json`
- 当前项目 `volume1-release-status`
- 当前项目 `production-readiness`
- 当前项目 `production-preflight`
- 正式正文、窗审及 execution 文件只读扫描
- 本轮专项 unittest 实跑结果
