# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-03-0bc4648bf63c-chunk-002`
- source_file: `novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt`
- source_file_sha256: `0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e`
- start_byte: 1500037
- end_byte: 3000088
- chunk_sha256: `afcd0971e2ad1ecc7b617cc19ac8e42c7310d3519e915dec083a8f9a6df97ad9`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `22ded40fa91b89a288c1fc2edc0ae9db38b3f01c016a88e7afa0bfb100e2c663`
- sampled_evidence_headings: ["第0222章 只拔一毛", "第0232章 月色真美", "第0241章 蜕变", "第0251章 布阵", "第0260章 夺日", "第0270章 肉身成神", "第0279章 三绝阵", "第0289章 文无第一武无第二", "第0299章 元神不死", "第0308章 大赢家", "第0318章 魂归来兮", "第0327章 性命双修", "第0337章 大日天魔真经", "第0346章 摩罗波旬", "第0356章 初次交锋", "第0365章 刑天", "第0374章 无路可退", "第0384章 双岳合璧", "第0393章 破局之战", "第0403章 冰封古城", "第0412章 变化玄功", "第0422章 钟祸祸下山", "第0431章 单挑", "第0441章 神异果"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-03-0bc4648bf63c-chunk-002.txt`

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
  "chunk_id": "book-03-0bc4648bf63c-chunk-002",
  "source_file": "novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt",
  "source_file_sha256": "0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e",
  "start_byte": 1500037,
  "end_byte": 3000088,
  "chunk_sha256": "afcd0971e2ad1ecc7b617cc19ac8e42c7310d3519e915dec083a8f9a6df97ad9",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "22ded40fa91b89a288c1fc2edc0ae9db38b3f01c016a88e7afa0bfb100e2c663",
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
