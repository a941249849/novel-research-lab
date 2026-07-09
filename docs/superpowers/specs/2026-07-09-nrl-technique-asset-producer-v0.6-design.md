# NRL Technique Asset Producer v0.6 Design Spec

## Accepted Direction

v0.5 created the first operational DNA Production Runtime:

```text
DNA Registry
  -> Research RAG Index
  -> Agent Job Queue
  -> Antigravity packet / inbox / validation / outbox
```

v0.6 must connect that runtime to the first creation asset producer. The first
target is `techniques`, because the creation coverage matrix marks techniques
as missing and v0.5 has a validated Antigravity review for the techniques job.

## Product Goal

Create a deterministic, schema-bound Technique Asset Producer that converts
validated evidence into seed-level technique candidate assets. This is the
first working bridge from research DNA to the project asset store.

The Owner should be able to run:

```text
python3 system/runtime/nrl.py producer-status
python3 system/runtime/nrl.py produce-techniques --job-id job-v05-techniques-antigravity-review
python3 system/runtime/nrl.py validate-creation-assets
```

and see that the system can produce valid, traceable technique candidates
without writing prose, final technique trees, or chapter content.

## Non-Goals

- No prose generation.
- No combat scenes.
- No final technique tree.
- No final naming dictionary.
- No character or NPC generation.
- No Hermes execution.
- No automatic Antigravity execution.
- No raw `novel_training_set/` reads.
- No Owner Gate bypass.

## Inputs

The producer reads only structured runtime artifacts:

- `system/agent_ops/job_queue.v0.5.json`
- `system/agent_ops/outbox/job-v05-techniques-antigravity-review_validated.md`
- `system/dna_registry/dna_registry.v0.5.json`
- `system/research_index/research_rag_index.v0.5.json`
- `system/creation_assets/project_assets.v0.2.json`
- `system/creation_assets/schemas/techniques.schema.json`

The validated Antigravity review is used as a gate signal and source reference.
It is not treated as a creative-writing model.

## Output

The producer writes seed technique candidates into:

```text
system/creation_assets/project_assets.v0.2.json
```

Each candidate is a normal creation asset envelope:

- `asset_id`
- `family: techniques`
- `display_name`
- `lifecycle_state: seed`
- `source_refs`
- `relationships`
- `constraints`
- `technique`

The `technique` payload remains intentionally small because the existing schema
only supports:

- `cost`
- `counter_ids`

v0.6 may create 3 candidates:

- `technique_costed_advancement`
- `technique_backlash_guard`
- `technique_state_reversal`

These are abstract system candidates, not final in-world move names.

## Producer Rules

The producer must:

1. Require the target job to be `validated`.
2. Require at least three RAG evidence items with positive evidence weight.
3. Require every produced asset to cite:
   - the validated Antigravity outbox path
   - at least one source DNA id
4. Use `lifecycle_state: seed`.
5. Keep display names descriptive and non-final.
6. Avoid relationships that create unresolved references.
7. Preserve existing project assets and upsert only the candidate ids it owns.
8. Remain idempotent: repeated runs must not duplicate assets or rewrite
   unchanged assets with noisy timestamps.

## Status Contract

`producer-status` must report:

- producer version
- supported families
- whether the techniques job is validated
- candidate count for techniques
- whether project asset store validates
- blocked actions
- next safe action

## Studio / API Boundary

Studio may expose producer status as data, but no new display-only panel is
required in v0.6.

The local server may expose:

```text
GET /api/producer-status
```

No API route may invoke production.

## Safety Rules

- Owner Gate remains active.
- Hermes remains `paused_not_removed`.
- Antigravity remains `manual_handoff`.
- `advance` remains blocked at Owner Gate.
- The producer may create seed assets, but it must not mark the family
  complete.
- Generated assets must not include `novel_training_set/`.
- Generated assets must not include words that imply prose or chapter output:
  `正文`, `第一章`, `Chapter 1`.

## Acceptance

- `producer-status` reports techniques as supported and the v0.5 job as
  validated.
- `produce-techniques --job-id job-v05-techniques-antigravity-review` writes
  exactly three seed `techniques` assets.
- Re-running `produce-techniques` remains idempotent.
- `validate-creation-assets` passes after production.
- `project_assets.v0.2.json` contains no raw corpus paths.
- `studio-data` contains `asset_producers`.
- `GET /api/producer-status` returns producer status.
- Existing v0.5, v0.4, v0.3, v0.2, and SYS-3 tests remain green.
