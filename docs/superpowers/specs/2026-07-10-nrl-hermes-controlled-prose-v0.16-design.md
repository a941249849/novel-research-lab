# NRL Hermes Controlled Prose v0.16 Design

## Purpose

Make Hermes a real, auditable NRL CLI adapter and use it only for one bounded
prose test after the promoted final assets and independent Antigravity audit.

## Flow

```text
Owner decision + promoted assets + Antigravity ACCEPT/ACCEPT_WITH_WARNINGS
  -> Codex builds a safe context packet from approved files
  -> hermes --oneshot (Codex OAuth, gpt-5.6-terra)
  -> controlled inbox output
  -> deterministic boundary and quality validation
```

Hermes returns text to stdout; Codex owns every file write. Hermes receives no
raw corpus path or content and cannot mutate runtime state.

## Gate

The test requires `authorize_controlled_prose_test` with
`generate_controlled_prose_test` and mission `phase2g_controlled_prose_test`.
It does not authorize a chapter, serial production, or phase advancement.

## Output Contract

- One 800-1,400 Chinese-character opening-scene test.
- Must use the promoted protagonist, mother-debt pressure, Mudlamp Lane mutual
  aid, a visible physical cost, and supernatural sensory evidence.
- Must not expose schema, ledger, database, metric, transaction, or audit
  vocabulary in reader-facing prose.
- Must not contain a chapter heading, raw-corpus path, or source-work content.

## Non-Goals

No full chapter, volume outline, bulk prose production, automatic publishing,
or Antigravity prose generation. The Antigravity audit is a read-only review.
