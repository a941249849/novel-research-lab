# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-001`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 0
- end_byte: 1500707
- chunk_sha256: `a48d52198b6102ed06114d645885167963227085bd22340ec7140f79d162e8bd`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `6d0e52424e2dd73ae808fddb6344761c9c540b08a8305a8b7c70f69e9234ce33`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-001.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-001",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 0,
  "end_byte": 1500707,
  "chunk_sha256": "a48d52198b6102ed06114d645885167963227085bd22340ec7140f79d162e8bd",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "6d0e52424e2dd73ae808fddb6344761c9c540b08a8305a8b7c70f69e9234ce33",
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
