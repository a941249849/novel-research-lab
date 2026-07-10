# NRL Final Asset Promotion v0.15 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans (inline execution authorized by the Owner) task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Validate and promote one Hermes final-asset bundle without permitting prose generation.

**Architecture:** A focused runtime module validates the candidate before it can touch the creation store. Promotion uses the existing Owner decision and schema validator, then writes an immutable provenance manifest alongside the merged store.

**Tech Stack:** Python 3, Draft-07 JSON Schema, unittest.

## Global Constraints

- Accept only the v0.15 controlled inbox candidate.
- Require exactly nine active creation families and new asset IDs.
- Keep raw corpus reads and all prose generation forbidden.
- Preserve existing seed assets and use atomic local JSON writes.

---

### Task 1: Candidate validator

**Files:**
- Create: `system/runtime/nrl_final_assets.py`
- Create: `tests/test_final_asset_promotion_v015.py`

**Interfaces:**
- Produces `validate_final_asset_payload(bundle, store)` and `validate_final_asset_bundle(file_arg)`.

- [x] **Step 1: Write failing validator tests** for exact family coverage, safe provenance, and combined schema validation.
- [x] **Step 2: Run the focused tests** and confirm import failure before implementation.
- [x] **Step 3: Implement the validator** with explicit candidate and store checks.
- [x] **Step 4: Run the focused tests** and confirm they pass.

### Task 2: Promotion gate and CLI

**Files:**
- Modify: `system/runtime/nrl_final_assets.py`
- Modify: `system/runtime/nrl.py`
- Modify: `tests/test_final_asset_promotion_v015.py`

**Interfaces:**
- Produces `promote_final_asset_bundle(file_arg)` and the `final-assets-validate` / `final-assets-promote` commands.

- [x] **Step 1: Write failing tests** for Owner-decision enforcement and promotion provenance.
- [x] **Step 2: Run focused tests** and confirm failure.
- [x] **Step 3: Implement atomic promotion and CLI wiring.**
- [x] **Step 4: Run focused tests** and confirm they pass.

### Task 3: Verify the Hermes bundle

**Files:**
- Modify: `system/creation_assets/project_assets.v0.2.json`
- Create: `system/creation_assets/promotions/hermes_final_asset_bundle_v0.15.json`

- [x] **Step 1: Validate the controlled candidate with the public CLI.**
- [x] **Step 2: Promote it with the public CLI.**
- [x] **Step 3: Run creation-store, runtime, full Python, and whitespace verification.**
