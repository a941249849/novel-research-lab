# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-012`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 16500898
- end_byte: 18000904
- chunk_sha256: `313cf544b54d287224fb9bde34ca83504ee5e31895de3dc689ebfc6dc238223e`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `313cf544b54d287224fb9bde34ca83504ee5e31895de3dc689ebfc6dc238223e`
- sampled_evidence_headings: ["第五百八十七节：囚禁人质", "第五百九十三节：紫薇的不安", "第六百节：你信命吗？", "第六百零六节：这是陷阱！", "第六百一十四节：阳莽背火衣", "第六百二十节：他作弊！", "第六百二十六节：洞天易主", "第六百三十三节：楚瀛身亡", "第六百三十九节：方源被救", "第六百四十六节：方源，你是好人", "第六百五十二节：我拒绝", "第六百五十七节：悔蛊异变", "第六百六十四节：进展", "第六百七十节：怪兽肆虐", "第六百七十六节：紫薇借蛊", "第六百八十四节：三人成虎", "第六百九十节：南仙众志", "第六百九十七节：尊者对决", "第七百零三节：阵中亡", "第七百零九节：四大龙将", "第七百一十六节：劫运坛反击", "第七百二十二节：元始天庭！", "第七百二十九节：陆畏因叛变", "第七百三十五节：我心里有数"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-012.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-012",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 16500898,
  "end_byte": 18000904,
  "chunk_sha256": "313cf544b54d287224fb9bde34ca83504ee5e31895de3dc689ebfc6dc238223e",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "313cf544b54d287224fb9bde34ca83504ee5e31895de3dc689ebfc6dc238223e",
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
