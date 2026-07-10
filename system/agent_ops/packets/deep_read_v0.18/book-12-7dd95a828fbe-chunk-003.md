# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-12-7dd95a828fbe-chunk-003`
- source_file: `novel_training_set/《永生》（校对版全本）作者：梦入神机.txt`
- source_file_sha256: `7dd95a828fbe1e4b3c91e761bd3ca59eeef5230a893aa7e1358d316b247b545a`
- start_byte: 3000199
- end_byte: 4500313
- chunk_sha256: `6ae8bc60215ebe7bd7c35462e986af26479e384fe34215483d558cb5670bc95d`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-003.txt`

The bounded chunk file contains exactly the bytes identified above. Read that
entire bounded file before responding. Do not inspect or summarize a different
range and do not use pre-existing book reports as a substitute.

Return one JSON object only with these binding fields and an `analysis` object.
The analysis must contain non-empty arrays named `major_events`,
`character_state_transitions`, `long_form_mechanisms`,
`continuity_observations`, `style_observations`, and `originality_risks`;
`chapter_span` as an array; and `creation_family_evidence` as a non-empty object.
Use chapter titles or abstract event labels as evidence anchors, never raw prose.
The job_id is `job-v018-verifiable-deep-reading` and contract_version is `0.18`. Copy every
binding field exactly from this template and replace only the analysis values:

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "chunk_id": "book-12-7dd95a828fbe-chunk-003",
  "source_file": "novel_training_set/《永生》（校对版全本）作者：梦入神机.txt",
  "source_file_sha256": "7dd95a828fbe1e4b3c91e761bd3ca59eeef5230a893aa7e1358d316b247b545a",
  "start_byte": 3000199,
  "end_byte": 4500313,
  "chunk_sha256": "6ae8bc60215ebe7bd7c35462e986af26479e384fe34215483d558cb5670bc95d",
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
