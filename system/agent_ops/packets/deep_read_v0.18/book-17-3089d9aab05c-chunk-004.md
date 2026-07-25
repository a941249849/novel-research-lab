# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-004`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 4500743
- end_byte: 6000818
- chunk_sha256: `504a39c675f4185bbb6feb32fcf421f5d6152cda47f93e128d5019e7037358c5`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `ae0af7908a9ca8776ed34dc49e50861660c4f3c94aa5291274080a7e295b75a7`
- sampled_evidence_headings: ["第一百六十七章 跟天下百姓要了一壶酒", "第四卷 共逐鹿", "第七章 真像", "第十四章 高树露的体魄", "第二十一章 道士下山挑山", "第二十八章 春秋之尾，草席之旁", "第三十五章 十分之争，将死之人", "第四十二章 一张帘子一字请", "第四十九章 武林新木", "第五十六章 秋愁煞人更杀人", "第六十三章 得道", "第七十章 不外乎人情", "第七十六章 井中月", "第八十三章 霜杀百草（一）", "第九十章 青灯", "第九十七章 为他人作嫁衣裳", "第一百零四章 旧账", "第一百一十一章 天无雪", "第一百一十八章 离阳失其鹿（下）", "第一百二十五章 仙人落子", "第一百三十二章 八方雷动", "第一百三十九章 天下动静（上）", "第一百四十六章 山中无虎", "第一百五十三章 死在更南，死于更北"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-004.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-004",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 4500743,
  "end_byte": 6000818,
  "chunk_sha256": "504a39c675f4185bbb6feb32fcf421f5d6152cda47f93e128d5019e7037358c5",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "ae0af7908a9ca8776ed34dc49e50861660c4f3c94aa5291274080a7e295b75a7",
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
