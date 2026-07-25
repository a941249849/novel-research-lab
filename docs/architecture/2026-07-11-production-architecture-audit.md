# NRL Production Architecture Audit

## Verdict

The v0.4 ten-layer Corpus-to-Creation architecture remains correct. It does not
need replacement. Its implementation previously had two critical gaps: corpus
depth was overstated, and the chapter production lifecycle was missing. Those
gaps are addressed by v0.18, v0.19, and v0.20 child runtimes.

## External Comparison

The audit inspected current source repositories and official documentation:

- InkOS: <https://github.com/Narcooo/inkos>
- Novel-OS: <https://github.com/mrigankad/Novel-OS>
- AutoNovel: <https://github.com/NousResearch/autonovel>
- AutoGen state persistence:
  <https://microsoft.github.io/autogen/dev/user-guide/agentchat-user-guide/tutorial/state.html>
- LangGraph supervisor reference:
  <https://reference.langchain.com/python/langgraph-supervisor/supervisor>

The reusable production patterns are compiled context, rule stacks, immutable
state deltas, continuity audits, trace artifacts, resumable execution, and
model routing by role. NRL already has a local state machine and heterogeneous
client adapters, so adding LangGraph or AutoGen would duplicate orchestration
without solving a current blocker.

## Retained Architecture

1. Protected corpus.
2. Verifiable single-book decomposition.
3. Cross-book mechanism distillation.
4. Research asset retrieval.
5. Original project synthesis.
6. Long-form creation asset OS.
7. Planning and context compilation.
8. Agent review and chapter production.
9. Runtime control plane.
10. Read-only Studio.

## Added Child Runtimes

- v0.18: contiguous corpus deep reading and hierarchical synthesis.
- v0.19: full-corpus impact review for `《借天改命账》`.
- v0.20: per-chapter intent, context, rule stack, trace, draft, observation,
  continuity audit, revision, and settlement lifecycle.

## Redundancy Decisions

- v0.8 proof is retained only as historical sampled-access provenance.
- `phase1/` and `phase1D/` remain historical inputs; promoted v0.18 derivatives
  become the corpus-depth truth source.
- `current_phase_state.json` owns story/gate state. `mission_registry.json`
  records execution attempts only. They are not interchangeable.
- `project_assets.v0.2.json` is the only mutable creation-asset store.
- `chapter_registry.v0.20.json` is the only chapter execution state.
- Studio snapshots are generated views and cannot authorize or mutate story
  state.
- Agent output remains candidate data until schema, hash, and review gates pass.

The machine-readable ownership contract is
`system/control_plane/source_ownership.v0.20.json`.

## Agent Topology

No additional persistent model clients are required:

- Codex is supervisor, compiler, validator, observer, and state settler.
- Antigravity performs deep reading and independent literary/continuity audit.
- Hermes is writer and bounded reviser after readiness gates.

The chapter lifecycle has multiple roles but only three execution adapters.
This preserves the original three-client design without forcing the Owner to
manually relay every stage.

## Remaining Gate

Production prose remains blocked until v0.18 is `deep_read_verified`, v0.19 is
accepted, creation assets validate, and the v0.20 runtime passes a multi-scene
stress test. Passing one sample scene is not sufficient evidence for serial
production.

## v0.21 Independent Review Closure

The production release gate additionally requires live corpus re-attestation,
hash-bound hierarchical synthesis, governed reconciliation application,
strict chapter chronology, separate draft/revision audits, observed-fact-bound
state settlement, and atomic state writes. These are implementation hardening
requirements under the existing v0.4 architecture, not new architecture layers.
