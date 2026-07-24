VERDICT: ACCEPT

# 《百工夜行录》文学语义完整性 v0.29 最终独立复审

审查日期：2026-07-24

canonical baseline SHA-256：

`af8fadce1b6d52c1c47f25a5d6f3437a056ee8c201d69625d1f50ab485cb09c4`

审查方式：以当前磁盘为准，对上轮三个阻断项做静态调用链检查、临时隔离状态下的内存对抗重放、CLI 校验、专项回归和全量测试。除覆盖本报告外，未修改运行代码、Schema、测试、项目资产、canonical baseline、chapter registry 或 Owner 决策。

## 最终结论

ACCEPT。

上轮三个阻断项均已在实际执行路径关闭：

1. production readiness、preflight、writer 和 prose entry gate 均按显式目标章节检查实时授权；011-020 窗口对 chapter-0011 有效，对 chapter-0021 无效。
2. Unicode 不可见字符、仅组合标记、纯标点及其他无字母/数字语义证据均被共享 validator 拒绝；dispatch、ingest、accept 均 fail closed 且不推进状态。
3. isolated project 直接调用 deterministic audit 会在读取 registry 前失败；CLI 和正式 pipeline 没有发现可绕过模型初审/终审的等价入口。

未发现由本轮修复引入的新 blocking regression。

本结论只接受 v0.29 文学语义与运行门禁完整性，不等同于正文生产授权。当前项目仍处于 Owner Gate，`content_authorized=false`，正式 chapter registry 为空，`production-readiness` 仍应返回 blocked。

## 1. 显式目标章节与窗口授权

### 静态调用链

`build_production_readiness(chapter_id)` 对 isolated project：

- 使用显式 `chapter_id`，缺省时才计算下一待生产章节；
- 根据 `volume1_windows()` 动态计算所属窗口；
- 将同一目标章节传给 intent 和 prose authorization；
- 动态生成 `target_window`、status 和 next action。

证据：

- `system/runtime/nrl_production_runtime.py:2948-3023`
- `system/runtime/nrl_production_runtime.py:2864-2928`

所有关键入口均传递目标章节：

- preflight：`system/runtime/nrl_production_runtime.py:879-885`
- chapter initialization：`system/runtime/nrl_production_runtime.py:958-969`
- writer prompt：`system/runtime/nrl_production_runtime.py:1058-1068`
- prose entry gate：`system/runtime/nrl_production_runtime.py:1122-1139`
- revision ingest：`system/runtime/nrl_production_runtime.py:2348-2367`
- revision dispatch：`system/runtime/nrl_production_runtime.py:2385-2402`
- acceptance：`system/runtime/nrl_production_runtime.py:2721-2737`

### 对抗重放

在临时 workspace 中构造：

- current baseline binding；
- Sol 与 Antigravity 双审查文件和精确哈希；
- `content_authorized=true`；
- chapter-0011 的 intent 与 prose 双授权；
- `outside-window-011-020`、bulk、raw corpus、publish 四项禁止范围；
- `hundred-crafts-night-procession-volume1-window-011-020-v1` mission。

结果：

```text
chapter-0011 intent authorization = true
chapter-0011 prose authorization = true
chapter-0021 intent authorization = false
chapter-0021 prose authorization = false

build_production_readiness("chapter-0011").ready = true
target_chapter_id = chapter-0011
target_window = [11, 20]
status = ready_for_formal_window_011_020

build_production_readiness("chapter-0021").ready = false
build_production_preflight(..., "chapter-0011").valid = true
build_production_preflight(..., "chapter-0021").valid = false
validate_prose_entry_gate("chapter-0011").valid = true
validate_prose_entry_gate("chapter-0021").valid = false
build_chapter_writer_prompt("chapter-0011") = pass
build_chapter_writer_prompt("chapter-0021") = blocked at preflight
```

结论：chapter-0011 可以在 011-020 授权下进入对应入口，chapter-0021 无法串用该窗口授权；上轮 chapter-0001 缺省锁死问题已关闭。

## 2. 无语义审计证据拒绝

### Schema 与共享 validator

continuity audit Schema 对 11 个维度全部要求：

- 字段必需；
- array `minItems=1`；
- item 为非空字符串并匹配 `\S`。

证据：`system/production_runtime/schemas/continuity_audit.schema.json:12-55`

共享 `validate_literary_audit_evidence()` 进一步执行 NFKC normalization，并要求每个 evidence item 至少包含一个 Unicode category 首字母为 `L` 或 `N` 的字符。

证据：`system/runtime/nrl_production_runtime.py:2000-2044`

该 validator 被三条正式路径复用：

- model dispatch：`system/runtime/nrl_production_runtime.py:2239-2261`
- external audit ingest：`system/runtime/nrl_production_runtime.py:2305-2323`
- chapter acceptance final audit：`system/runtime/nrl_production_runtime.py:2742-2757`

### 对抗输入

以下内容逐项作为单一维度 evidence 重放，均返回 invalid：

```text
empty string
ASCII spaces
U+00A0 NO-BREAK SPACE
U+200B ZERO WIDTH SPACE
U+2060 WORD JOINER
U+FEFF ZERO WIDTH NO-BREAK SPACE
combining marks only
ASCII punctuation only
CJK punctuation only
emoji only
```

包含零宽字符但同时有真实中文证据的字符串正常通过，证明实现拒绝的是无语义内容，不是机械拒绝全部含格式字符的文本。

路径级重放结果：

```text
dispatch = invalid; registry not loaded; no audit artifact written
ingest = RuntimeError; registry not loaded; no audit artifact written
accept = RuntimeError; acceptance not written; registry not saved
```

结论：上轮 U+200B/U+2060/U+FEFF 和纯标点绕过已关闭，且失败发生在状态推进之前。

## 3. deterministic audit 旁路

`record_deterministic_chapter_audit()` 现在首先检查 active project；除 `borrowed-heaven` 外立即抛出 `legacy-only` 错误。

证据：`system/runtime/nrl_production_runtime.py:2095-2100`

isolated project 直接调用重放结果：

```text
result = RuntimeError:
  deterministic chapter audit is legacy-only;
  project chapters require model review
registry loaded = false
artifact written = false
```

等价入口检查：

- 正式 pipeline 的 initial 和 final 两处均统一调用 `requires_external_chapter_audit()`；
- isolated project 对 `initial`、`final` 都返回 true；
- deterministic 分支仅保留给 legacy `borrowed-heaven`；
- CLI `chapter-audit` 直接调用 model dispatch；
- CLI `chapter-audit-ingest` 进入 Schema、hash binding 和共享 evidence validator；
- repo 内未发现其他 deterministic audit 调用点。

证据：

- `system/runtime/nrl_production_runtime.py:2047-2052`
- `system/runtime/nrl_production_runtime.py:2642-2711`
- `system/runtime/nrl.py:1259-1267`

结论：project 无法通过 public CLI、正式 pipeline 或直接 helper 调用绕过模型审查。

## 4. 连带回归与 fail-closed 边界

复审确认：

- 所有 project chapter 的 initial/final 均要求模型审读。
- model dispatch 与 ingest 均检查 artifact kind、artifact hash、context hash。
- final audit 必须精确关闭所有既有 blocking/major issue，且自身不能保留 blocking/major issue。
- accept 重新验证 live prose authorization、hash-bound semantic context、final audit evidence 和 writer/observer/reviewer 执行身份。
- chapter-0067 不在七个 Volume 1 窗口中，无法获得项目授权。
- baseline 或双审查文件/hash 漂移时，authorization 与 readiness 均 fail closed。
- 旧的无 `authorization_contract_version=0.29`、无 current baseline binding 的 Borrowed Heaven 授权继续失效。
- 18 本书 × 12 个文学维度、216 个 signature dispositions、project semantic contracts 和 66 个 chapter semantic beats 的现有校验均通过。
- Volume 1 future dossier leak 检查继续通过。

未发现本轮修复放宽 stage transition、跨窗口授权、raw corpus 禁令、publish 禁令或 accepted chapter immutability。

## 5. Canonical baseline

当前 baseline：

```text
path = projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json
sha256 = af8fadce1b6d52c1c47f25a5d6f3437a056ee8c201d69625d1f50ab485cb09c4
version = 1.1
canonical input count = 98
missing inputs = 0
hash drift = 0
```

关键门禁实现已纳入 baseline：

```text
system/runtime/nrl_production_runtime.py
  3c3406634fefb30a1652c06197e0a0f4ad71593445435d5c44c6f1951d2cb174

system/production_runtime/schemas/continuity_audit.schema.json
  5fa5ec0f95afaabd0f76934e9e2910e130f605227175710d448aff0bdeb5b90b
```

baseline 自身记录位置：

- `projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json:5`
- runtime binding：同文件 `:87`
- audit Schema binding：同文件 `:99`

## 6. 验证结果

CLI：

```text
literary-semantic-validate = valid
profiles = 18
dimensions = 12
cross-book mechanisms = 16
protected signatures = 18

project-semantic-validate = valid
volumes = 15
history dossiers = 15
volume1 semantic beats = 66

project-production-validate = valid
chapters = 66
windows = 7
canonical inputs = 98

production-readiness exit code = 1
status = blocked_before_formal_prose
target = chapter-0001 / window 001-010
project content authorized = false
formal chapter registry count = 0
```

测试：

```text
tests.test_literary_semantic_integrity_v029
  18/18 passed

tests.test_production_chapter_runtime_v020
tests.test_hundred_crafts_production_readiness
tests.test_production_runtime_gate
  75/75 passed

python3 -m unittest discover -s tests -v
  362/362 passed

git diff --check
  passed
```

## 发布门禁说明

覆盖本报告会改变 Sol review 文件哈希。任何旧 `final-review-index` 或旧 Owner authorization 不得自动复用；后续必须重新绑定本 ACCEPT 报告与独立 Antigravity 报告的当前哈希，再由 Owner 单独授权具体 chapter/window。

在完成该重新绑定和显式 Owner 授权前，保持：

```text
owner_gate = active
content_authorized = false
generate_chapter_draft = blocked
bulk_prose = blocked
publish = blocked
```

该阻塞是预期的 fail-closed 发布状态，不是本次文学语义完整性缺陷。
