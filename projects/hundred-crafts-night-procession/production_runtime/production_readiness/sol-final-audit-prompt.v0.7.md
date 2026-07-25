# 《百工夜行录》正式生产前终审补充核验 v0.7

只读核验，不修改文件，不生成正文。读取以下文件并以当前磁盘为准独立复核：

- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.5.md`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.6.md`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_hundred_crafts_production_readiness.py`

重点确认：

1. v0.6 指出的 major 已修复：`record_independent_window_review()` 在任何写盘前，拒绝缺失 `payload.review_model`，并拒绝 `payload.review_model != execution.model`。
2. 已补充直接调用通用落盘入口的 model mismatch 负向测试，且相关 28 项测试全部通过。
3. v0.5 已接受的其余生产合同、执行身份、Owner Gate、窗口门禁和状态结算结论仍成立。
4. 不得因为当前没有正文或窗审产物而误判系统合同失效；这些缺失应继续使 release/readiness 对应检查 fail closed。
5. 当前正式生产登记表仍为空，不得发现任何已生成正文。

输出 Markdown：`# Verdict`（ACCEPT/REVISE）、`# Delta Verification`、`# Authorization Recommendation`、`# Evidence Read`。只有无 blocking/major 才可 ACCEPT，并且只能建议开放第 1-10 章；第 11+、连续批量、release/upload/publish 继续禁止。
