# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-12-7dd95a828fbe-chunk-001`
- source_file: `novel_training_set/《永生》（校对版全本）作者：梦入神机.txt`
- source_file_sha256: `7dd95a828fbe1e4b3c91e761bd3ca59eeef5230a893aa7e1358d316b247b545a`
- start_byte: 0
- end_byte: 1500125
- chunk_sha256: `d6453663569342a8417bb55e5ea3f0fbeb1043939234785bf1f6a9390f4eaa09`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `e95fe8efa3ba28afff0a84f92b056c59a960bf96e129b60a534aed1ada84783f`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-001.txt`

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
  "chunk_id": "book-12-7dd95a828fbe-chunk-001",
  "source_file": "novel_training_set/《永生》（校对版全本）作者：梦入神机.txt",
  "source_file_sha256": "7dd95a828fbe1e4b3c91e761bd3ca59eeef5230a893aa7e1358d316b247b545a",
  "start_byte": 0,
  "end_byte": 1500125,
  "chunk_sha256": "d6453663569342a8417bb55e5ea3f0fbeb1043939234785bf1f6a9390f4eaa09",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "e95fe8efa3ba28afff0a84f92b056c59a960bf96e129b60a534aed1ada84783f",
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
