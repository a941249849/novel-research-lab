# NRL Corpus-to-Creation Ingestion v0.14 Design

## Intent

Turn the validated Antigravity full-corpus review into a structured research
asset manifest that the existing evidence-pack and creation-contract pipeline
can consume. This closes the gap between “18 books were reviewed” and “the
creation pipeline has traceable family evidence.”

## Scope

- Ingest only the validated structured outbox artifact.
- Preserve book reviews, cross-book mechanisms, and nine family evidence sets.
- Keep raw `novel_training_set/` files out of every derived artifact.
- Align registered Agent review inputs with the exact evidence-pack IDs.
- Enrich the naming contract with roots, form rules, originality policy, and
  anti-contamination terms.
- Reject naming assets containing forbidden Phase 2A concepts.

## Non-Goals

- No raw novel reading by Codex.
- No final names, character cards, NPC sheets, faction dossiers, technique
  trees, chapter plans, or prose.
- No Hermes execution.
- No automatic promotion of final creative assets.

## Acceptance Contract

The ingest command must refuse missing, unvalidated, malformed, or raw-path
source artifacts. A successful output must contain 18 book reviews, 12
cross-book mechanisms, and all nine family evidence sections, with provenance,
owner decision, and content-generation disabled. Agent packets must use the
same evidence IDs emitted by the pipeline plan.
