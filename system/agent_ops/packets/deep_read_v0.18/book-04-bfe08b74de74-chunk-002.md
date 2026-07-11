# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-04-bfe08b74de74-chunk-002`
- source_file: `novel_training_set/《仙逆》（校对版全本）作者：耳根.txt`
- source_file_sha256: `bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82`
- start_byte: 1500136
- end_byte: 3000188
- chunk_sha256: `eb5b6e80d1a6fa00059ee3b40a1d09c2114d763969524c33586e51c57840f20f`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `bc641a4f107eaba6ad9495e7aae60c9a8d6c617d527c9d7f9f25df2c466f5eb7`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-04-bfe08b74de74-chunk-002.txt`

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
  "chunk_id": "book-04-bfe08b74de74-chunk-002",
  "source_file": "novel_training_set/《仙逆》（校对版全本）作者：耳根.txt",
  "source_file_sha256": "bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82",
  "start_byte": 1500136,
  "end_byte": 3000188,
  "chunk_sha256": "eb5b6e80d1a6fa00059ee3b40a1d09c2114d763969524c33586e51c57840f20f",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "bc641a4f107eaba6ad9495e7aae60c9a8d6c617d527c9d7f9f25df2c466f5eb7",
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
