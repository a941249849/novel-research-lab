# NRL Runtime Autonomy Convergence v0.13 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the installed Antigravity CLI bridge a truthful, guarded NRL Runtime adapter and close the registered-review loop without enabling prose generation or bypassing Owner Gate.

**Architecture:** Keep `agent_adapters.json` as the declared adapter registry, but derive effective Antigravity readiness from the live `agy --version` probe. Add one reusable execution-status contract and one allowlisted `agent-dispatch` command; dispatch writes only controlled request/response artifacts and leaves validation and promotion as explicit later commands.

**Tech Stack:** Python 3 standard library, existing `unittest` suite, file-backed JSON job queue, existing `agy` CLI bridge, Vite + React + Astryx Studio.

## Global Constraints

- Antigravity is `cli_bridge` only when `agy --version` succeeds.
- Dispatch is limited to registered `antigravity_structural_review` jobs.
- A bridge response is `output_received`, never automatically `validated` or `promoted`.
- No Phase 2F advance, prose, final creative asset, Hermes execution, or Studio execute button.
- No raw `novel_training_set/` prose reads or paths in normal Runtime payloads.
- Existing `current_phase_state.json`, `mission_registry.json`, and `agent_adapters.json` remain source-of-truth files.
- Existing 18 full-corpus response files remain evidence candidates and are not automatically promoted.

## File Structure

- Modify `system/runtime/nrl_antigravity_bridge.py`: derive reusable effective execution status.
- Modify `system/runtime/agent_adapters.json`: declare the installed CLI bridge and its allowlist.
- Modify `system/runtime/nrl_agent_ops.py`: implement guarded dispatch and queue transitions.
- Modify `system/runtime/nrl.py`: expose `agent-dispatch` and wire status helpers.
- Modify `system/runtime/nrl_system_status.py` and `system/runtime/nrl_architecture.py`: expose truthful role/state data.
- Modify `system/runtime/nrl_studio_data.py`, `apps/studio/src/types.ts`, and `apps/studio/src/App.tsx`: expose the connected CLI collaboration state in Chinese.
- Modify `system/runtime/README.md`: document the controlled dispatch boundary.
- Modify `tests/test_antigravity_bridge_v08.py`, `tests/test_dna_production_runtime_v05.py`, and create `tests/test_agent_dispatch_v013.py` for red/green coverage.

### Task 1: Converge Antigravity Capability State

**Interfaces:**

- Produce `build_antigravity_execution_status(adapters: dict[str, Any]) -> dict[str, Any]`.
- Return `declared_mode`, `bridge_available`, `effective_state`, `can_dispatch_registered_reviews`, `blocked_reason`, and `allowed_job_types`.
- Keep `build_antigravity_bridge_status()` as the live binary probe.

- [ ] Write failing tests for `cli_bridge / ready`, missing binary, and stale `manual_handoff`.
- [ ] Run `python3 -m unittest tests.test_antigravity_bridge_v08 -v` and confirm the new expectations fail against the old adapter state.
- [ ] Add the execution-status helper and update the Antigravity adapter declaration.
- [ ] Update system status and architecture role payloads to consume the helper.
- [ ] Run the bridge and status tests until green.

### Task 2: Add Guarded Registered-Job Dispatch

**Interfaces:**

- Produce `dispatch_agent_job(job_id: str, print_timeout: str = "5m0s") -> dict[str, Any]`.
- Produce CLI `python3 system/runtime/nrl.py agent-dispatch --job-id <job-id>`.
- Allowed transition: `ready_for_antigravity -> external_running -> output_received`.
- Failure transition: bridge failure or empty output -> `blocked` with no validation/promotion.

- [ ] Create `tests/test_agent_dispatch_v013.py` with a fake `agy` fixture and tests for valid dispatch, invalid job state, invalid owner/type, missing packet, raw-corpus packet, bridge failure, and empty output.
- [ ] Run the focused dispatch test and confirm it fails because the command and function do not exist.
- [ ] Implement packet validation, controlled request copy, exact inbox output path, queue updates, and bridge log metadata in `nrl_agent_ops.py`.
- [ ] Add the CLI parser and command handler in `nrl.py`.
- [ ] Run the focused dispatch tests and verify no state mutation occurs on rejected jobs.

### Task 3: Align Runtime, Studio, and Documentation

**Interfaces:**

- Add `antigravity_execution` to production runtime and Studio data.
- Replace stale display text with `CLI 协作文学审查` and effective states such as `ready`, `blocked_bridge_unavailable`, and `output_received`.
- Preserve read-only Studio controls and existing forbidden actions.

- [ ] Add failing assertions for system status, production runtime, Studio data, built HTML, and README command coverage.
- [ ] Run the focused integration tests to verify the assertions fail on stale data.
- [ ] Update Python payload builders, TypeScript types, and the Antigravity panel copy.
- [ ] Update README with `agent-dispatch` and explicit validation/promotion sequencing.
- [ ] Build Studio and run Astryx doctor.

### Task 4: Full Verification and Delivery

- [ ] Run the bridge, dispatch, production runtime, corpus pipeline, proof gate, control plane, architecture, and SYS-3 test suites.
- [ ] Run `validate-state`, `system-check`, `studio-build`, `npm run build`, `npx astryx doctor`, and `git diff --check`.
- [ ] Confirm no Hermes call, no prose output, no raw corpus path in new Runtime payloads, and Owner Gate remains frozen.
- [ ] Review the diff, commit the v0.13 implementation, and push the current branch.
