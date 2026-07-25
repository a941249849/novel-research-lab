# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-04-bfe08b74de74-chunk-007`
- source_file: `novel_training_set/《仙逆》（校对版全本）作者：耳根.txt`
- source_file_sha256: `bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82`
- start_byte: 9000529
- end_byte: 10500604
- chunk_sha256: `ee9ecb5edef0a60920c3f96ace055f5d6e06c734132701a276c87899b1d4eb04`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `205e9d60293b522718649058a2f02db9096901daa4c78a90d038ff9eb7bb5745`
- sampled_evidence_headings: ["第1382章 故人", "第1391章 骗道", "第1401章 钓龙", "第1412章 九色归一！", "第1422章 封香火界！", "第1432章 情与恩", "第1442章 疗伤的契机！", "第1453章 寒目望天！", "第1462章 破坏规则", "第1472章 七星古神！！", "第1481章 今昔横云有雨", "第1491章 一声道友尽沧桑", "第1502章 猎幽冥（2）", "第1512章 金色铃铛", "第1522章 三道封印！", "第1532章 战老鬼", "第1542章 惊吓", "第1552章 你说什么？", "第1562章 召河", "第1572章 往如烟", "第1582章 阴月有晴", "第1593章 古庙夜雨归魂来", "第1603章 家在恒岳山下", "第1613章 梦醒！"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-04-bfe08b74de74-chunk-007.txt`

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
  "chunk_id": "book-04-bfe08b74de74-chunk-007",
  "source_file": "novel_training_set/《仙逆》（校对版全本）作者：耳根.txt",
  "source_file_sha256": "bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82",
  "start_byte": 9000529,
  "end_byte": 10500604,
  "chunk_sha256": "ee9ecb5edef0a60920c3f96ace055f5d6e06c734132701a276c87899b1d4eb04",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "205e9d60293b522718649058a2f02db9096901daa4c78a90d038ff9eb7bb5745",
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
