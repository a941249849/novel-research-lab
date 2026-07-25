# 《百工夜行录》正式生产窗口状态 v0.31

生成时间：2026-07-25

项目：`hundred-crafts-night-procession`

授权窗口：`chapter-0001` 至 `chapter-0010`

## 结论

当前系统基线已完成工程加固，并通过绑定同一基线的 Sol 审查与
Antigravity 独立审查。正式生产运行时已经实际跑通写作、连续性审计、
完整改写、观察、终审、结算和接受链路。

本轮已正式接受 7 章。第 8 至 10 章尚未完成，原因是 Codex CLI 正式
Terra 写作通道触发账户额度限制。系统没有用 Antigravity 冒充 Terra，
也没有把失败候选写入正式注册表。

## 已接受章节

| 章节 | 标题 | 中文字符数 | 状态 |
| --- | --- | ---: | --- |
| `chapter-0001` | 梁失其名 | 3321 | `chapter_accepted` |
| `chapter-0002` | 加固之后 | 3013 | `chapter_accepted` |
| `chapter-0003` | 模型之外 | 3074 | `chapter_accepted` |
| `chapter-0004` | 空角色 | 3772 | `chapter_accepted` |
| `chapter-0005` | 不戴盔 | 3055 | `chapter_accepted` |
| `chapter-0006` | 毛坯街 | 3249 | `chapter_accepted` |
| `chapter-0007` | 守门余响 | 3427 | `chapter_accepted` |

正式注册表与活动章节目录均只包含上述 7 章。

## 第 8 章失败处理

- 第一份候选在结算阶段发现观察状态超出冻结意图，已隔离至
  `production_runtime/quarantine/chapter-0008-20260725T045224Z`。
- 第二份候选来自额度耗尽后的 Antigravity 备用输出，因不满足正式
  Terra 执行身份而被拒绝，已隔离至
  `production_runtime/quarantine/chapter-0008-20260725T050128Z`。
- 两份候选均未进入正式章节注册表，不影响已接受的 1 至 7 章。

## 恢复点

Codex CLI 返回的额度恢复时间为 **2026-07-31 16:42（本地时间）**。
额度恢复后使用唯一续跑命令：

```bash
python3 system/runtime/nrl.py --project hundred-crafts-night-procession produce --until 10
```

运行时会从 `chapter-0008` 继续，不重写已接受章节。

## 持续有效的边界

- `chapter-0011` 及之后未授权。
- 批量连续生产未授权。
- 发布包、上传和公开发布未授权。
- 原始训练语料读取不属于正文生产权限。
- 当前状态不是第一卷完成状态，也不是番茄可发布状态。
