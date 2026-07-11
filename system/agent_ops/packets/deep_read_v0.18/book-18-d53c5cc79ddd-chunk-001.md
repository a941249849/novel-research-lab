# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `book-18-d53c5cc79ddd-chunk-001`
- source_file: `novel_training_set/蛊真人.txt`
- source_file_sha256: `d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88`
- start_byte: 0
- end_byte: 1500213
- chunk_sha256: `0cb5f65ce9d3575639a47ee98185f92a8c6656e9ace1a893735b431b743429ec`
- source_encoding: `utf-8`
- bounded_chunk_utf8_sha256: `0cb5f65ce9d3575639a47ee98185f92a8c6656e9ace1a893735b431b743429ec`
- sampled_evidence_headings: ["第一卷 ：魔性不改", "第七节：蛊师有九转，花酒留遗藏", "第十三节：月下竹林，一点珠雪", "第二十节：学堂家老无语了", "第二十七节：公然勒索", "第三十三节：你骂吧", "第四十节：紫金石中蟾蛊眠", "第四十七节：贾金生，其实我不想杀你的", "第五十四节：我可是班头啊！", "第六十节：影灭壁破现甬道，魔道传承岂易", "第六十七节：你放心，我会饶了你们的", "第七十四节：智窥迷雾现杀机", "第八十节：战力大涨", "第八十七节：态度就是心的面具", "第九十四节：忽然收力", "第一百节：白玉蛊", "第一百零七节：熟能生巧掂元石，酒肆当中恶客来", "第一百一十四节：洞中有猴王", "第一百二十一节：四味酒虫", "第一百二十七节：所谓的道德和感情（大章 ）", "第一百三十四节：追杀", "第一百四十二节：古月青书VS白凝冰（下）", "第一百四十八节：局面（第一更）", "第一百五十五节：借"]
- bounded_chunk_file: `.nrl-work/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-001.txt`

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
  "chunk_id": "book-18-d53c5cc79ddd-chunk-001",
  "source_file": "novel_training_set/蛊真人.txt",
  "source_file_sha256": "d53c5cc79ddd02c45ad8e6ad334a3f8feac558c67726486d9f41417cfd718d88",
  "start_byte": 0,
  "end_byte": 1500213,
  "chunk_sha256": "0cb5f65ce9d3575639a47ee98185f92a8c6656e9ace1a893735b431b743429ec",
  "source_encoding": "utf-8",
  "bounded_chunk_utf8_sha256": "0cb5f65ce9d3575639a47ee98185f92a8c6656e9ace1a893735b431b743429ec",
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
