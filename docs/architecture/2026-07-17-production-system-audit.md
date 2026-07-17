# NRL Production System Audit

## Verdict

The ten-layer v0.4 Corpus-to-Creation architecture remains the correct system
boundary. The first volume proves that the research, creation-asset, planning,
chapter-runtime, continuity, review, settlement, and release layers can complete
a 100-chapter production run without reading raw corpus text during writing.

The system is production-grade for controlled local production and clean-clone
deployment. Release truth remains stricter than chapter acceptance: a release
is valid only when every effective chapter body, every ten-chapter review hash,
all titles, and the exported package agree.

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

### Fixed: clean-checkout corpus verification

Production validation previously required the protected `novel_training_set/`
directory even though raw novels must not enter Git. A promotion attestation now
hash-binds 166 durable artifacts: the plan and validation records, 143 chunk
responses, 18 book syntheses, and cross-book distillation. Research machines can
revalidate against protected sources; clean production checkouts verify the
promoted root without reading or storing raw novels.

### Fixed: environment-dependent tests

Agent tests now inject a bounded fake adapter instead of assuming a locally
installed `agy` binary. Runtime CI installs the Studio dependencies before tests
that invoke `studio-build`, server checks allow realistic clean-run latency, and
the GitHub workflow uses current Node-based action releases.

### Fixed: first-window contract gap

Chapters 1-10 now have a retrospective, settlement-derived Story Window. It
does not rewrite accepted prose; it records the same event, choice, state-delta,
and hook contract used by the active runtime. Volume 1 therefore exposes ten
validated ten-chapter windows rather than one legacy exception plus nine current
windows.

### Fixed: resumable deep-read dispatch

The deep-read dispatcher now rematerializes an absent UTF-8 bounded chunk from
the protected source byte range and verifies both raw and normalized hashes
before dispatch. A provider timeout, permission error, or malformed response no
longer deletes the previous receipt. Headless Antigravity calls keep the CLI
sandbox active while approving the bounded file-read tool that print mode cannot
prompt for interactively.

## Clean-Checkout Verification

The final acceptance copy excluded `novel_training_set/`, `.nrl-work/`, all
dependency directories, Studio output, release exports, Python caches, and Git
metadata. From that copy the system completed:

- 271 Python tests;
- state validation and the complete production system check;
- promoted deep-read verification over 166 hash-bound artifacts;
- the Studio TypeScript production build; and
- Astryx doctor with six passes, zero warnings, and zero failures.

## Remaining Boundaries

- Automated and independent-model review cannot replace a human publisher's
  final taste, typo, sensitivity, and platform-policy pass.
- `phase0*`, `phase1*`, and `phase2*` remain historical provenance. They should
  not be consulted by the active writing loop unless a migration explicitly
  promotes an artifact into the current fact sources.
- Antigravity is an external backup adapter; quota or client availability may
  pause a requested second opinion or fallback attempt but does not block the
  primary Codex production loop.
- Superseded by v0.27: Hermes is retired from active production; Codex
  Sol/Terra/Luna own the full primary production loop and Antigravity is backup
  only. The route is bound by the v0.27 operational attestation.
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
