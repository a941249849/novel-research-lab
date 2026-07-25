# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-03-0bc4648bf63c-chunk-001`
- source_file: `novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt`
- source_file_sha256: `0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e`
- start_byte: 0
- end_byte: 1500037
- chunk_sha256: `bd3fd1bef924fac92bbeb28f24290d6191775a80a446f698131d0f7cac38b42a`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `a8ff2f11c901652a53e83e8dbb6914608ab196234cd10a3ee31349bf0ccd0770`
- sampled_evidence_headings: ["第一卷 人间世", "第0010章 剑门魔墟", "第0019章 生死之间", "第0029章 雷中少女", "第0038章 阵杀炼气士", "第0048章 剑门蜃龙", "第0058章 有点儿疼", "第0067章 河边种人", "第0077章 大日无疆", "第0086章 狼狈与鬣狗", "第0096章 武道防御", "第0106章 剑斩美人头", "第0115章 大吹法螺", "第0125章 六翼金蜈", "第0135章 神魔宝藏", "第0144章 蛟龙真传", "第0154章 其心可诛", "第0163章 雷池", "第0173章 逆开五轮", "第0183章 忠奸莫辨", "第0192章 神兵金船", "第0202章 闭门思过", "第0211章 是非之地", "第0221章 祖血"]
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
For million-byte chunks, provide at least 16 major events, 10 character-state
transitions, 8 long-form mechanisms, 8 continuity observations, 6 style
observations, and 4 originality risks. Cite at least 6 exact chapter headings
from the bounded UTF-8 file when that many headings exist.
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
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "a8ff2f11c901652a53e83e8dbb6914608ab196234cd10a3ee31349bf0ccd0770",
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
