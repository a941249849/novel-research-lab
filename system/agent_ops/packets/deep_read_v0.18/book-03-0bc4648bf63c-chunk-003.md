# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-03-0bc4648bf63c-chunk-003`
- source_file: `novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt`
- source_file_sha256: `0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e`
- start_byte: 3000088
- end_byte: 4500239
- chunk_sha256: `7cc1dab134ebe5581db7a78f04e2b95d5747c778f424fabaf2d684927a47c5af`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `b6faa78988091e3251a34b1ce5fbc4ff84fa07e72b32f8278e9ae35b8c14ee75`
- sampled_evidence_headings: ["第0442章 河中的脸", "第0452章 险恶莫过人心", "第0461章 天雷地火一相逢", "第0471章 至宝之水", "第0480章 求道者", "第0490章 神话榜首", "第0500章 前往昆星", "第0509章 背叛", "第0519章 送伊远去", "第0528章 科技神树", "第0538章 狂狮百战，八极凶兵", "第0548章 问易", "第0557章 反祭天地", "第0567章 诡异爆发", "第0577章 飞龙在天", "第0586章 壮怀激烈", "第0596章 绝不会被绊住", "第0605章 祭鲲侯", "第0614章 走一路死一路", "第0624章 拧断脖子", "第0633章 伪造生死簿", "第0643章 祖庭表亲", "第0652章 幸不辱命", "第0662章 逃脱无门"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-03-0bc4648bf63c-chunk-003.txt`

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
  "chunk_id": "book-03-0bc4648bf63c-chunk-003",
  "source_file": "novel_training_set/《人道至尊》（校对版全本）作者：宅猪.txt",
  "source_file_sha256": "0bc4648bf63c6efbb17d3932d2642bbd81dac3d90c5ea424c89cdec7698cfc5e",
  "start_byte": 3000088,
  "end_byte": 4500239,
  "chunk_sha256": "7cc1dab134ebe5581db7a78f04e2b95d5747c778f424fabaf2d684927a47c5af",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "b6faa78988091e3251a34b1ce5fbc4ff84fa07e72b32f8278e9ae35b8c14ee75",
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
