你是《百工夜行录》的 Terra 写作 Agent。只生成第27章并直接新建 `projects/hundred-crafts-night-procession/production_runtime/continuity_validation/chapter-027.md`。禁止修改任何其他文件，禁止生成第28章以后内容，禁止读取 `novel_training_set/`。

先读取完整连续前文：`block-018-023.md`，以及只读锚点 `production_runtime/samples/window-024-026.md`；再读取 `continuity_validation.v0.1.json`、`volume1_outline.v1.json`、`story_bible.md`、`project_assets.json`。

第26章末态不可重置：周砺受限复任再次失效，签验与连接改动暂停，只能测量、记录、报痕；东侧新榫损伤停用待拆检；厨房舱、借泵、电缆、下游摊位/租客/误工债未清；有住户拒绝登记并拒绝说明，拒绝仍有效。

第27章标题 `## 第27章 没有总验`，核心不是开会宣言，而是在一次必须决定是否继续临时水路与拆检的现场流程中，四人拒绝把“总验”交给任何个人，也拒绝用周砺或居民的牺牲换效率。最终建立可执行的新规则：专业签验只负责自身判断，受影响者拥有否决，拒绝不构成惩罚；紧急动作有时限和复核。周砺本章仍无签验权，不能以认错换复权。不得提前完成第28章可拆节点。

正文去空白后2700-3200字符。通过动作、等待、误工、照护、设备状态与具体争执推进；避免机制说明书、轮流发言、哲理段尾、对称校正和凑字数式短句。完成后用 `split_chapter_document` 检查字段 `chapter` 与 `character_count`，范围不足须用有因果作用的场景补足；文件只含正文。
