# Verdict

REVISE

v0.5 的唯一 minor 已关闭，但第二项修复未完整落实。发现 1 个新的 **major**：独立窗审通用落盘入口未在写入前强制 `payload.review_model == execution.model`。

# Delta Verification

1. **无主窗审时独立窗审不得误报：已修复**

当前 `volume1-release-status`：

- `all_required_independent_window_reviews_accepted=false`
- `missing_or_rejected_independent_windows` 正确包含：
  - `001-010`
  - `041-050`
  - `061-066`

这与三个窗口合同中的 `independent_antigravity_required=true` 一致。实现会在主窗审缺失时，同时累计独立窗审缺失：[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:733)。

2. **独立窗审 payload/execution model 一致性：未完整修复，major**

消费端已经 fail closed：`_window_execution_valid()` 要求 `review_model == execution.model`，[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:157)。

标准 dispatch 路径也会把同一个 `used_model` 写入两者。

但通用落盘入口 `record_independent_window_review()` 只检查 `execution.model` 非空，没有检查其与 `payload.review_model` 相等，随后直接写入两个文件：[nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py:493)。

因此，调用者可提交 model 不一致的 payload/execution，并使不一致证据落盘。虽然后续 readiness 会拒绝它，暂时不能绕过 release，但这仍违反明确的落盘证据一致性合同，不能确认 v0.5 ACCEPT 继续成立。

3. **专项验证**

以下 3 项只读专项测试通过：

- 第 11 章在缺少前窗审时保持阻断。
- 自报 Sol、无 execution 的主窗审被拒绝。
- 第 11 章重新核验已落盘窗审身份并正确阻断。

主进程报告的完整测试结果为 342 tests 全部通过；本轮未重复运行完整套件。

# Authorization Recommendation

当前不建议开放正式生产授权。

修复要求：`record_independent_window_review()` 必须在任何写盘发生前拒绝缺失 `review_model` 或 `payload.review_model != execution.model`，并补充直接调用落盘入口的负向测试。

修复并复核通过后，也只能建议开放正式第 1—10 章。以下范围继续禁止：

- 第 11 章及以后；
- 连续批量生产；
- release package；
- upload；
- publish。

# Evidence Read

- [sol-deep-audit.v0.5.md](/Users/liuneng/Documents/Novel%20Research%20Lab/projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.5.md)
- [nrl_volume1_release.py](/Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_volume1_release.py)
- [test_hundred_crafts_production_readiness.py](/Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_hundred_crafts_production_readiness.py)
- 七个 `story_windows` 合同
- 当前 `volume1-release-status`
- 三项只读专项 unittest
- 主进程提供的完整测试结论：342 tests passed