# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-03-0bc4648bf63c-chunk-001`
- source_file: `novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt`
- source_file_sha256: `0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e`
- start_byte: 0
- end_byte: 1500037
- chunk_sha256: `bd3fd1bef924fac92bbeb28f24290d6191775a80a446f698131d0f7cac38b42a`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-03-0bc4648bf63c-chunk-001.txt`

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
  "chunk_id": "book-03-0bc4648bf63c-chunk-001",
  "source_file": "novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt",
  "source_file_sha256": "0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e",
  "start_byte": 0,
  "end_byte": 1500037,
  "chunk_sha256": "bd3fd1bef924fac92bbeb28f24290d6191775a80a446f698131d0f7cac38b42a",
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
