# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-04-bfe08b74de74-chunk-004`
- source_file: `novel_training_set/《仙逆》（校对版全本）作者：耳根.txt`
- source_file_sha256: `bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82`
- start_byte: 4500288
- end_byte: 6000336
- chunk_sha256: `ff5a866f8079c4bf31cb138b7c560ca6db676d2c001650677586de8fc7daa4d2`
- source_encoding: `gb18030`
- bounded_chunk_utf8_sha256: `b6be9bc881e7e07bc3cf3e83a5b92861b43666e4d9bdf758ec3494fb8c883d8c`
- sampled_evidence_headings: ["第683章 惊退千葵子", "第693章 青宜", "第704章 一世轮回，结束……", "第714章 望月苏醒", "第724章 看到了第三步！", "第734章 占了大便宜", "第744章 剑尖", "第755章 惊变", "第765章 血星", "第776章 千丈禁地，入者死！", "第786章 “谁，也不能离去！”", "第796章 师兄？", "第807章 传送小阵", "第817章 避天棺（1）", "第827章 姚冰云", "第838章 冰云", "第848章 姚冰云的道", "第858章 目标，一百零八仙", "第868章 不合格（2）", "第878章 第三目", "第八卷 联盟隐秘", "第898章 雷吉", "第909章 给你一场奇迹", "第919章 周天（2）"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-04-bfe08b74de74-chunk-004.txt`

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
  "chunk_id": "book-04-bfe08b74de74-chunk-004",
  "source_file": "novel_training_set/《仙逆》（校对版全本）作者：耳根.txt",
  "source_file_sha256": "bfe08b74de74bea1f5979eadb2e98f8a699473d565974582cf6629583278bc82",
  "start_byte": 4500288,
  "end_byte": 6000336,
  "chunk_sha256": "ff5a866f8079c4bf31cb138b7c560ca6db676d2c001650677586de8fc7daa4d2",
  "source_encoding": "gb18030",
  "bounded_chunk_utf8_sha256": "b6be9bc881e7e07bc3cf3e83a5b92861b43666e4d9bdf758ec3494fb8c883d8c",
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
