# Novel Research Lab Runtime MVP

## What This Runtime Does

`system/runtime/nrl.py` is a minimal local Mission Runtime. It can:

- Read `system/mission_controller/current_phase_state.json`.
- Report current status and the next recommended mission.
- Prepare bounded handoff task files and dispatch registered Antigravity review jobs through the local CLI bridge.
- Register externally produced Hermes or Antigravity outputs.
- Update Mission Controller state after ingest.
- Validate current phase state against `phase_state.schema.json`.

## What This Runtime Does Not Do

- It does not call Hermes.
- It does not operate the Antigravity GUI.
- It can call Antigravity CLI only for registered structural-review jobs through the guarded `agent-dispatch` command.
- It does not generate novel prose.
- It does not generate first chapters.
- It does not generate Outline Trees by itself unless Codex is explicitly tasked outside this runtime.
- It does not read `novel_training_set/`.
- It does not replace Codex validation, Antigravity review, or Owner Gate.

## Why Hermes Remains Manual And Antigravity Is Guarded

No Hermes CLI/API adapter is currently configured. Antigravity has a local CLI
bridge, but its Runtime adapter is restricted to registered review jobs. The
runtime therefore uses:

- Hermes adapter: `manual_handoff`
- Antigravity adapter: `cli_bridge`
- Codex adapter: `local`

Antigravity dispatch copies the registered packet, calls `agy -p`, captures the
response in the controlled inbox, and leaves validation and promotion as
explicit later commands.

The effective state is checked with `agy --version` at runtime. If the bridge is
unavailable, dispatch is blocked without changing the job state.

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

Dispatch a registered structural-review job through the CLI bridge:

```bash
python3 system/runtime/nrl.py agent-dispatch --job-id <job-id>
```

Dispatch only produces `output_received`. Validate it explicitly with
`agent-validate`; dispatch never promotes an asset, advances a phase, or calls
Hermes.

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

## Antigravity CLI Bridge Adapter

The configured Antigravity adapter uses `cli_bridge` with:

- `mode`: `cli_bridge`
- registered review-job allowlist
- handoff input file
- expected review report path
- status mapping for pass, warnings, hold, or fail

The runtime must not mark review complete until a report artifact is ingested and registered.

## Antigravity Full Corpus Handoff v0.7

Use this when the architecture is frozen and the Owner wants Antigravity to
perform full-corpus rereading, reanalysis, and replanning. This remains an
Owner-gated full-corpus workflow; the CLI bridge does not automatically promote
its candidate outputs.

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

SYS-3 keeps Codex / NRL as the local runtime host. Hermes remains paused;
Antigravity is a guarded local CLI adapter and can dispatch only registered
structural-review jobs.

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

Studio is a read-only cockpit plus command launcher. It must not maintain independent project state. It reads `current_phase_state.json`, `mission_registry.json`, and `agent_adapters.json`; it does not call Hermes, does not dispatch Antigravity, does not generate novel prose, and does not read `novel_training_set/`.

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
Research RAG Index, and manages registered Antigravity review jobs through a
file-backed queue and the guarded CLI bridge.

Build and inspect the DNA mother-library:

```bash
python3 system/runtime/nrl.py dna-registry-build
python3 system/runtime/nrl.py dna-registry
```

Build and inspect the structured retrieval index:

```bash
python3 system/runtime/nrl.py rag-index-build
python3 system/runtime/nrl.py rag-index
python3 system/runtime/nrl.py creation-context-index-build
python3 system/runtime/nrl.py creation-context-index
```

`creation-context-index` expands the guarded evidence-pack matrix into a
metadata-only context index for downstream Story Bible and Hermes handoff
preparation. It remains content-frozen: no prose, no final creative assets, and
no Hermes execution.

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

This runtime calls Antigravity only through the guarded `agent-dispatch`
command. It validates returned artifacts and keeps Owner Gate active before
any prose or final creative asset generation. Hermes remains paused.

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
- no Antigravity dispatch from Studio
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

Studio v0.1 intentionally keeps the current Phase 2E Owner Gate pending state visible as a system-state sample. It must not progress Phase 2F, produce chapter content, call Hermes, or dispatch Antigravity jobs; Codex Runtime remains the only dispatch surface.

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
nine Draft-07 creation asset contracts. The project asset store may contain
schema-bound seed contracts after the research promotion gate; these are not
final creative assets and do not authorize prose generation.

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
python3 system/runtime/nrl.py evidence-pack-validate --all
python3 system/runtime/nrl.py evidence-pack-matrix --write
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
`evidence-pack-matrix --write` materializes guarded evidence packages for all
nine creation asset families and writes
`system/research_assets/evidence_packs/manifest.v0.11.json` as the all-family
input manifest for downstream Corpus-to-Creation planning.

The current expected next family is derived from the creation coverage matrix
by readiness score and stable family priority. It is a refinement candidate,
not a permission to generate final content. When all nine schema-bound seed
contracts exist, `pipeline-status` reports
`creation_contract_seed_matrix_ready: true` and changes `next_safe_action` to
`hermes-readiness`; the final asset and writing gate remains with the Owner.

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
- Antigravity: guarded CLI collaborative literary review for registered jobs.
- Hermes: `paused_not_removed`, later writer/literary enrichment only after
  explicit Owner authorization.
- Web GPT: architecture review only, not task dispatcher.
- Owner: gate authority.

v0.4 remains read-only. It does not progress Phase 2F, call Hermes, dispatch
Antigravity from Studio, read `novel_training_set/`, generate prose, or generate
final creative assets.

## Corpus Review Ingestion v0.14

After the full-corpus proof and the explicit research-promotion decision, the
validated Antigravity review can be ingested into structured research assets:

```bash
python3 system/runtime/nrl.py full-corpus-proof-promote
python3 system/runtime/nrl.py full-corpus-review-ingest
python3 system/runtime/nrl.py evidence-pack-matrix --write
python3 system/runtime/nrl.py creation-context-index-build
```

The promoted research artifact records 18 book reviews, cross-book mechanisms,
and nine creation-family evidence sets. It contains no raw novel text and is
not a training set. The nine seed producers then establish contract coverage:

```bash
python3 system/runtime/nrl.py produce-naming-seed --job-id job-v05-naming-antigravity-review
python3 system/runtime/nrl.py produce-npc-seed --job-id job-v05-npcs-antigravity-review
python3 system/runtime/nrl.py produce-artifact-seed --job-id job-v05-artifacts-antigravity-review
python3 system/runtime/nrl.py produce-state-ledger-seed --job-id job-v05-state_ledger-antigravity-review
python3 system/runtime/nrl.py produce-emotional-bond-seed --job-id job-v05-emotional_bonds-antigravity-review
python3 system/runtime/nrl.py produce-foreshadowing-seed --job-id job-v05-foreshadowing-antigravity-review
python3 system/runtime/nrl.py produce-character-seed --job-id job-v05-characters-antigravity-review
python3 system/runtime/nrl.py produce-faction-seed --job-id job-v05-factions-antigravity-review
python3 system/runtime/nrl.py produce-techniques --job-id job-v05-techniques-antigravity-review
```

Check the final handoff boundary:

```bash
python3 system/runtime/nrl.py hermes-readiness
```

Validate and promote a Hermes final-asset bundle through the controlled inbox:

```bash
python3 system/runtime/nrl.py final-assets-validate --file system/agent_ops/inbox/hermes-final-asset-bundle-v015.json
python3 system/runtime/nrl.py final-assets-promote --file system/agent_ops/inbox/hermes-final-asset-bundle-v015.json
```

The v0.15 promotion preserves all seed assets, requires the matching Owner
decision, records the candidate SHA-256, and is idempotent once promoted. The
current expected state after promotion is
`final_assets_promoted_awaiting_prose_owner_gate` with
`ready_to_call_hermes: false`: final creation assets are available, but novel
prose still requires a separate bounded Owner authorization.

After an independent final-asset review, Hermes can run one controlled prose
test through the Codex OAuth bridge. This is not chapter or serial production:

```bash
python3 system/runtime/nrl.py hermes-bridge-status
python3 system/runtime/nrl.py controlled-prose-status
python3 system/runtime/nrl.py controlled-prose-test
python3 system/runtime/nrl.py controlled-prose-validate --file system/agent_ops/inbox/hermes-controlled-prose-test-v016.md
```

The bridge pins `openai-codex` and `gpt-5.6-terra`, captures Hermes stdout in a
controlled inbox file, and rejects output outside the one-scene character
range, story anchors, and reader-facing jargon boundary. A passing test is a
style benchmark only; full chapters and serial prose remain blocked.

## Verifiable deep reading v0.18

The historical v0.8 proof verifies source-file identity and four sampled byte
ranges. It is retained as `access_sample_verified` evidence and must not be
described as proof that every corpus byte was deeply read.

The v0.18 pipeline creates contiguous bounded files under the Git-ignored
`.nrl-work/` directory. Every corpus byte belongs to exactly one chunk, every
Antigravity response is hash-bound to that chunk, and per-book plus cross-book
synthesis gates are required before `deep_read_verified`.

```bash
python3 system/runtime/nrl.py deep-read-plan --target-bytes 1500000
python3 system/runtime/nrl.py deep-read-status
python3 system/runtime/nrl.py deep-read-dispatch --workers 2 --model "Gemini 3.5 Flash (High)"
python3 system/runtime/nrl.py deep-read-validate-all
python3 system/runtime/nrl.py deep-read-synthesis-pack
python3 system/runtime/nrl.py deep-read-synthesis-dispatch --workers 2
python3 system/runtime/nrl.py deep-read-synthesis-validate
python3 system/runtime/nrl.py deep-read-cross-pack
python3 system/runtime/nrl.py deep-read-cross-dispatch
python3 system/runtime/nrl.py deep-read-cross-validate
```

Antigravity quota failures and empty responses never count toward coverage.
All dispatch commands are resumable and retry only missing or invalid outputs.
Hermes serial prose remains blocked until v0.18, project impact review, and
creation-asset validation complete.

## Production chapter runtime v0.20

The chapter runtime is an ordered, artifact-backed state machine. It does not
create prose until corpus depth and project reconciliation gates pass.

```bash
python3 system/runtime/nrl.py project-reconciliation-pack
python3 system/runtime/nrl.py project-reconciliation-dispatch
python3 system/runtime/nrl.py project-reconciliation-validate
python3 system/runtime/nrl.py project-reconciliation-apply
python3 system/runtime/nrl.py production-readiness
python3 system/runtime/nrl.py chapter-runtime-status
python3 system/runtime/nrl.py prose-metrics --file <draft-or-revision.md>
```

The nine stages are chapter intent, context compilation, draft generation,
fact observation, draft continuity audit, revision, revision audit, state
settlement, and acceptance. Normal bounded execution uses `chapter-init`,
`chapter-compile`, `chapter-draft`, `chapter-observe`, `chapter-audit`,
`chapter-revise`, `chapter-audit`, `chapter-settle`, and `chapter-accept`.
Reconciliation application requires a matching Owner decision bound to the
validated response SHA-256. Chapter settlement accepts only state deltas that
match schema-valid observed facts.
Accepted chapters are immutable; later corrections create explicit revision and
settlement artifacts rather than rewriting history silently.

GitHub binding is intentionally outside the runtime. Bind the workspace to a confirmed repository first; then `doctor` will report repository root, branch, and remotes. Do not bind this workspace to an unrelated repository.
