# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-04-bfe08b74de74-chunk-005`
- source_file: `novel_training_set/《仙逆》（校对版全本）作者：耳根.txt`
- source_file_sha256: `bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82`
- start_byte: 6000336
- end_byte: 7500405
- chunk_sha256: `57944e8a9d2628f6cedee5d6985db141f8844f0c5f297c506162a6e0efdd1050`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `aed075c9043b77c052e66a0e9554b1d60d1ad410c0acc4edbc30f2e0794df09a`
- sampled_evidence_headings: ["第920章 周天（3）", "第930章 联盟长老团", "第940章 四星王族古神", "第950章 杀域界", "第960章 初窥本源", "第970章 破指", "第981章 可还记得灵儿", "第991章 重逢（1）", "第1001章 第二分身（上）", "第1011章 仙灵天境", "第1021章 朱雀觉醒", "第1031章 枯符", "第1041章 深坑之下", "第1051章 周佚再现", "第1061章 苏醒", "第1071章 来临", "第1081章 梦回远古", "第1091章 三世火元之威", "第1102章 你们找死！", "第1112章 雨界呼救", "第1122章 周茹", "第1132章 无极子", "第1141章 吕烟菲", "第1151章 来的好快！"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-04-bfe08b74de74-chunk-005.txt`

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
  "chunk_id": "book-04-bfe08b74de74-chunk-005",
  "source_file": "novel_training_set/《仙逆》（校对版全本）作者：耳根.txt",
  "source_file_sha256": "bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82",
  "start_byte": 6000336,
  "end_byte": 7500405,
  "chunk_sha256": "57944e8a9d2628f6cedee5d6985db141f8844f0c5f297c506162a6e0efdd1050",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "aed075c9043b77c052e66a0e9554b1d60d1ad410c0acc4edbc30f2e0794df09a",
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
