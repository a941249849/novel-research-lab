# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-010`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 13500564
- end_byte: 15000739
- chunk_sha256: `6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-010.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-010",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 13500564,
  "end_byte": 15000739,
  "chunk_sha256": "6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "6f7f96ef536d9ea556d3c463c156cecfbe5bb3c715e02ce64cd32e0ea02a2169",
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
