# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-014`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 19500993
- end_byte: 19898596
- chunk_sha256: `2a85acdb4b842a8030086dabd48a1e162b86bd21f7302cff2f438177cf8faf33`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `2a85acdb4b842a8030086dabd48a1e162b86bd21f7302cff2f438177cf8faf33`
- sampled_evidence_headings: ["第八百七十八节：再救夏琳", "第八百八十节：中型任务", "第八百八十一节：一下就打死", "第八百八十三节：积土为山", "第八百八十四节：大型任务", "第八百八十五节：老好人", "第八百八十七节：欺负八转", "第八百八十九节：领土蛊", "第八百九十一节：竟是方源！", "第八百九十二节：人道准无上", "第八百九十四节：沈从声的仙材", "第八百九十六节：功德倒扣", "第八百九十七节：大炼仙蛊", "第八百九十九节：超级任务", "第九百零一节：终极任务", "第九百零二节：认我作爹", "第九百零四节：仙蛊应运", "第九百零六节：烽火四起", "第九百零八节：白日星现", "第九百零九节：肉鞭仙", "第九百一十一节：北原反击", "第九百一十三节：方源出手", "第九百一十四节：孽龙脱困", "第九百一十六节：沈伤的破解"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-014.txt`

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
observations, and 4 originality risks. Cite at least 6 exact chapter headings
from the bounded UTF-8 file when that many headings exist.
The job_id is `job-v018-verifiable-deep-reading` and contract_version is `0.18`. Copy every
binding field exactly from this template and replace only the analysis values:

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "chunk_id": "book-18-d53c5cc79ddd-chunk-014",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 19500993,
  "end_byte": 19898596,
  "chunk_sha256": "2a85acdb4b842a8030086dabd48a1e162b86bd21f7302cff2f438177cf8faf33",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "2a85acdb4b842a8030086dabd48a1e162b86bd21f7302cff2f438177cf8faf33",
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
