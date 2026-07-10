# NRL Production Chapter Runtime v0.20 Design

## Purpose

NRL has a differentiated research stack and a validated creation-asset store,
but it does not yet have a production-grade chapter lifecycle. v0.20 adds that
missing runtime without replacing the v0.4 Corpus-to-Creation architecture.

The design was checked against current InkOS, Novel-OS, AutoNovel, AutoGen
state persistence, and LangGraph supervisor patterns. The useful common ideas
are compiled context, explicit handoffs, immutable state deltas, continuity
audits, and resumable state. NRL keeps its local file-state runtime instead of
adding a framework dependency.

## Chapter State Machine

```text
chapter_intent
  -> context_compiled
  -> draft_generated
  -> facts_observed
  -> continuity_audited
  -> revision_generated
  -> state_settled
  -> chapter_accepted
```

Every transition requires the previous artifact to validate. No Agent may
claim a stage completed without a valid artifact on disk.

## Per-Chapter Artifacts

- `intent.json`: dramatic purpose, must-keep, must-avoid, expected state deltas.
- `context.json`: only the relevant Story Bible, assets, prior state, hooks, and
  research mechanisms selected for this chapter.
- `rule_stack.json`: ordered hard rules, project rules, volume rules, scene
  constraints, anti-AI style rules, and one-off Owner direction.
- `trace.json`: source hashes and why each context item was selected.
- `draft.md`: Hermes prose output; never accepted directly.
- `observation.json`: over-extracted facts for characters, NPCs, locations,
  factions, artifacts, techniques, relationships, emotions, information,
  hooks, timeline, physical state, and naming.
- `continuity_audit.json`: Antigravity findings against canonical truth.
- `revision.md`: bounded Hermes revision responding only to accepted findings.
- `settlement.json`: validated state delta applied by Codex.

## Role Mapping

- Codex: production supervisor, intent compiler, context composer, rule-stack
  compiler, schema validator, fact observer, state-settlement executor.
- Hermes (`gpt-5.6-terra`): writer and bounded literary reviser only.
- Antigravity: independent continuity, pacing, vitality, originality, and
  anti-AI-taste auditor.
- Owner: project direction and exceptional gate authority, not manual courier.

These are workflow roles, not eight new persistent Agent processes.

## Canonical Truth

The canonical production sources are reduced to:

1. Story Bible and volume outline.
2. Creation asset store.
3. Accepted chapter settlements.
4. Owner direction.

Research assets are read-only evidence used by the context compiler. Historical
phase documents and v0.8 proof files are provenance, not live truth sources.

## Anti-AI and Literary Quality

The rule stack includes measurable and reviewable checks for repetitive sentence
openings, paragraph symmetry, exposition density, abstract-vs-sensory balance,
dialogue distribution, repeated metaphors, transition-word habits, rhetorical
templates, named-entity drift, and emotional causality. Metrics flag candidates;
Antigravity makes the literary judgment. No banned-word counter alone can claim
human-quality prose.

## Production Gate

No chapter draft may start until all are true:

- v0.18 status is `deep_read_verified`.
- v0.19 project reconciliation is accepted.
- creation asset store validates.
- chapter runtime schemas validate.
- current Story Bible, Volume 1 outline, and state ledger hashes are locked.
- a bounded chapter intent exists.

## Redundancy Policy

- Keep historical phase and proof artifacts, but mark them provenance-only.
- Do not add another independent mission registry or database.
- `current_phase_state.json` remains story/gate state; chapter runtime owns only
  chapter execution state.
- Studio reads generated status; it does not duplicate state.
- Agent outputs are candidates until deterministic validation and the required
  independent review complete.

## Non-Goals

- No prose in this implementation pass.
- No autonomous publishing or bulk chapter generation.
- No importing InkOS, LangGraph, or AutoGen runtime dependencies.
- No direct imitation or style transfer from corpus books.
