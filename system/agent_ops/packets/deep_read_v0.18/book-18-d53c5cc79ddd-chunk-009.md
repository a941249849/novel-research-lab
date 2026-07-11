# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-009`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 12000510
- end_byte: 13500564
- chunk_sha256: `4b262214fd33f2ab2d401a466e4dfa31c4fa222518936a030d48e39384abbd43`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `4b262214fd33f2ab2d401a466e4dfa31c4fa222518936a030d48e39384abbd43`
- sampled_evidence_headings: ["第一百二十七节：暂时的休整", "第一百三十四节：夺蚌", "第一百四十节：试用道可道仙蛊", "第一百四十七节：电炼马鸿运", "第一百五十四节：不在乎", "第一百六十节：风云突变利益心", "第一百六十六节：方源的修行契机", "第一百七十三节：不跪", "第一百七十九节：仙蛊龙息", "第一百八十六节：干点坏事", "第一百九十二节：仙缘生意", "第一百九十九节：登场南疆", "第二百零六节：龙人", "第二百一十三节：中洲蛊仙集结", "第二百二十节：境界之妙", "第二百二十七节：水道宗师", "第二百三十三节：自找死路", "第二百四十节：引魂入梦", "第二百四十六节：我爱他！", "第二百五十二节：什么东西？", "第二百五十七节：马赵相会", "第二百六十三节：逆流河太古秘辛：<!--80txt.com-ouoou-->", "第二百六十九节：逆流护身印", "第二百七十四节：楚瀛再现"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-009.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-009",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 12000510,
  "end_byte": 13500564,
  "chunk_sha256": "4b262214fd33f2ab2d401a466e4dfa31c4fa222518936a030d48e39384abbd43",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "4b262214fd33f2ab2d401a466e4dfa31c4fa222518936a030d48e39384abbd43",
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
