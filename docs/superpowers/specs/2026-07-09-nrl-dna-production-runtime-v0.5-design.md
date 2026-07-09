# NRL DNA Production Runtime v0.5 Design Spec

## Accepted Direction

Novel Research Lab is a DNA-based Corpus-to-Creation system:

```text
provided novel corpus
  -> single-book reading and decomposition
  -> Book / Narrative / Mechanism / State DNA
  -> cross-book mechanism distillation
  -> creation mother-library
  -> original project Story Bible and asset system
  -> agent review and production
  -> Hermes writing only after explicit authorization
```

v0.5 corrects the v0.4 failure mode. v0.4 made the architecture visible, but it
did not make the system operational. v0.5 must build the production runtime
that moves artifacts through the DNA pipeline.

## Product Goal

Within five minutes, the Owner should be able to answer:

1. What DNA assets exist in the mother-library?
2. Which DNA assets are only stubs, candidates, or promoted evidence?
3. Which production job is next?
4. Which Agent owns the next job?
5. What must be given to Antigravity, and where must its output return?
6. Which returned artifacts passed validation and can be promoted?
7. Which creative asset family is still blocked?
8. Why Hermes is not yet allowed to write prose?

## Non-Goals

- No Phase 2F transition.
- No prose generation.
- No chapter drafting.
- No final character sheets, technique trees, naming dictionaries, or NPC
  dossiers.
- No raw `novel_training_set/` reads.
- No fake Antigravity or Hermes execution.
- No new display-only dashboard work.
- No database migration. v0.5 remains file-backed.

## Runtime Sources Of Truth

Existing runtime sources remain authoritative:

- `system/mission_controller/current_phase_state.json`
- `system/runtime/mission_registry.json`
- `system/runtime/agent_adapters.json`
- `system/creation_assets/creation_asset_registry.v0.1.json`
- `system/creation_assets/project_assets.v0.2.json`
- `system/creation_assets/schemas/*.schema.json`
- `phase1/05_review/phase1C_asset_manifest.json`
- `phase1/04_mechanism_library/category_manifest.json`

v0.5 adds generated runtime indexes under:

- `system/dna_registry/dna_registry.v0.5.json`
- `system/agent_ops/job_queue.v0.5.json`
- `system/agent_ops/packets/`
- `system/agent_ops/inbox/`
- `system/agent_ops/outbox/`
- `system/research_index/research_rag_index.v0.5.json`

These files are runtime artifacts, not creative content.

## DNA Registry

The DNA Registry is the creation mother-library index. It must normalize
existing structured assets into five entity families:

- `book_dna`
- `narrative_dna`
- `mechanism_dna`
- `state_dna`
- `project_dna`

Each DNA entry contains:

- `dna_id`
- `family`
- `title`
- `source_path`
- `review_state`
- `provenance`
- `promotion_state`
- `evidence_tags`
- `blocked_for_generation`

Promotion states are:

- `stub`
- `candidate`
- `promoted`
- `blocked`

The registry must reject raw corpus paths and must preserve source provenance.

## Agent Job Queue

v0.5 introduces a real file-backed Agent Job Queue. Job states are:

- `planned`
- `ready_for_codex`
- `ready_for_antigravity`
- `external_running`
- `output_received`
- `validated`
- `promoted`
- `rejected`
- `blocked`

Each job contains:

- `job_id`
- `job_type`
- `target_family`
- `owner_agent`
- `state`
- `source_dna_ids`
- `input_packet_path`
- `expected_output_path`
- `actual_output_path`
- `validation_report_path`
- `promotion_target`
- `created_at`
- `updated_at`
- `blocked_reason`

Job queue commands must be deterministic and must not execute arbitrary shell
commands.

## Antigravity Pack / Inbox / Outbox

Antigravity remains manual and external, but the workflow must become
productized:

1. Codex creates a standard Antigravity packet from a job.
2. The packet lands in `system/agent_ops/packets/`.
3. The Owner runs Antigravity manually in the shared project folder.
4. Antigravity output is placed in `system/agent_ops/inbox/`.
5. Codex ingests the output, validates path, job id, required sections, and
   forbidden actions.
6. Validated output is copied into `system/agent_ops/outbox/`.
7. The job becomes `validated` or `rejected`.

The packet must clearly tell Antigravity to perform literary review and
structural analysis only. It must not request prose generation.

## Research RAG Index

The Research RAG Index is a structured retrieval surface over already reviewed
derivatives. It is not model training and it does not read raw novels.

Each index item contains:

- `index_id`
- `source_dna_id`
- `source_path`
- `title`
- `asset_type`
- `mechanism_categories`
- `retrieval_text`
- `evidence_weight`

Retrieval text must be concise metadata derived from structured assets and
mechanism manifests, not copied novel prose.

## Creation Producer Boundary

v0.5 may produce schema-bound job plans and evidence packets for creation
asset families. It must not produce final story assets.

The first production target is the current next family from v0.3:

```text
techniques
```

The output is an Agent job plus evidence packet for technique-system planning,
not a final technique tree.

## Studio Role After v0.5

Studio is demoted from product center to workbench surface. It should read the
same runtime data and show:

- DNA Registry summary
- Agent Job Queue
- current Antigravity packet
- inbox/outbox status
- Research RAG Index summary
- blocked Hermes readiness

Studio changes are only allowed when backed by actual runtime data produced by
v0.5. No display-only panels are accepted.

## CLI Interfaces

Add:

```text
dna-registry
dna-registry-build
rag-index
rag-index-build
agent-jobs
agent-job-plan --family <asset_family>
agent-pack --job-id <job_id>
agent-ingest --job-id <job_id> --file <path>
agent-validate --job-id <job_id>
production-runtime-status
```

Existing v0.1-v0.4 commands must remain backward compatible.

## Safety Rules

- `advance` remains blocked at Owner Gate.
- Hermes remains `paused_not_removed`.
- Antigravity remains `manual_handoff`.
- `novel_training_set/` must not appear in generated v0.5 runtime artifacts.
- Job packets must list forbidden actions.
- Output ingest must reject files outside the repository unless explicitly
  copied into `system/agent_ops/inbox/`.
- No job may transition directly from `planned` to `promoted`.

## Acceptance

- `dna-registry-build` generates `system/dna_registry/dna_registry.v0.5.json`.
- `dna-registry` reports all five DNA families and no raw corpus paths.
- `rag-index-build` generates `system/research_index/research_rag_index.v0.5.json`.
- `rag-index` reports structured retrieval items with evidence weights.
- `agent-job-plan --family techniques` creates one job in
  `system/agent_ops/job_queue.v0.5.json`.
- `agent-pack --job-id <job_id>` creates a manual Antigravity packet.
- `agent-ingest` rejects files outside `system/agent_ops/inbox/`.
- `agent-validate` rejects missing required sections and forbidden content.
- A valid sample Antigravity output can move a job to `validated`.
- `production-runtime-status` shows DNA, RAG, queue, Antigravity, Hermes, and
  Owner Gate status.
- `system-status` remains `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- `advance` still stops at Owner Gate.
- Existing Python tests remain green.
