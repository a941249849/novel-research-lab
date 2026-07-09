# NRL Full-Corpus Proof Gate v0.8 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a proof gate that prevents schema-valid full-corpus reports from being promoted unless all corpus files have verifiable reading receipts.

**Architecture:** Keep v0.7 handoff validation intact as structural validation. Add a separate v0.8 module and CLI commands for corpus inventory, per-book Antigravity request generation, and receipt verification.

**Tech Stack:** Python standard library, `unittest`, existing `system/runtime/nrl.py` CLI.

## Global Constraints

- No raw novel prose is copied into generated proof artifacts.
- Hermes remains paused.
- Owner Gate remains active.
- v0.8 proof verification is required before full-corpus output can be treated as promotable research material.

---

### Task 1: Failing Tests

**Files:**
- Create: `tests/test_full_corpus_proof_gate_v08.py`

- [x] Write tests for status, no-receipt rejection, valid receipt acceptance, missing phase rejection, and per-book packet generation.
- [x] Run: `python3 -m unittest tests.test_full_corpus_proof_gate_v08 -v`
- [x] Expected: fail because CLI commands do not exist.

### Task 2: Runtime Module

**Files:**
- Create: `system/runtime/nrl_full_corpus_proof.py`
- Modify: `system/runtime/nrl.py`

- [x] Implement corpus inventory from `novel_training_set/*.txt`.
- [x] Implement manifest extraction and receipt validation.
- [x] Implement per-book Antigravity proof request packet generation.
- [x] Wire CLI commands.

### Task 3: Verification

**Files:**
- Test: `tests/test_full_corpus_proof_gate_v08.py`

- [x] Run focused tests.
- [x] Run existing Antigravity/full-corpus/runtime regression tests.
- [x] Validate current real v0.7 output is `schema_valid_but_depth_unverified`.
- [ ] Run `git diff --check`.
