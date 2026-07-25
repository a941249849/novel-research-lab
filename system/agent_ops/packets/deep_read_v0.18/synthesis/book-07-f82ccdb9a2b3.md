# NRL Antigravity Per-Book Synthesis v0.18

Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.
Do not use pre-existing short reports and do not quote source prose.

- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-001.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-002.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-003.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-004.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-005.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-006.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-07-f82ccdb9a2b3-chunk-007.json`

Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.
All synthesis arrays and all nine creation-family keys must be non-empty.
Add evidence_map entries with claim, chunk_id, and exact chapter_heading for every synthesis family.

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "book_id": "book-07-f82ccdb9a2b3",
  "book_title": "《大主宰》（校对版全本）作者：天蚕土豆",
  "covered_chunk_ids": [
    "book-07-f82ccdb9a2b3-chunk-001",
    "book-07-f82ccdb9a2b3-chunk-002",
    "book-07-f82ccdb9a2b3-chunk-003",
    "book-07-f82ccdb9a2b3-chunk-004",
    "book-07-f82ccdb9a2b3-chunk-005",
    "book-07-f82ccdb9a2b3-chunk-006",
    "book-07-f82ccdb9a2b3-chunk-007"
  ],
  "covered_chunk_hashes": [
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-001",
      "response_sha256": "3a8f11ae0340bf2c0d8605690b1ba5d028052d912cb2f970ba19ded57060e58d"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-002",
      "response_sha256": "9e9f6517d5ccef6a965a0e46160dc7160d08b2f8ba7036c4c4c616af3dba3b51"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-003",
      "response_sha256": "0ec13a8417150d8e13feac4a5163aac572904a30739ad88879829473343e19a4"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-004",
      "response_sha256": "f0e0aebeb3dc6be55282672916500faa9a420137247ad5d8851973983bca7653"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-005",
      "response_sha256": "dc278ed37ff85078e2913f74e5d505fe499e34255a594ec9158f1884551a5c47"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-006",
      "response_sha256": "3b499a4cfc09b2915fa3dc971a49f94687cdd501ae12e051e1479edb78cb327c"
    },
    {
      "chunk_id": "book-07-f82ccdb9a2b3-chunk-007",
      "response_sha256": "e24b488589a1d75ae57e4942c2dc7aa93c16ea8465c6aa3bfc21d513f706f9ba"
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
