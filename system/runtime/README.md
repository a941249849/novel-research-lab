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
- It does not call Antigravity.
- It does not generate novel prose.
- It does not generate first chapters.
- It does not generate Outline Trees by itself unless Codex is explicitly tasked outside this runtime.
- It does not read `novel_training_set/`.
- It does not replace Codex validation, Antigravity review, or Owner Gate.

## Why Hermes And Antigravity Use Manual Handoff

No Hermes or Antigravity CLI/API adapter is currently configured. The runtime therefore uses:

- Hermes adapter: `manual_handoff`
- Antigravity adapter: `manual_handoff`
- Codex adapter: `local`

Manual handoff means the runtime writes a task file, waits for an external human-run or tool-run agent output, then ingests that output path.

## Commands

Show current Mission Controller state:

```bash
python3 system/runtime/nrl.py status
```

Run the runtime health check:

```bash
python3 system/runtime/nrl.py doctor
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
python3 system/runtime/nrl.py studio-build
```

Studio is a read-only cockpit plus command launcher. It must not maintain independent project state.

`client_handoff` is a staging mode, not API execution. If a client cannot be automated, the runtime falls back to manual handoff while preserving task packet, expected output path, and ingest command.

## SYS-4 Doctor And Smoke Harness

Use `doctor` as the first local check before moving a mission forward:

```bash
python3 system/runtime/nrl.py doctor
```

It reports:

- local Git repository status and remotes
- active mission and registry attempt status
- adapter modes and execution capability
- current validation, review, and Owner Gate state
- expected handoff output paths
- current blocked actions
- recommended next runtime command

The smoke-test path is covered by `tests/test_sys3_runtime.py` and verifies:

1. Antigravity handoff preparation records a handoff attempt.
2. A manually produced expected output can be ingested.
3. Ingest moves the mission to Owner Gate instead of bypassing review.

GitHub binding is intentionally outside the runtime. Bind the workspace to a confirmed repository first; then `doctor` will report repository root, branch, and remotes. Do not bind this workspace to an unrelated repository.
