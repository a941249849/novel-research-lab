# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-013`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 18000904
- end_byte: 19500993
- chunk_sha256: `0aa8b981e80bc56ea0cf0f1c7355346fab459f90c46c9f6c41d9e780e85c32ab`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `0aa8b981e80bc56ea0cf0f1c7355346fab459f90c46c9f6c41d9e780e85c32ab`
- sampled_evidence_headings: ["第七百三十六节：杀仙夺财", "第七百四十二节：天庭来攻", "第七百四十八节：评估战果", "第七百五十四节：池曲由要说服自己", "第七百六十节：房家太上客卿长老", "第七百六十六节：参悟尊者真传", "第七百七十三节：怀疑重生", "第七百七十九节：蛊如故大阵", "第七百八十五节：你的性命，我取走了", "第七百九十一节：舆情汹涌", "第七百九十七节：恐怖兽潮", "第八百零三节：剑道宗师", "第八百零九节：红花眷属", "第八百一十六节：天庭察觉", "第八百二十二节：龙公招揽方源", "第八百二十八节：如此牺牲为那般", "第八百三十四节：新龙人之祖", "第八百四十节：参悟气墙", "第八百四十七节：八转蚁穴蛊", "第八百五十三节：各方进展", "第八百五十九节：天翻地覆", "第八百六十五节：天庭议事", "第八百七十一节：赤心行走榜新主", "第八百七十七节：一起来分析楚瀛"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-013.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-013",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 18000904,
  "end_byte": 19500993,
  "chunk_sha256": "0aa8b981e80bc56ea0cf0f1c7355346fab459f90c46c9f6c41d9e780e85c32ab",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "0aa8b981e80bc56ea0cf0f1c7355346fab459f90c46c9f6c41d9e780e85c32ab",
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
