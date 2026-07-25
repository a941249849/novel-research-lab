# NRL Antigravity Per-Book Synthesis v0.18

Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.
Do not use pre-existing short reports and do not quote source prose.

- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-001.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-002.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-003.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-004.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-005.json`
- `system/agent_ops/inbox/deep_read_v0.18/chunks/book-01-45bcee82acba-chunk-006.json`

Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.
All synthesis arrays and all nine creation-family keys must be non-empty.
Add evidence_map entries with claim, chunk_id, and exact chapter_heading for every synthesis family.

```json
{
  "job_id": "job-v018-verifiable-deep-reading",
  "contract_version": "0.18",
  "book_id": "book-01-45bcee82acba",
  "book_title": "《一念永恒》（校对版全本）作者：耳根",
  "covered_chunk_ids": [
    "book-01-45bcee82acba-chunk-001",
    "book-01-45bcee82acba-chunk-002",
    "book-01-45bcee82acba-chunk-003",
    "book-01-45bcee82acba-chunk-004",
    "book-01-45bcee82acba-chunk-005",
    "book-01-45bcee82acba-chunk-006"
  ],
  "covered_chunk_hashes": [
    {
      "chunk_id": "book-01-45bcee82acba-chunk-001",
      "response_sha256": "7ae575b08be84988bea725ca488be0aac17bb1619f65e8498b781b971a6684b0"
    },
    {
      "chunk_id": "book-01-45bcee82acba-chunk-002",
      "response_sha256": "11fb59fb7cb78446e20e5b1753031dd5711f7e8813f659b5db346144eaf6b4b7"
    },
    {
      "chunk_id": "book-01-45bcee82acba-chunk-003",
      "response_sha256": "b5f909d528067b7179e8817c1c855f584693c88693f238e9f9844e25867b9cb8"
    },
    {
      "chunk_id": "book-01-45bcee82acba-chunk-004",
      "response_sha256": "8ff9801b64cc6a12eaa45d853788855c32a7649e17a6ac3916489f833eb9795d"
    },
    {
      "chunk_id": "book-01-45bcee82acba-chunk-005",
      "response_sha256": "070c60ea4671c95d820ca9b191d22ead7e1f5c968d60658c822aca593f710228"
    },
    {
      "chunk_id": "book-01-45bcee82acba-chunk-006",
      "response_sha256": "614bcc6ab02128e89c45f7eedf37cc4c1070445fe48a50365b86d5b97aed66a3"
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
