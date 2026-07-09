# NRL Antigravity Full Corpus Handoff v0.7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a manual Antigravity full-corpus command packet and runtime validator so full-corpus review output can be safely ingested by NRL.

**Architecture:** Add a focused `nrl_full_corpus_handoff.py` module that owns v0.7 packet generation, status, ingestion, and validation. Wire the module into `nrl.py` with CLI commands and keep v0.5 single-family agent jobs unchanged.

**Tech Stack:** Python standard library, existing NRL runtime path helpers, `unittest`, file-backed Markdown and JSON artifacts.

## Global Constraints

- Do not call Antigravity directly.
- Do not call Hermes.
- Do not generate prose, chapters, outlines, scenes, or final creative assets.
- Do not read or quote `novel_training_set/`.
- Preserve `SYSTEM_HARDENING / FROZEN_AT_OWNER_GATE`.
- The Owner-facing command packet must be a durable file under `system/agent_ops/packets/`.

---

### Task 1: Failing Tests For v0.7 Handoff

**Files:**
- Create: `tests/test_antigravity_full_corpus_v07.py`
- Create: `tests/fixtures/agent_ops/valid_full_corpus_antigravity_review.md`

**Interfaces:**
- Produces expected CLI behavior for `antigravity-full-corpus-pack`, `antigravity-full-corpus-status`, `antigravity-full-corpus-ingest`, and `antigravity-full-corpus-validate`.

- [ ] **Step 1: Write failing CLI tests**

Create tests that assert:

- `antigravity-full-corpus-pack` writes packet and command files.
- The command packet contains Chinese instructions, the v0.4 architecture, all nine asset families, and the expected output path.
- Status reports job id `job-v07-full-corpus-antigravity-review`.
- Ingest rejects files outside `system/agent_ops/inbox`.
- Validate accepts the fixture review and rejects forbidden markers.

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_antigravity_full_corpus_v07 -v
```

Expected: FAIL because the new CLI commands do not exist.

### Task 2: Runtime Module

**Files:**
- Create: `system/runtime/nrl_full_corpus_handoff.py`

**Interfaces:**
- Produces `write_full_corpus_packet(state, adapters) -> dict`
- Produces `build_full_corpus_status(state, adapters) -> dict`
- Produces `ingest_full_corpus_output(file_arg: str) -> dict`
- Produces `validate_full_corpus_output() -> dict`

- [ ] **Step 1: Implement packet generation**

Write packet files:

- `system/agent_ops/packets/job-v07-full-corpus-antigravity-review.md`
- `system/agent_ops/packets/job-v07-full-corpus-antigravity-command.md`

The command file must be paste-ready for Antigravity.

- [ ] **Step 2: Implement status and ingestion**

Use `system/agent_ops/full_corpus_job.v0.7.json` as the durable state file. Ingest only accepts files under `system/agent_ops/inbox/`.

- [ ] **Step 3: Implement validation**

Check required headings, parse the `JSON Manifest` fenced code block, verify all nine asset families, and reject forbidden markers.

- [ ] **Step 4: Run focused tests**

Run:

```bash
python3 -m unittest tests.test_antigravity_full_corpus_v07 -v
```

Expected: PASS.

### Task 3: CLI Wiring And Docs

**Files:**
- Modify: `system/runtime/nrl.py`
- Modify: `system/runtime/README.md`

**Interfaces:**
- Adds CLI commands:
  - `antigravity-full-corpus-pack`
  - `antigravity-full-corpus-status`
  - `antigravity-full-corpus-ingest --file <path>`
  - `antigravity-full-corpus-validate`

- [ ] **Step 1: Wire commands into argparse**

Import the four v0.7 functions and add command handlers.

- [ ] **Step 2: Document exact commands**

Add the v0.7 commands and the expected Owner workflow to `system/runtime/README.md`.

- [ ] **Step 3: Run regression tests**

Run:

```bash
python3 -m unittest tests.test_antigravity_full_corpus_v07 tests.test_asset_producers_v06 tests.test_dna_production_runtime_v05 tests.test_sys3_runtime -v
```

Expected: PASS.

### Task 4: Generate Owner Packet And Verify

**Files:**
- Generated: `system/agent_ops/packets/job-v07-full-corpus-antigravity-review.md`
- Generated: `system/agent_ops/packets/job-v07-full-corpus-antigravity-command.md`
- Generated: `system/agent_ops/full_corpus_job.v0.7.json`

- [ ] **Step 1: Generate the packet**

Run:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-pack
```

Expected: JSON prints packet and command paths.

- [ ] **Step 2: Validate fixture path**

Copy fixture to inbox through the test path or run tests; do not mark fixture output as real Owner-approved production unless it is explicitly for validation.

- [ ] **Step 3: Run final checks**

Run:

```bash
python3 system/runtime/nrl.py antigravity-full-corpus-status
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py validate-state
git diff --check
```

Expected: status is stable, system remains frozen at Owner Gate, diff check is clean.

