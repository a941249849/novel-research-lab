# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-011`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 15000739
- end_byte: 16500898
- chunk_sha256: `fff6dc5d87a95bb7648e28c7ffc4cc094828890e91ea89870a5a61d9f657386a`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `fff6dc5d87a95bb7648e28c7ffc4cc094828890e91ea89870a5a61d9f657386a`
- sampled_evidence_headings: ["第四百二十五节：青丝成空", "第四百三十二节：年蛊商战", "第四百三十九节：光照菌生意", "第四百四十六节：实力井喷", "第四百五十四节：万金妙华体", "第四百六十一节：一抹微笑", "第四百六十七节：香消玉殒：<!--80txt.com-ouoou-->", "第四百七十三节：盗天机缘？", "第四百七十九节：想输", "第四百八十六节：直接就动手", "第四百九十三节：落英馆", "第五百节：算计了人还要发难", "第五百零八节：房家八转", "第五百一十六节：方源至", "第五百二十三节：方源爱情", "第五百三十节：乐土传人", "第五百三十六节：位置暴露", "第五百四十三节：巅峰盛景", "第五百五十节：睡姑吐血", "第五百五十七节：方源动手", "第五百六十五节：牛魔花子", "第五百七十二节：云竹山脉", "第五百七十九节：宙道宗师", "第五百八十六节：俘虏"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-011.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-011",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 15000739,
  "end_byte": 16500898,
  "chunk_sha256": "fff6dc5d87a95bb7648e28c7ffc4cc094828890e91ea89870a5a61d9f657386a",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "fff6dc5d87a95bb7648e28c7ffc4cc094828890e91ea89870a5a61d9f657386a",
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
