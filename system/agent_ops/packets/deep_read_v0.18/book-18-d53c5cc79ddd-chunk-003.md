# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-003`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 3000282
- end_byte: 4500368
- chunk_sha256: `0632b1cad388419950dfd8119258a3d0918b6b95f37d3a5689d15be12d2d05ed`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `0632b1cad388419950dfd8119258a3d0918b6b95f37d3a5689d15be12d2d05ed`
- sampled_evidence_headings: ["第九十八节：一蹴而就蛊", "第一百零四节：真想扼杀掉", "第一百一十节：心慈之志", "第一百一十七节：必胜魔心", "第一百二十三节：竞争压力", "第一百二十九节：都是吃", "第一百三十五节：仙鹤门，方正", "第一百四十二节：何等的穷凶极恶！", "第一百四十八节：何等的奴道造诣！", "第一百五十四节：雷猪、岩鳄", "第一百六十节：拦截", "第一百六十六节：狐仙福地开启", "第一百七十三节：地灵——蛊仙之殇", "第一百七十九节：他死了", "第一百八十五节：狡诈鬼医，生死秘门", "第一百九十一节：魔无天", "第一百九十七节：白凝冰！", "第二百零四节：白凝冰，你演够了吗？", "第四节：执掌福地", "第十节：为了明天！", "第十六节：石人族大发展", "第二十三节：鬼脸葵海", "第二十九节：常山阴，做我的丈夫吧！", "第三十五节：十年风雪两茫茫"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-003.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-003",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 3000282,
  "end_byte": 4500368,
  "chunk_sha256": "0632b1cad388419950dfd8119258a3d0918b6b95f37d3a5689d15be12d2d05ed",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "0632b1cad388419950dfd8119258a3d0918b6b95f37d3a5689d15be12d2d05ed",
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
