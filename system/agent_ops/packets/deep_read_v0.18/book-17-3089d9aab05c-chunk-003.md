# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-003`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 3000736
- end_byte: 4500743
- chunk_sha256: `75e95fdb582df27c0eba18806bfe1b25bf78d6ec1bec5a7eea65ad22002d46cf`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-003.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-003",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 3000736,
  "end_byte": 4500743,
  "chunk_sha256": "75e95fdb582df27c0eba18806bfe1b25bf78d6ec1bec5a7eea65ad22002d46cf",
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
