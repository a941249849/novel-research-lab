# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-004`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 4500368
- end_byte: 6000481
- chunk_sha256: `1b994e235166f26fabbfd4ec15231edb4b5950900ce208bbd6149bb2e11bf2e1`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `1b994e235166f26fabbfd4ec15231edb4b5950900ce208bbd6149bb2e11bf2e1`
- sampled_evidence_headings: ["第三十六节：洪福齐天马鸿运", "第四十二节：蛛丝马迹蛊", "第四十八节：激战（中）", "第五十五节：古往炼道第一仙", "第六十一节：没有什么不能出卖的", "第六十七节：奴道之威!", "第七十三节：中流砥柱", "第七十九节：影响", "第八十五节：第二空窍！", "第九十二节：墨狮狂", "第九十八节：东方余亮", "第一百零三节：先挑狼王", "第一百零九节：狼王的狠辣", "第一百一十三节：扬名", "第一百二十节：风云急变少猛将", "第一百二十七节：大战（中）", "第一百三十三节：挑将", "第一百三十九节 陷害蛊仙？", "第一百四十五节 诗仙陨落星鹫峰", "第一百五十一节：竟是蛊仙传承！", "第一百五十七节：贪生怕死因由何？", "第一百六十四节：六臂天尸王", "第一百七十节 再探真阳楼", "第一百七十六节：升六角，难找试蛊之人"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-004.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-004",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 4500368,
  "end_byte": 6000481,
  "chunk_sha256": "1b994e235166f26fabbfd4ec15231edb4b5950900ce208bbd6149bb2e11bf2e1",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "1b994e235166f26fabbfd4ec15231edb4b5950900ce208bbd6149bb2e11bf2e1",
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
