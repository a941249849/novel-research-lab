# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-010`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 13500564
- end_byte: 15000739
- chunk_sha256: `6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169`
- sampled_evidence_headings: ["第二百七十五节：东海交易会", "第二百八十二节：卜卦龟变化", "第二百八十八节：无赖！可耻！", "第二百九十四节：收购神鹿果", "第三百节：请你“赏析”", "第三百零七节：给池伤的挑战信", "第三百一十三节：掠影", "第三百二十节：死鬼快来铁面神", "第三百二十七节：柴家有人烟", "第三百三十三节：菟舔", "第三百四十节：方源绝境", "第三百四十六节：龙公苏醒", "第三百五十二节：紫陨（下）", "第三百五十八节：武庸追击", "第三百六十五节：方源的判断", "第三百七十一节：一曲离歌退武庸！", "第三百七十八节：千变老祖", "第三百八十五节：燃魂爆运！", "第三百九十一节：青爪鬼翼狮", "第三百九十八节：暗算成功！", "第四百零四节：再炼净魂仙蛊", "第四百一十节：入河", "第四百一十七节：回来", "第四百二十四节：净魂终成！"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-010.txt`

The bounded chunk file contains exactly the bytes identified above. Read that
entire bounded file before responding. Do not inspect or summarize a different
range and do not use pre-existing book reports as a substitute.

Return one JSON object only with these binding fields and an `analysis` object.
The analysis must contain non-empty arrays named `major_events`,
`character_state_transitions`, `long_form_mechanisms`,
`continuity_observations`, `style_observations`, and `originality_risks`;
`chapter_span` as an array; and `creation_family_evidence` as a non-empty object.
Use chapter titles or abstract event labels as evidence anchors, never raw prose.
For million-byte chunks, provide at least 16 major events, 10 character-state
transitions, 8 long-form mechanisms, 8 continuity observations, 6 style
observations, and 4 originality risks. Cite at least 8 exact chapter headings
from the bounded UTF-8 file when that many headings exist.
The job_id is `job-v018-verifiable-deep-reading` and contract_version is `0.18`. Copy every
binding field exactly from this template and replace only the analysis values:

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "chunk_id": "book-18-d53c5cc79ddd-chunk-010",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 13500564,
  "end_byte": 15000739,
  "chunk_sha256": "6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169",
  "analysis": {
    "chapter_span": [],
    "major_events": [],
    "character_state_transitions": [],
    "long_form_mechanisms": [],
    "continuity_observations": [],
    "style_observations": [],
    "creation_family_evidence": {},
    "originality_risks": []
  }
}
```
