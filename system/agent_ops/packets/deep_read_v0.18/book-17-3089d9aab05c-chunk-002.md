# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-002`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 1500707
- end_byte: 3000736
- chunk_sha256: `30926365d7e13f31f64087101661084bebfc9bd157e3ab93e753d22c0150b30b`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `648bc070b81c8440142bea572823ed35418fb4d1abde01049ed6aa76be00760b`
- sampled_evidence_headings: ["第二百零二章 东游西归", "第二百一十章 说书人酌酒闭目而谈", "第六章 最坏的最好的江湖", "第十四章 一样米养江湖百样人", "第二十二章 没有你们的天下十人", "第二十九章 烧纸不易死人易", "第三十七章 跪不跪", "第四十五章 好鸟", "第五十三章 你是佛陀，我入金刚", "第五十九章 下马", "第六十七章 聚散", "第七十五章 大雨撑小伞，指玄对金刚", "第八十二章 揽雀收覆水", "第九十章 山中相厌城外相欢", "第九十八章 猩红叠猩红", "第一百零五章 女子种桂", "第一百一十三章 钓起一湖", "第一百二十一章 弹剑如弹琴", "第一百二十九章 师父和草鞋", "第一百三十六章 南归，过河，拽山", "第一百四十三章 刀归鞘刀出鞘", "第一百五十一章 小娘不知羞", "第一百五十八章 北凉饮尽两杯绿蚁酒", "第一百六十六章 风起凤飞，柳环卖花声"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-002.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-002",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 1500707,
  "end_byte": 3000736,
  "chunk_sha256": "30926365d7e13f31f64087101661084bebfc9bd157e3ab93e753d22c0150b30b",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "648bc070b81c8440142bea572823ed35418fb4d1abde01049ed6aa76be00760b",
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
