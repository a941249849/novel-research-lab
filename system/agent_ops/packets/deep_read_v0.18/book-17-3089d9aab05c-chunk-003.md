# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-003`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 3000736
- end_byte: 4500743
- chunk_sha256: `75e95fdb582df27c0eba18806bfe1b25bf78d6ec1bec5a7eea65ad22002d46cf`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `c6c1cb404cb3e12f3251f8c7d02ad0c1eb50f92da6ca349d8d145989f6e58e03`
- sampled_evidence_headings: ["第一百六十七章 亭中三言两语定江湖", "第一章 倒酒七十一颗", "第八章 问剑答剑", "第十六章 一人想赠剑春秋，一人折剑出江湖", "第二十三章 桌上皇帝两字", "第三十一章 真武见我", "第三十八章 我以黑剑杀白雪", "第四十六章 过河卒子", "第五十三章 魔高一丈", "第六十一章 晚来天欲雪", "第六十八章 守不住寡的江湖", "第七十六章 雨伞", "第八十三章 最后一趟江湖", "第九十一章 事未了拂衣去", "第九十八章 灯笼", "第一百零六章 姓徐的", "第一百一十三章 骤然富贵", "第一百二十一章 开门不见山", "第一百二十八章 与人言一二三", "第一百三十六章 北上南下", "第一百四十三章 帝王相逢风雪中", "第一百五十一章 你方唱罢", "第一百五十八章 北凉要跟北莽离阳讲道理", "第一百六十六章 回望和回神"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-003.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-003",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 3000736,
  "end_byte": 4500743,
  "chunk_sha256": "75e95fdb582df27c0eba18806bfe1b25bf78d6ec1bec5a7eea65ad22002d46cf",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "c6c1cb404cb3e12f3251f8c7d02ad0c1eb50f92da6ca349d8d145989f6e58e03",
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
