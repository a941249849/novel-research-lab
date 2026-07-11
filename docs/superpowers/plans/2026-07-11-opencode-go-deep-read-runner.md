# OpenCode Go Deep-Read Runner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a validator-gated OpenCode Go worker to v0.18 corpus deep reading.

**Architecture:** Keep the current `agy` path intact and introduce a runner selector. The OpenCode path executes the existing packet, extracts only the bound JSON object from command output, and delegates all acceptance to `validate_chunk_response`.

**Tech Stack:** Python 3 standard library, existing unittest suite, installed OpenCode CLI.

## Global Constraints

- Credentials stay in the user OpenCode credential store and never enter the repository.
- The existing v0.18 response validator remains the sole acceptance authority.
- Default behavior stays `agy` for backward compatibility.

---

### Task 1: Bound JSON extraction

**Files:**
- Modify: `tests/test_verifiable_deep_reading_v018.py`
- Modify: `system/runtime/nrl_deep_read.py`

- [ ] Add a failing unit test with a transcript containing tool logs, two JSON objects, and one matching `chunk_id`; require extraction of only the matching object.
- [ ] Run `python3 -m unittest tests.test_verifiable_deep_reading_v018 -q` and confirm the import/function failure.
- [ ] Implement a standard-library JSON decoder scan that returns the unique matching response object and rejects no-match or ambiguous match output.
- [ ] Re-run the focused test suite.

### Task 2: OpenCode runner

**Files:**
- Modify: `system/runtime/nrl_deep_read.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_verifiable_deep_reading_v018.py`

- [ ] Add a failing CLI parser test for `--runner opencode-go --variant max`.
- [ ] Add the runner selector and invoke `opencode run --model opencode-go/<model> --variant <variant>` with the existing packet as prompt.
- [ ] Write only extracted bound JSON to the planned response path and run the unchanged validator.
- [ ] Keep `agy` as the default and reject unknown runners.
- [ ] Run focused tests, then the full runtime suite and `git diff --check`.
