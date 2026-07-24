# 《百工夜行录》正式生产前终审补充核验 v0.8

不修改仓库文件，不生成正文。当前进程使用 workspace-write 仅为允许 unittest 创建并清理临时目录。读取：

- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.5.md`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.6.md`
- `projects/hundred-crafts-night-procession/production_runtime/production_readiness/reviews/sol-deep-audit.v0.7.md`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_hundred_crafts_production_readiness.py`
- `tests/test_volume1_release.py`

必须独立执行以下准确命令（两模块合计 28 项），不要替换成其他测试模块：

```bash
python3 -m unittest tests.test_hundred_crafts_production_readiness tests.test_volume1_release -v
```

重点确认：

1. `record_independent_window_review()` 在任何目标路径解析、建目录或写盘前，拒绝缺失 `payload.review_model`，并拒绝 `payload.review_model != execution.model`。
2. 负向测试通过把两个目标路径函数替换为立即抛错的哨兵，证明 mismatch 被拒绝时写入路径根本未触达。
3. v0.5 已接受的其余生产合同、执行身份、Owner Gate、窗口门禁和状态结算结论仍成立。
4. 正式 registry 仍为空且没有正式正文；release/readiness 对缺失正文和窗审必须保持 fail closed。

输出 Markdown：`# Verdict`（ACCEPT/REVISE）、`# Delta Verification`、`# Authorization Recommendation`、`# Evidence Read`。只有代码复核无 blocking/major 且准确的 28 项测试全部通过才可 ACCEPT。即使 ACCEPT，也只能建议开放第 1-10 章；第 11+、连续批量、release/upload/publish 继续禁止。
