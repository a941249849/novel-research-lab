# Provider-Aware Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make model-provider routing and evidence quality resilient across quota windows.

**Architecture:** A common runner executes bounded packets through either provider. An append-only ledger records only metadata. Book synthesis gains claim-level source anchors without invalidating existing chunk responses.

**Tech Stack:** Python standard library, unittest, existing NRL runtime.

## Global Constraints

- Existing valid v0.18 evidence remains valid and immutable.
- All provider output remains subject to existing schema validation.
- No prose generation.

### Task 1: Provider Dispatch
- [ ] Add failing tests for provider selection, local timeout, and classified failure metadata.
- [ ] Implement the common runner and metadata ledger.
- [ ] Add OpenCode Go support to synthesis, cross-book, and reconciliation dispatch.

### Task 2: Evidence Quality
- [ ] Add failing synthesis validation tests requiring per-claim chunk and chapter anchors.
- [ ] Implement anchor validation against validated chunk metadata.

### Task 3: Verification
- [ ] Run focused tests, full runtime tests, `validate-state`, and `git diff --check`.
