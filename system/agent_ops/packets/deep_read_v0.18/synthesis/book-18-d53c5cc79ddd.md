# NRL Antigravity Per-Book Synthesis v0.18

Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.
Do not use pre-existing short reports and do not quote source prose.

- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-001.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-002.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-003.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-004.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-005.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-006.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-007.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-008.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-009.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-010.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-011.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-012.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-013.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-18-d53c5cc79ddd-chunk-014.json`

Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.
All synthesis arrays and all nine creation-family keys must be non-empty.
Add evidence_map entries with claim, chunk_id, and exact chapter_heading for every synthesis family.

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "book_id": "book-18-d53c5cc79ddd",
  "book_title": "蛊真人",
  "covered_chunk_ids": [
    "book-18-d53c5cc79ddd-chunk-001",
    "book-18-d53c5cc79ddd-chunk-002",
    "book-18-d53c5cc79ddd-chunk-003",
    "book-18-d53c5cc79ddd-chunk-004",
    "book-18-d53c5cc79ddd-chunk-005",
    "book-18-d53c5cc79ddd-chunk-006",
    "book-18-d53c5cc79ddd-chunk-007",
    "book-18-d53c5cc79ddd-chunk-008",
    "book-18-d53c5cc79ddd-chunk-009",
    "book-18-d53c5cc79ddd-chunk-010",
    "book-18-d53c5cc79ddd-chunk-011",
    "book-18-d53c5cc79ddd-chunk-012",
    "book-18-d53c5cc79ddd-chunk-013",
    "book-18-d53c5cc79ddd-chunk-014"
  ],
  "covered_chunk_hashes": [
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-001",
      "response_sha256": "9183783d39c5af56bcc35cf8ac409c42a4a3964348cf380f7f9813bd1f48f622"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-002",
      "response_sha256": "d390663f180569fc756c05585bbce27655f0b01e4f9b7784708b33e85898f9e3"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-003",
      "response_sha256": "7b34638525ce762154fe1d5b7d376707b949fb5eddd4ecb5c9b8c7d69d530318"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-004",
      "response_sha256": "c395dc9d39cce9ad586eb347010e6a4fb8c2342e7a20735e4cb498676ca3c779"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-005",
      "response_sha256": "c65555f62493336307d4fc353f4e52fc07e6647e1e00dd5e1342044557ecdd70"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-006",
      "response_sha256": "3cdd023d4796fb03e1bed9b7981dad8b6a68e09c62201fc0bbdf5ed39768c7e2"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-007",
      "response_sha256": "6c0c6537aacb4cde5ddaa934a55a89db35eddbeb1c3f2d7b87dc46d6e79d7634"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-008",
      "response_sha256": "9a48239565b2b5b7d9ecafe2effbb7dbe88eec8106ebf2e1b2cbfde326934763"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-009",
      "response_sha256": "deab40e1de42c27e4dc2347cf63eebca35db9036a750de82ae30117efb05c57e"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-010",
      "response_sha256": "77d9287fd41bf08f4fde2a67c41de253c3112cdd950773d5eaca861b87f2552f"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-011",
      "response_sha256": "a602ee47144fb95d3a208f7f9fc56ea017a08d28c5691de33b0d377169617a1f"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-012",
      "response_sha256": "637a121f804860688baf8408a7690e6ba86d7a55e633a88f073c6654f8dc9b48"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-013",
      "response_sha256": "87ee035fd413aee1a0a14beca1a86aa0934e286087421bea6ef77e5a19f9197c"
    },
    {
      "chunk_id": "book-18-d53c5cc79ddd-chunk-014",
      "response_sha256": "9f9fc1e592a1683ff6a755de575bd2ec58dddd51c798382dde4943539690ee0d"
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
