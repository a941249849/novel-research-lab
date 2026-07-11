# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-16-9cbf8da97dac-chunk-007`
- source_file: `novel_training_set/《遮天》（精校版全本）作者：辰东.txt`
- source_file_sha256: `9cbf8da97daceb36fbd85edd84e2874a9ceac28252c18386fecf167d5a95660b`
- start_byte: 9000122
- end_byte: 10500181
- chunk_sha256: `93eed021930d8685893e047f0cea2dc0e847fa39e8533e45e3c7c7e5c2040466`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `08b20636ba03f0a6a6a18314d7f94bec3cba38b8d69bed7602ccd1fe5c46a461`
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-16-9cbf8da97dac-chunk-007.txt`

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
  "chunk_id": "book-16-9cbf8da97dac-chunk-007",
  "source_file": "novel_training_set/《遮天》（精校版全本）作者：辰东.txt",
  "source_file_sha256": "9cbf8da97daceb36fbd85edd84e2874a9ceac28252c18386fecf167d5a95660b",
  "start_byte": 9000122,
  "end_byte": 10500181,
  "chunk_sha256": "93eed021930d8685893e047f0cea2dc0e847fa39e8533e45e3c7c7e5c2040466",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "08b20636ba03f0a6a6a18314d7f94bec3cba38b8d69bed7602ccd1fe5c46a461",
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
