# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-002`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 1500213
- end_byte: 3000282
- chunk_sha256: `38705d7dab34a28227616a927e001784c80eefc82085d5eb942dce6d98d614cf`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `38705d7dab34a28227616a927e001784c80eefc82085d5eb942dce6d98d614cf`
- sampled_evidence_headings: ["第一百五十六节：照影秘方，花酒迷离", "第一百六十三节：雷冠头狼", "第一百七十节：铁面无私血可冷？", "第一百七十六节：牺牲的觉悟", "第一百八十二节：血湖墓地", "第一百八十七节：时间长河唯一条，春秋蝉做舟来渡", "第一百九十三节：神捕后手", "第一百九十七节：改命！", "第一节：黄龙江上竹筏倾", "第六节：夜宿树冠", "第十节：遭遇魔道蛊师", "第十七节：青铜舍利蛊", "第二十三节：白骨传承（上）", "第三十节：村庄休整（第二更）", "第三十七节：好人会有好报？", "第四十三节：聪明人的默契", "第五十节：滴水之恩，当涌泉相报！", "第五十六节：丁浩，你给我出来！", "第六十三节：卖不出去", "第七十节：家宴", "第七十七节：星辰石", "第八十三节：灵光一闪蛊", "第九十节：不能阻挡我", "第九十七节：拍卖会"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-002.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-002",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 1500213,
  "end_byte": 3000282,
  "chunk_sha256": "38705d7dab34a28227616a927e001784c80eefc82085d5eb942dce6d98d614cf",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "38705d7dab34a28227616a927e001784c80eefc82085d5eb942dce6d98d614cf",
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
