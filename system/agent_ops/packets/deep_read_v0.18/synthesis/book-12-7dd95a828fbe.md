# NRL Antigravity Per-Book Synthesis v0.18

Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.
Do not use pre-existing short reports and do not quote source prose.

- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-001.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-002.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-003.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-004.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-005.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-006.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-007.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-12-7dd95a828fbe-chunk-008.json`

Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.
All synthesis arrays and all nine creation-family keys must be non-empty.
Add evidence_map entries with claim, chunk_id, and exact chapter_heading for every synthesis family.

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "book_id": "book-12-7dd95a828fbe",
  "book_title": "《永生》（校对版全本）作者：梦入神机",
  "covered_chunk_ids": [
    "book-12-7dd95a828fbe-chunk-001",
    "book-12-7dd95a828fbe-chunk-002",
    "book-12-7dd95a828fbe-chunk-003",
    "book-12-7dd95a828fbe-chunk-004",
    "book-12-7dd95a828fbe-chunk-005",
    "book-12-7dd95a828fbe-chunk-006",
    "book-12-7dd95a828fbe-chunk-007",
    "book-12-7dd95a828fbe-chunk-008"
  ],
  "covered_chunk_hashes": [
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-001",
      "response_sha256": "a20805bc36b45cbde2da2090080519339a0d8ac780a61effe81610c0a2192580"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-002",
      "response_sha256": "672c20b93b9f61593743980352c7d44bcb3e7bf1575eef35ee427273eaa358f8"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-003",
      "response_sha256": "d44a0448762db1de0fdac5594d0b7dfe4abcf70d5256c5540a51a7964d406c52"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-004",
      "response_sha256": "22e07f59cb47f9300e928fc95149eccab52a99c0ae8c431a9cc6a7bffc248522"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-005",
      "response_sha256": "de22e0abffe85625fd120c35876074dca2922b4955387baa7d9cd91d266711f8"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-006",
      "response_sha256": "2dbca005ad0de7671e281db28d81cd730e254b1fe57d4061e322357dc5f3c9bf"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-007",
      "response_sha256": "59840651b6353a7f1b071909eba8f75d995d8e87b6c177b8c6c4cf493022bb44"
    },
    {
      "chunk_id": "book-12-7dd95a828fbe-chunk-008",
      "response_sha256": "6fdca0ae444cc96d7fe568d219140a84b08ead21536a30be6393c31d2d6c0649"
    }
  ],
  "synthesis": {
    "narrative_spine": [],
    "character_arcs": [],
    "mechanism_evolution": [],
    "world_expansion": [],
    "long_term_reader_hooks": [],
    "style_and_life_force": [],
    "continuity_failures": [],
    "evidence_map": [],
    "creation_family_evidence": {},
    "originality_red_lines": []
  }
}
```
