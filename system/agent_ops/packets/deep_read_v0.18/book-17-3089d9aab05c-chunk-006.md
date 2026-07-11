# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-006`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 7501479
- end_byte: 9001519
- chunk_sha256: `3db5c99255a60b7b13a741d61cf8f3ca034d60bb0f0cc1ef04d6d14f24189f68`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `80f370d4d94db458bb60e0848a53efbdb3d6c9ffc89e2d490f1f9e04a84b893a`
- sampled_evidence_headings: ["第二百七十一章 君只见独不见", "第二百七十七章 死结和理由", "第二百八十四章 风雪铁骑下江南（六）", "第二百九十章 中原和北凉", "第二百九十六章 灯火阑珊处，独坐城头人", "第三百零二章 西楚霸王（三）", "第三百零九章 野花", "第三百一十五章 收尸", "第三百二十一章 再见如初见", "第三百二十七章 秋风扶起春风", "第三百三十四章 秋天的阳光里", "第三百四十章 衮衮诸公，滚滚黄沙（六）", "第三百四十六章 不曾下雨", "第三百五十二章 有杀气", "第三百五十九章 姑娘好刀法", "第三百六十五章 立地成佛", "第三百七十一章 一气呵成", "第三百七十七章 天门洞开", "第三百八十四章 大戟横江", "第三百九十章 流州铁骑", "第三百九十六章 生气歌", "第四百零二章 快哉快哉", "第四百零九章 豪赌", "第四百一十五章 谪仙如雨落"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-006.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-006",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 7501479,
  "end_byte": 9001519,
  "chunk_sha256": "3db5c99255a60b7b13a741d61cf8f3ca034d60bb0f0cc1ef04d6d14f24189f68",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "80f370d4d94db458bb60e0848a53efbdb3d6c9ffc89e2d490f1f9e04a84b893a",
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
