# Novel Research Lab Runtime MVP

## What This Runtime Does

`system/runtime/nrl.py` is a minimal local Mission Runtime. It can:

- Read `system/mission_controller/current_phase_state.json`.
- Report current status and the next recommended mission.
- Prepare manual handoff task files for Hermes or Antigravity.
- Register externally produced Hermes or Antigravity outputs.
- Update Mission Controller state after ingest.
- Validate current phase state against `phase_state.schema.json`.

## What This Runtime Does Not Do

- It does not call Hermes.
- It does not call Antigravity through the generic mission adapter or GUI.
- It can call Antigravity CLI only through explicit allowlisted bridge commands.
- It does not generate novel prose.
- It does not generate first chapters.
- It does not generate Outline Trees by itself unless Codex is explicitly tasked outside this runtime.
- It does not read `novel_training_set/`.
- It does not replace Codex validation, Antigravity review, or Owner Gate.

## Why Hermes And Antigravity Use Manual Handoff

No Hermes CLI/API adapter is currently configured, and the generic Antigravity
mission adapter remains manual. The runtime therefore uses:

- Hermes adapter: `manual_handoff`
- Antigravity adapter: `manual_handoff`
- Codex adapter: `local`

Manual handoff means the runtime writes a task file, waits for an external human-run or tool-run agent output, then ingests that output path.

Antigravity also has a separate CLI bridge for bounded review/proof tasks. This
does not change the generic Antigravity adapter to `can_execute: true`.

## Commands

Show current Mission Controller state:

```bash
python3 system/runtime/nrl.py status
```

Run the runtime health check:

```bash
python3 system/runtime/nrl.py doctor
```

Advance the current mission through the next safe runtime step:

```bash
python3 system/runtime/nrl.py advance
```

Show the next mission package:

```bash
python3 system/runtime/nrl.py next
```

Prepare Hermes handoff:

```bash
python3 system/runtime/nrl.py prepare-handoff --agent hermes
```

This writes:

```text
handoff/hermes/current_task.md
```

Prepare Antigravity handoff:

```bash
python3 system/runtime/nrl.py prepare-handoff --agent antigravity
```

This writes:

```text
handoff/antigravity/current_task.md
```

Ingest a Hermes external output:

```bash
python3 system/runtime/nrl.py ingest --agent hermes --file <path>
```

Ingest an Antigravity external review:

```bash
python3 system/runtime/nrl.py ingest --agent antigravity --file <path>
```

Validate current Mission Controller state:

```bash
python3 system/runtime/nrl.py validate-state
```

Emit the read-only data contract used by Studio:

```bash
python3 system/runtime/nrl.py studio-data
```

Emit the read-only Creation Asset Registry:

```bash
python3 system/runtime/nrl.py creation-assets
```

This reports long-form asset family readiness for characters, NPCs, factions,
artifacts, techniques, naming, emotional bonds, foreshadowing, and state
ledger. It is system metadata, not creative generation. It must not create
final character cards, NPC sheets, faction dossiers, technique trees, naming
dictionaries, item catalogs, prose, or chapter plans.

## Future Hermes CLI/API Adapter

A future Hermes adapter can extend `agent_adapters.json` with:

- `mode`: `cli` or `api`
- executable path or endpoint
- input contract path
- output directory
- timeout policy
- failure status mapping

The runtime must still keep blocked actions and Owner Gate checks.

## Future Antigravity CLI/API Adapter

A future Antigravity adapter can extend `agent_adapters.json` with:

- `mode`: `cli` or `api`
- review command or endpoint
- handoff input file
- expected review report path
- status mapping for pass, warnings, hold, or fail

The runtime must not mark review complete until a report artifact is ingested and registered.

## Antigravity Full Corpus Handoff v0.7

Use this when the architecture is frozen and the Owner wants Antigravity to
perform full-corpus rereading, reanalysis, and replanning. This is a manual
external review workflow, not an Antigravity API call.

Generate the Owner-facing command packet:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-pack
```

This writes:

```text
system/agent_ops/packets/job-v07-full-corpus-antigravity-review.md
system/agent_ops/packets/job-v07-full-corpus-antigravity-review-command.md
```

Paste the command file into Antigravity. Antigravity must save the completed
structured review to:

```text
system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md
```

Check handoff status:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-status
```

After Antigravity writes the output file, ingest and validate it:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-ingest --file system/agent_ops/inbox/job-v07-full-corpus-antigravity-review.md
python3 system/runtime/nrl.py antigravity-full-corpus-validate
```

The validator requires the v0.7 JSON Manifest, all nine creation asset
families, at least one book review, at least one cross-book mechanism, and no
forbidden content-generation markers. Hermes remains paused after validation.

## Antigravity CLI Bridge v0.8

Use this when Codex needs to send a bounded task file to Antigravity CLI and
capture the response as a repo artifact. This bridge calls only `agy -p`; it is
not arbitrary shell execution and it does not operate the Antigravity GUI.

Check bridge availability:

```bash
python3 system/runtime/nrl.py antigravity-bridge-status
```

Write a request file:

```bash
mkdir -p .agent-handoff/antigravity/requests .agent-handoff/antigravity/responses
cat > .agent-handoff/antigravity/requests/nrl-review.md <<'EOF'
Review the current NRL runtime state and return a structured markdown report.
Do not write creative prose. Do not advance Owner Gate.
EOF
```

Send it to Antigravity and save the response:

```bash
python3 system/runtime/nrl.py antigravity-bridge-ask \
  --request-file .agent-handoff/antigravity/requests/nrl-review.md \
  --output-file .agent-handoff/antigravity/responses/nrl-review.md \
  --print-timeout 5m0s
```

The last run metadata is written to:

```text
system/agent_ops/antigravity_bridge_last_run.v0.8.json
```

The bridge should be used for bounded review, proof-gated reading tasks, and
second-opinion architecture critique. It should not be used for prose
generation, Owner Gate bypass, or unrestricted full-corpus claims without a
separate proof-of-work validator.

## Full Corpus Proof Gate v0.8

v0.7 structural validation is not enough to prove full-corpus reading. v0.8
adds a separate proof gate that requires one machine-verifiable reading receipt
per corpus file. Receipts contain file paths, byte sizes, SHA-256 hashes, and
early/middle/late/ending byte-range chunk hashes. They must not contain raw
novel prose.

Check proof-gate status and corpus inventory:

```bash
python3 system/runtime/nrl.py full-corpus-proof-status
```

Generate one bounded Antigravity request packet per corpus book:

```bash
python3 system/runtime/nrl.py full-corpus-proof-pack --all
```

Send an individual proof packet through the bridge:

```bash
python3 system/runtime/nrl.py antigravity-bridge-ask \
  --request-file system/agent_ops/packets/full_corpus_proof_v0.8/02-7624374abf2e.md \
  --output-file system/agent_ops/inbox/full_corpus_proof_v0.8/02-7624374abf2e_response.md \
  --print-timeout 15m0s
```

Merge per-book Antigravity responses into a master manifest:

```bash
python3 system/runtime/nrl.py full-corpus-proof-merge \
  --input-dir system/agent_ops/inbox/full_corpus_proof_v0.8 \
  --output-file system/agent_ops/inbox/full_corpus_proof_v0.8/master.md
```

Validate proof before any research-asset promotion:

```bash
python3 system/runtime/nrl.py full-corpus-proof-validate \
  --file system/agent_ops/inbox/full_corpus_proof_v0.8/master.md
```

If a report lacks `reading_receipts`, the validator returns
`schema_valid_but_depth_unverified` and `promotion_allowed: false`.

Promotion from `proof_verified` into a promotable research asset requires a
fresh Owner Gate decision scoped only to research-asset promotion:

```bash
python3 system/runtime/nrl.py owner-gate record \
  --decision-id owner_gate_full_corpus_proof_promote_001 \
  --decision-type authorize_research_promotion \
  --authorized-scope promote_full_corpus_proof_to_research_assets \
  --forbidden-scope generate_novel_prose \
  --forbidden-scope execute_hermes \
  --expires-after-mission job-v08-full-corpus-proof-review
```

This does not authorize prose, chapter planning, Hermes execution, raw corpus
exposure, or automatic content generation. A stale Owner Gate decision with a
different `expires-after-mission` is ignored by `full-corpus-proof-status`.

After that narrow decision exists, run the promotion executor:

```bash
python3 system/runtime/nrl.py full-corpus-proof-promote
```

Without the matching Owner Gate decision, this command exits non-zero and writes
no manifest. With the matching decision, it writes only:

```text
system/research_assets/promotions/full_corpus_proof_v0.9.json
```

The manifest records proof hashes, the Owner decision id, receipt counts,
`content_generation_allowed: false`, and forbidden actions. It still does not
promote prose generation or Hermes execution.

## Owner Gate Rules

Owner Gate is required when:

- A phase explicitly sets `owner_gate_required: true`.
- A review output recommends hold, fail, or major creative correction.
- A mission would authorize prose, first chapter, detailed chapter plans, complete role cards, or new source access.
- A new adapter would move from `manual_handoff` to real `cli` or `api` execution.

Owner Gate is not required for status reads, schema validation, or manual handoff preparation unless the current state says otherwise.

## SYS-3 Runtime Control Patch

SYS-3 keeps Codex / NRL as the local runtime host. Hermes and Antigravity remain external adapters unless their adapter mode is explicitly upgraded by Owner Gate.

New read commands:

```bash
python3 system/runtime/nrl.py missions
python3 system/runtime/nrl.py check-inputs
python3 system/runtime/nrl.py gate-status
```

New handoff and compilation commands:

```bash
python3 system/runtime/nrl.py compile-context --agent antigravity
python3 system/runtime/nrl.py prepare-handoff --agent antigravity
python3 system/runtime/nrl.py ingest --agent antigravity --file handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md
```

Owner Gate records:

```bash
python3 system/runtime/nrl.py owner-gate record --decision-id owner_gate_phase2d_review_acceptance_001 --decision-type accept_review --authorized-scope prepare_phase2e_entry --forbidden-scope write_novel_prose --expires-after-mission phase2e_entry_preparation
python3 system/runtime/nrl.py owner-gate list
```

Studio build:

```bash
python3 system/runtime/nrl.py studio-data
python3 system/runtime/nrl.py studio-build
open system/runtime/studio/index.html
```

Studio is a read-only cockpit plus command launcher. It must not maintain independent project state. It reads `current_phase_state.json`, `mission_registry.json`, and `agent_adapters.json`; it does not call Hermes, does not call Antigravity, does not generate novel prose, and does not read `novel_training_set/`.

`client_handoff` is a staging mode, not API execution. If a client cannot be automated, the runtime falls back to manual handoff while preserving task packet, expected output path, and ingest command.

## SYS-4 Doctor And Smoke Harness

Use `doctor` as the first local check before moving a mission forward:

```bash
python3 system/runtime/nrl.py doctor
```

Use `system-status` to check whether the runtime is in system hardening mode
or content progression mode:

```bash
python3 system/runtime/nrl.py system-status
```

When Owner Gate is pending, `system-status` reports:

```text
operating_mode: SYSTEM_HARDENING
content_progression: FROZEN_AT_OWNER_GATE
```

This means the current review output is a system-state sample. Do not advance
the story phase, do not write novel prose, do not write the first chapter, and
do not generate full character cards.

Hermes is paused, not removed. Its durable role is later writer or literary
enrichment after explicit authorization. While paused, system hardening and
production-chain work continue through Codex local runtime work and
Antigravity manual review packages.

Use `advance` as the normal single entrypoint for progression:

```bash
python3 system/runtime/nrl.py advance
```

`advance` is intentionally conservative:

- If no handoff attempt exists, it prepares one.
- If a handoff attempt exists but the expected output file is missing, it waits and reports the exact missing file.
- If the expected output file exists, it ingests it through the existing ingest contract.
- If Owner Gate is required, it stops and reports that a manual owner decision is required.
- It must not reuse an old Owner Gate decision for a later gate.

For Antigravity, the handoff input is consolidated into one file:

```text
handoff/antigravity/current_packet.md
```

Use that packet as the single Antigravity prompt/input surface. The expected
output path is mission-specific and appears in `doctor`, `next`, and the
handoff packet. For the current Phase 2E planning review it is:

```text
handoff/antigravity/outputs/phase2e_antigravity_controlled_planning_review.md
```

It reports:

- local Git repository status and remotes
- active mission and registry attempt status
- adapter modes and execution capability
- current validation, review, and Owner Gate state
- expected handoff output paths

## DNA Production Runtime v0.5

v0.5 is the first operational Corpus-to-Creation runtime layer. It converts
structured research derivatives into a DNA Registry, builds a metadata-only
Research RAG Index, and manages manual Antigravity review jobs through a
file-backed queue.

Build and inspect the DNA mother-library:

```bash
python3 system/runtime/nrl.py dna-registry-build
python3 system/runtime/nrl.py dna-registry
```

Build and inspect the structured retrieval index:

```bash
python3 system/runtime/nrl.py rag-index-build
python3 system/runtime/nrl.py rag-index
```

Create the first production job for the current missing asset family:

```bash
python3 system/runtime/nrl.py agent-job-plan --family techniques
python3 system/runtime/nrl.py agent-pack --job-id job-v05-techniques-antigravity-review
python3 system/runtime/nrl.py agent-jobs
```

Manual Antigravity output must be placed under:

```text
system/agent_ops/inbox/
```

Then ingest and validate it:

```bash
python3 system/runtime/nrl.py agent-ingest --job-id job-v05-techniques-antigravity-review --file system/agent_ops/inbox/job-v05-techniques-antigravity-review.md
python3 system/runtime/nrl.py agent-validate --job-id job-v05-techniques-antigravity-review
```

Inspect the complete production runtime status:

```bash
python3 system/runtime/nrl.py production-runtime-status
```

This runtime still does not call Antigravity or Hermes. It only creates the
shared-folder contract, validates returned artifacts, and keeps Owner Gate
active before any prose or final creative asset generation.

## Technique Asset Producer v0.6

v0.6 connects the validated techniques review to the first seed-level creation
asset producer. It writes schema-bound technique candidates into the project
asset store, not final technique trees.

Inspect producer readiness:

```bash
python3 system/runtime/nrl.py producer-status
```

Produce the current seed technique candidates:

```bash
python3 system/runtime/nrl.py produce-techniques --job-id job-v05-techniques-antigravity-review
```

Validate the project asset store after production:

```bash
python3 system/runtime/nrl.py validate-creation-assets
```

The producer remains bounded:

- no prose
- no combat scenes
- no final technique tree
- no Hermes execution
- no automatic Antigravity execution
- no raw `novel_training_set/` reads
- current blocked actions
- recommended next runtime command

The smoke-test path is covered by `tests/test_sys3_runtime.py` and verifies:

1. Antigravity handoff preparation records a handoff attempt.
2. A manually produced expected output can be ingested.
3. Ingest moves the mission to Owner Gate instead of bypassing review.
4. `advance` does not duplicate handoff attempts or bypass Owner Gate.
5. `advance` does not reuse stale Owner Gate decisions across gates.
6. `system-status` exposes SYSTEM_HARDENING and FROZEN_AT_OWNER_GATE.

## NRL Studio v0.1

`Novel Research Lab Studio v0.1` is the first visible product shell for the runtime. It is a local dashboard, not a content phase.

Exact commands:

```bash
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py studio-data
python3 system/runtime/nrl.py creation-assets
python3 system/runtime/nrl.py studio-build
open system/runtime/studio/index.html
```

The dashboard renders:

- System Identity
- Current Project
- Agent Panel
- Artifact Map
- Creation Coverage Matrix
- Creation Asset Registry drill-down
- Runtime Status
- Next Safe Action
- Owner Gate

The Studio build generates current runtime data, builds the React/Astryx app from `apps/studio/`, copies the static output to `system/runtime/studio/`, and injects the current data into `index.html` for offline inspection.

Studio v0.1 intentionally keeps the current Phase 2E Owner Gate pending state visible as a system-state sample. It must not progress Phase 2F, produce chapter content, call Hermes, call Antigravity, or convert manual handoff into automatic execution.

## NRL Control Plane v0.2

Control Plane v0.2 is the normal local system surface. It keeps the portable
`studio-build` snapshot, but day-to-day inspection should use the live Chinese
console:

```bash
python3 system/runtime/nrl.py studio-build
python3 system/runtime/nrl.py studio-serve --port 4173
```

Open `http://127.0.0.1:4173`.

The live console exposes only fixed local routes for Studio data, research
assets, creation schemas, `system-check`, and `validate-state`. It does not
accept arbitrary commands and does not expose `advance`, Hermes execution, or
Antigravity execution.

Control-plane commands:

```bash
python3 system/runtime/nrl.py hardening-status
python3 system/runtime/nrl.py research-assets
python3 system/runtime/nrl.py research-assets --title 遮天
python3 system/runtime/nrl.py research-assets --category 升级与境界机制
python3 system/runtime/nrl.py creation-schemas
python3 system/runtime/nrl.py validate-creation-assets
python3 system/runtime/nrl.py system-check
```

`research-assets` indexes structured Phase 1 derivatives and preserves
provenance. It does not read raw corpus files. `creation-schemas` reports the
nine Draft-07 creation asset contracts. The production project asset store is
intentionally empty until a later Owner-authorized content workflow.

## Corpus-to-Creation v0.3

Corpus-to-Creation v0.3 is the first executable pipeline layer. It does not
generate story content. It produces deterministic plans that connect reviewed
research assets to the nine creation asset contracts.

Pipeline commands:

```bash
python3 system/runtime/nrl.py pipeline-status
python3 system/runtime/nrl.py pipeline-plan --next
python3 system/runtime/nrl.py pipeline-plan --family characters
python3 system/runtime/nrl.py pipeline-plan --family techniques
python3 system/runtime/nrl.py evidence-pack --next
python3 system/runtime/nrl.py evidence-pack --next --write
python3 system/runtime/nrl.py evidence-pack-validate --next
python3 system/runtime/nrl.py evidence-pack-validate --file system/research_assets/evidence_packs/naming.v0.10.json
```

`pipeline-status` reports the stage graph, the next recommended creation asset
family, and blocked production actions. `pipeline-plan` emits a schema-bound
plan for a target family, including structured research evidence, evidence
requirements, schema path, validation gates, agent review policy, and Owner
Gate status. `evidence-pack` turns that plan into a guarded, reusable research
evidence package for the target creation asset family. With `--write`, it writes
the package under `system/research_assets/evidence_packs/` without copying raw
corpus text or generating final creative assets. `evidence-pack-validate`
actively enforces schema validity, source evidence existence, raw corpus
boundaries, current creation asset store consistency, Owner Gate, and external
agent execution boundaries before a pack can be treated as usable downstream.

The current expected next family is derived from the creation coverage matrix
by readiness score and stable family priority. At the current Phase 2E Owner
Gate state, the next family is `naming`, because naming coverage is missing and
has the lowest readiness score under the current stable ordering.

v0.3 remains read-only and infrastructure-only:

- no prose
- no chapter plan progression
- no final character cards
- no final NPC, faction, artifact, technique, naming, emotional bond,
  foreshadowing, or state ledger content
- no raw `novel_training_set/` reads
- no Hermes or Antigravity execution

## Architecture Reconciliation v0.4

Architecture Reconciliation v0.4 exposes the accepted Novel Research Lab source
architecture as a read-only runtime contract. It locks the product identity as
Corpus-to-Creation and classifies v0.3 `corpus_pipeline` as the
`planning_pipeline` layer under the full architecture, not as the whole system.

Architecture commands:

```bash
python3 system/runtime/nrl.py architecture-status
python3 system/runtime/nrl.py studio-data
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py studio-build
```

`architecture-status` returns the ten-layer architecture:

```text
corpus_layer
single_book_decomposition
cross_book_distillation
research_asset_engine
original_project_synthesis
long_form_creation_asset_os
planning_pipeline
agent_review_and_production
runtime_control_plane
studio_cockpit
```

The command also records the Core7 small-batch experiment as the accepted
calibration basis, exposes the current mismatch report, and keeps the agent
contract explicit:

- Codex: local runtime host, engineering, validation, orchestration.
- Antigravity: manual external literary review.
- Hermes: `paused_not_removed`, later writer/literary enrichment only after
  explicit Owner authorization.
- Web GPT: architecture review only, not task dispatcher.
- Owner: gate authority.

v0.4 remains read-only. It does not progress Phase 2F, call Hermes, call
Antigravity, read `novel_training_set/`, generate prose, or generate final
creative assets.

GitHub binding is intentionally outside the runtime. Bind the workspace to a confirmed repository first; then `doctor` will report repository root, branch, and remotes. Do not bind this workspace to an unrelated repository.
