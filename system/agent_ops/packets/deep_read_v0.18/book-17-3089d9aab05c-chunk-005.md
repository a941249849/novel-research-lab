# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-17-3089d9aab05c-chunk-005`
- source_file: `novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt`
- source_file_sha256: `3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1`
- start_byte: 6000818
- end_byte: 7501479
- chunk_sha256: `c2069bb870178b7fd741b04384c89eb58d713122c5ee197d76362156c2825da5`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `4bcbbfb60f87051d27849f18e8252a7efee15a74543b81c719ac061dfff0e885`
- sampled_evidence_headings: ["第一百五十四章 草蛇灰线", "第一百五十九章 就在那里！", "第一百六十四章 骨灰", "第一百六十九章 珠帘，铁甲（中）", "第一百七十四章 今年清明无苦雨", "第一百七十九章 想不想坐那张椅子", "第一百八十四章 两人之战，两国之战（三）", "第一百八十九章 两人之战，两国之战（八）", "第一百九十四章 一桩买卖", "第一百九十九章 六两三", "第二百零四章 南北共分天下", "第二百零九章 我从山中来，山风翻我书", "第二百一十五章 于无声处听惊雷", "第二百二十章 北凉四战（二）", "第二百二十五章 北凉四战（七）", "第二百三十章 痛痛快快", "第二百三十五章 百无一用是（三）", "第二百四十章 噤若寒蝉（三）", "第二百四十五章 噤若寒蝉（八）", "第二百五十章 一位位仙人在前", "第二百五十五章 大胆吕洞玄", "第二百六十章 事了拂衣（三）", "第二百六十五章 侠客行（一）", "第二百七十章 楼外日头正暖"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-17-3089d9aab05c-chunk-005.txt`

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
  "chunk_id": "book-17-3089d9aab05c-chunk-005",
  "source_file": "novel_training_set/《雪中悍刀行》（校对版全本）作者：烽火戏诸侯.txt",
  "source_file_sha256": "3089d9aab05c39e0192a229c41164ecc1b25ef830f29b2d6edfcfdf8dab216c1",
  "start_byte": 6000818,
  "end_byte": 7501479,
  "chunk_sha256": "c2069bb870178b7fd741b04384c89eb58d713122c5ee197d76362156c2825da5",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "4bcbbfb60f87051d27849f18e8252a7efee15a74543b81c719ac061dfff0e885",
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
