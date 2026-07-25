# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-001`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 0
- end_byte: 1500707
- chunk_sha256: `a48d52198b6102ed06114d645885167963227085bd22340ec7140f79d162e8bd`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `6d0e52424e2dd73ae808fddb6344761c9c540b08a8305a8b7c70f69e9234ce33`
- sampled_evidence_headings: ["第一卷 白马出凉州", "第九章 雪中刀", "第十七章 说与山鬼听", "第二十六章 公主何苦为难公主", "第三十五章 半斤红妆", "第四十四章 读书用心所为何", "第五十二章 白马出凉州", "第六十一章 天师府上小天师（上）", "第七十章 还是打劫的", "第七十九章 右菩萨左金刚", "第八十七章 上山入城进宫（上）", "第九十六章 一脚踏黄龙", "第一百零五章 咫尺风雷（下）", "第一百一十四章 笔下游青蛇", "第一百二十二章 卸甲与狞笑", "第一百三十一章 上柱国老供奉", "第一百四十章 祸端", "第一百四十九章 亭前青衣", "第一百五十七章 亲家，出京，赚亏", "第一百六十六章 书生和砧板", "第一百七十五章 步步长生莲", "第一百八十四章 还了个放屁", "第一百九十二章 两座江湖", "第二百零一章 雷池和道理"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-001.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-001",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 0,
  "end_byte": 1500707,
  "chunk_sha256": "a48d52198b6102ed06114d645885167963227085bd22340ec7140f79d162e8bd",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "6d0e52424e2dd73ae808fddb6344761c9c540b08a8305a8b7c70f69e9234ce33",
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
