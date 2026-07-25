# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-04-bfe08b74de74-chunk-010`
- source_file: `novel_training_set/《仙逆》（校对版全本）作者：耳根.txt`
- source_file_sha256: `bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82`
- start_byte: 13500699
- end_byte: 13547557
- chunk_sha256: `0fa467ffe1684441fd5bccbff6f63c2b69e6b7d814393ef7888daab27c18f854`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `0c4ce88439fb573d7f3f2c06a15a3fdbf7b22910e87148e20e52fb41ecba8e2f`
- sampled_evidence_headings: ["第2082章 惊变", "第2083章 踏入的资格", "第2084章 那女子，东梅", "第2085章 缺的一个", "第2086章 轮回就在那里", "第2087章 婉儿，醒来吧", "第2088章 蓦然回首"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-04-bfe08b74de74-chunk-010.txt`

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
  "chunk_id": "book-04-bfe08b74de74-chunk-010",
  "source_file": "novel_training_set/《仙逆》（校对版全本）作者：耳根.txt",
  "source_file_sha256": "bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82",
  "start_byte": 13500699,
  "end_byte": 13547557,
  "chunk_sha256": "0fa467ffe1684441fd5bccbff6f63c2b69e6b7d814393ef7888daab27c18f854",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "0c4ce88439fb573d7f3f2c06a15a3fdbf7b22910e87148e20e52fb41ecba8e2f",
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
