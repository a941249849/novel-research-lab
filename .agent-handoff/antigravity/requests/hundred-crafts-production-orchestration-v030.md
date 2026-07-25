# Antigravity Production Orchestration Review v0.31

Perform one independent, read-only release-gate review for Novel Research Lab.
Do not edit files, generate prose, authorize production, use subagents, or
narrate tool usage.

Canonical baseline:

`397559ead2903aa8c0c31ff04050d74f3a045e2d20a66d08d60e3e570cc8aabc`

Compute the baseline with `shasum -a 256
projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json`.
The existing final-review index is expected to be `valid=false` before this
fresh review and is not the source of the current baseline. Do not treat its
older `bound_baseline_sha256` as the active baseline or as a blocking finding.

Review:

- `system/runtime/nrl_codex_writer.py`
- `system/runtime/nrl_project_production.py`
- `system/runtime/nrl_production_runtime.py`
- `system/runtime/nrl_volume1_release.py`
- `tests/test_codex_direct_writer.py`
- `tests/test_hundred_crafts_production_readiness.py`
- `tests/test_production_chapter_runtime_v020.py`
- `projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json`
- `projects/hundred-crafts-night-procession/production_runtime/quality/first_window_quality_contract.v1.json`
- `projects/hundred-crafts-night-procession/production_runtime/chapter_registry.v0.20.json`
- `system/projects/hundred-crafts-night-procession/project.json`

Verify:

1. Formal production is still fail-closed, project-isolated, limited to the
   Owner-authorized 001-010 window, and chapter 11 remains blocked.
2. Codex Terra writes, Luna observes, and Sol audits; provider request schemas
   do not weaken the unchanged local Draft-07 validation.
3. Independent review prefers Antigravity. OpenCode Go is accepted only as a
   truthful fallback with exact provider/model identity, request/report/
   execution hashes, successful execution metadata, and baseline-bound
   Antigravity-unavailable evidence.
4. Neither final-review nor window-review records can be accepted through
   provider impersonation, stale hashes, missing evidence, or self-reported
   model identity.
5. Failed prose candidates remain quarantined, formal registry is empty, and
   `content_authorized=false`.
6. The canonical baseline is current and binds all runtime sources including
   `system/runtime/opencode_direct.mjs`.
7. Semantic revision retries rewrite the complete chapter, explicitly execute
   every required fix, and delete or merge repeated ending beats. A short
   revision must be retried as a full rewrite; it must not be padded by
   inserting or appending an alternate duplicate tail.
8. Every audit issue, including `minor`, enters the revision path. The runtime
   may reuse the draft only when the audit issue list is empty.
9. Settlement candidates include only observation facts that exactly match a
   frozen intent delta by asset, field, before, and after, and emit at most one
   delta per declared key. Observation-only facts never mutate canonical state.
10. Settlement validation independently rejects duplicate asset/field keys,
    including manually supplied payloads that bypass candidate generation.
11. A short semantic revision retry carries the prior corrected text only as
    rewrite material, raises the target to 3800-4000 Chinese characters, and
    still requires a complete rewrite rather than insertion or tail append.
12. When every issue is exact repetition and a repeated suffix paragraph block
    is mechanically provable, the runtime removes only the duplicate suffix,
    preserves the Terra source execution binding, and still requires Luna
    observation plus Sol final audit. Other issues continue through full rewrite.
13. The deterministic route rejects mixed semantic fixes, compares suffix
    paragraphs byte-for-byte, and validates Terra source execution before
    ingesting or advancing any revision state.

Return a concise report with blocking findings, residual risks, and concrete
evidence. It must end with exactly these two unformatted lines and contain no
other line beginning with `BASELINE:` or `VERDICT:`:

BASELINE: 397559ead2903aa8c0c31ff04050d74f3a045e2d20a66d08d60e3e570cc8aabc
VERDICT: ACCEPT

If a blocking defect exists, replace only the final line with
`VERDICT: REVISE`.
