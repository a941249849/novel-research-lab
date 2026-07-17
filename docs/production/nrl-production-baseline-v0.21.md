# NRL Production Baseline v0.21

## Scope

This baseline freezes the verified Corpus-to-Creation runtime before continuous
chapter production. It is not a content-completion claim.

## Production Contract

- Corpus research remains read-only and is never read by the chapter runtime.
- `system/creation_assets/project_assets.v0.2.json` is the active creation
  asset store.
- `system/production_runtime/active_story_blueprint.v0.24.json` is the active
  long-form blueprint.
- Accepted chapter artifacts are immutable and must be followed through the
  chapter runtime, not edited directly.
- The active v0.27 route supersedes the original writer assignment: Sol owns
  planning and review, Terra owns prose and bounded editing, and Luna owns
  observation and mechanical checks. Antigravity is a non-blocking backup.
  Hermes is retired from the production path.

## Baseline Evidence

- `python3 system/runtime/nrl.py production-preflight` must return `valid: true`.
- The direct-writer calibration must remain `accepted_route_restricted`.
- The current accepted chapter set is `chapter-0001` through `chapter-0007`.
- Audit packets under `.agent-handoff/antigravity/` are retained because active
  validation records reference them by path.

## Repository Hygiene

- One-off corpus scripts and outputs are archived under
  `.nrl-work/archive/`, which is ignored by Git.
- Sensitive local material is quarantined outside the repository and must not
  be committed.
- New transient output belongs in `.nrl-work/`, never at repository root.

## Production Start

The first continuous production batch is Chapters 8-10. Keep the existing
per-chapter lifecycle intact: Sol draft/revision, Luna final-text observation,
Opus final audit, state settlement, then acceptance.
