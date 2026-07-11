# Provider-Aware Runtime Design

## Goal

Allow NRL to use staggered Antigravity and OpenCode Go quotas without changing verified v0.18 chunk evidence or allowing prose generation.

## Decisions

- Keep all valid v0.18 chunk responses immutable.
- Add per-book synthesis evidence objects that bind each conclusion to a validated chunk ID and exact chapter heading.
- Generalize dispatch for book synthesis, cross-book distillation, and project reconciliation to support `agy` and `opencode-go`.
- Persist provider attempts in a runtime ledger with provider, model, outcome, classified error, and retry eligibility.
- Apply a local subprocess timeout to Antigravity as already used for OpenCode.

## Constraints

- No API keys or model output logs in git.
- No raw corpus input outside existing bounded deep-read files.
- No transition past production readiness gates.
