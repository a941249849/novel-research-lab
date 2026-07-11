# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-008`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 10500505
- end_byte: 12000510
- chunk_sha256: `73007111a63f89ec7fcd88ccc5d995be866958fdef1e389387ddb99a071a7562`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `73007111a63f89ec7fcd88ccc5d995be866958fdef1e389387ddb99a071a7562`
- sampled_evidence_headings: ["第三百六十一节：巨手！", "第三百六十七节：幕幕往昔", "第一节：一切都是天意", "第七节：九五至尊仙窍（下）", "第十二节：如今迈步从头越", "第十九节：方源vs戚灾", "第二十四节：是机缘还是麻烦？", "第三十节：三道无上真传", "第三十六节：方源渡劫（结）", "第四十二节：变化道！", "第四十八节：天庭！", "第五十四节：话本平常蛇龙变", "第六十一节：贵精不贵多?", "第六十七节：猴获功成", "第七十三节：天大地大我最大", "第七十八节：变化道宗师！：<!--80txt.com-ouoou-->", "第八十四节：黑家大战（上）", "第八十九节：八转蛊仙岂容算", "第九十五节：一颗死蛋", "第一百零二节：此蛊何名？", "第一百零七节：黑凡四珍（上）", "第一百一十三节：对战落星犬", "第一百二十节：不听不信", "第一百二十六节：策反楚度？"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-008.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-008",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 10500505,
  "end_byte": 12000510,
  "chunk_sha256": "73007111a63f89ec7fcd88ccc5d995be866958fdef1e389387ddb99a071a7562",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "73007111a63f89ec7fcd88ccc5d995be866958fdef1e389387ddb99a071a7562",
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
