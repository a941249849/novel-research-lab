# NRL Hermes Controlled Prose v0.16 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans for inline delivery. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a guarded Hermes CLI bridge and run one validated prose test.

**Architecture:** A dedicated bridge executes Hermes in output-only mode from an allowlisted context packet. A separate runtime module enforces the Owner decision and Antigravity verdict before invoking it, then validates the captured prose before it becomes an artifact.

**Tech Stack:** Python 3, unittest, Hermes CLI.

## Global Constraints

- Use `openai-codex` with `gpt-5.6-terra`.
- Never pass or read `novel_training_set/`.
- Accept one bounded scene only; never produce a chapter or serial text.
- Codex writes the inbox artifact; Hermes returns stdout only.

---

### Task 1: Hermes capability and Owner gate

**Files:**
- Create: `system/runtime/nrl_hermes_bridge.py`
- Modify: `system/runtime/nrl_owner_gate.py`, `system/runtime/nrl_system_status.py`
- Test: `tests/test_hermes_controlled_prose_v016.py`

- [x] Write failing tests for a configured Hermes CLI bridge and matching prose-test decision.
- [x] Run focused tests and confirm failure.
- [x] Implement capability detection and gate lookup.
- [x] Run focused tests and confirm pass.

### Task 2: Controlled packet, dispatch, and validation

**Files:**
- Create: `system/runtime/nrl_hermes_controlled_prose.py`
- Modify: `system/runtime/nrl.py`, `system/runtime/agent_adapters.json`
- Test: `tests/test_hermes_controlled_prose_v016.py`

- [x] Write failing tests for allowed context, output capture, and prose boundaries.
- [x] Run focused tests and confirm failure.
- [x] Implement dispatch and deterministic validation.
- [x] Run focused tests and confirm pass.

### Task 3: Independent audit and real test

**Files:**
- Create: `system/agent_ops/packets/antigravity-final-assets-audit-v016.md`
- Create: `system/agent_ops/inbox/antigravity-final-assets-audit-v016.md`
- Create: `system/agent_ops/packets/hermes-controlled-prose-test-v016.md`
- Create: `system/agent_ops/inbox/hermes-controlled-prose-test-v016.md`

- [x] Validate the Antigravity verdict.
- [x] Record the bounded Owner decision and dispatch the Hermes test.
- [x] Validate output, run runtime tests, build Studio, and commit the bounded artifacts.
