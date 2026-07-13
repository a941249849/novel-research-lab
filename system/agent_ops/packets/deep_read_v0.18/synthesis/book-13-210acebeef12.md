# NRL Antigravity Per-Book Synthesis v0.18

Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.
Do not use pre-existing short reports and do not quote source prose.

- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-001.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-002.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-003.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-004.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-005.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-006.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-13-210acebeef12-chunk-007.json`

Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.
All synthesis arrays and all nine creation-family keys must be non-empty.
Add evidence_map entries with claim, chunk_id, and exact chapter_heading for every synthesis family.

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "book_id": "book-13-210acebeef12",
  "book_title": "《求魔》（校对版全本）作者：耳根",
  "covered_chunk_ids": [
    "book-13-210acebeef12-chunk-001",
    "book-13-210acebeef12-chunk-002",
    "book-13-210acebeef12-chunk-003",
    "book-13-210acebeef12-chunk-004",
    "book-13-210acebeef12-chunk-005",
    "book-13-210acebeef12-chunk-006",
    "book-13-210acebeef12-chunk-007"
  ],
  "covered_chunk_hashes": [
    {
      "chunk_id": "book-13-210acebeef12-chunk-001",
      "response_sha256": "dd6e62749c978b0b7a29d1999271d42ba0859bf05280ecbfbf6673818caad831"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-002",
      "response_sha256": "0e1279933c6063a710516bf998f5f41ab1021f6871929f7d7eed5376a8bed485"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-003",
      "response_sha256": "9607824e0926bbb79bcf1ad3ca685d6495aca1f5e9990bb5efd2a1acec32f024"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-004",
      "response_sha256": "d220ca090acb7f363c15cee20aa4bb433508e9e66c535cff20f9de6d3f6d833a"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-005",
      "response_sha256": "3dee6ce1c6f3bf25e8cb39a5f0184aaf3645b7adaa07668cb3c8edc5a3551c1b"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-006",
      "response_sha256": "f0fddbe6466d4b7710f099824f597d5d1c6565d1781312cb809a4f68e597c085"
    },
    {
      "chunk_id": "book-13-210acebeef12-chunk-007",
      "response_sha256": "add472f8146f6f0d6bce94a498e55f53a3e0e608a574c76ecd0339c414ab8df0"
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
