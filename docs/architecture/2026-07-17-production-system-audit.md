# NRL Production System Audit

## Verdict

The ten-layer v0.4 Corpus-to-Creation architecture remains the correct system
boundary. The first volume proves that the research, creation-asset, planning,
chapter-runtime, continuity, review, settlement, and release layers can complete
a 100-chapter production run without reading raw corpus text during writing.

The system is production-capable, but release truth must remain stricter than
chapter acceptance. A release is valid only when every effective chapter body,
every ten-chapter review hash, all titles, and the exported package agree.

## Authoritative Flow

1. Protected corpus and verified deep-reading receipts.
2. Promoted book DNA, narrative DNA, state ledgers, and mechanism library.
3. Original project assets across nine creation families.
4. Long-form contract and ten-chapter story windows.
5. Per-chapter intent, bounded context, prose, audit, observation, settlement,
   and immutable acceptance.
6. Optional release-only edits that never rewrite accepted runtime history.
7. Hash-bound ten-chapter literary review over the effective release text.
8. Title registry and reproducible platform export.

## Deep-Audit Findings

### Fixed: stale review acceptance

The release gate previously checked only the stored review verdict. A chapter
could receive a later release edit while the old `ACCEPT` remained visible.
Release readiness and production status now compare every review's chapter IDs
and revision hashes against the current effective text. Any mismatch becomes
`STALE` and blocks release.

### Fixed: incomplete window health check

The operator previously inspected only the latest completed ten-chapter window.
It now checks every completed window in order and stops at the first missing,
rejected, or stale review.

### Fixed: package completeness

Chapter titles are a separate release asset. The package manifest now records
the title, canonical body hash, exported chapter-file hash, full-manuscript path,
and full-manuscript hash. Missing or duplicate titles block release.

### Fixed: repository hygiene

Generated review manuscripts, platform export copies, frontend builds, local
dependencies, and runtime caches are reproducible and excluded from Git. Durable
chapter revisions, observations, audits, settlements, acceptances, release edits,
window reviews, and title assets remain versioned.

### Added: continuous verification

GitHub Actions now runs the full Python suite, state validation, system health
check, Studio TypeScript build, and Astryx doctor on pushes and pull requests.

## Remaining Boundaries

- Automated and independent-model review cannot replace a human publisher's
  final taste, typo, sensitivity, and platform-policy pass.
- `phase0*`, `phase1*`, and `phase2*` remain historical provenance. They should
  not be consulted by the active writing loop unless a migration explicitly
  promotes an artifact into the current fact sources.
- Antigravity is an external review adapter; quota or client availability may
  pause new review work but cannot silently bypass its gate.
- Hermes remains optional literary enhancement, not a required runtime
  dependency.
- Some immutable v0.18 provider receipts under
  `system/agent_ops/inbox/deep_read_v0.18/chunks/` contain raw response framing
  around the bound JSON despite their historical `.json` suffix. The v0.18
  validator extracts and hash-checks the unique payload. Renaming them would
  invalidate the promoted evidence chain, so they remain provenance artifacts,
  not general JSON configuration.

## Release Commands

```bash
python3 system/runtime/nrl.py production-status
python3 system/runtime/nrl.py volume1-release-status
python3 system/runtime/nrl.py volume1-fanqie-package
python3 system/runtime/nrl.py system-check
```
