# Hermes Input Manifest

- phase: Phase 2B
- prepared_by: Codex
- timestamp: 2026-07-08 16:26:58 CST
- status: INPUT_LOCKED

## 1. Allowed Hermes Inputs

Hermes may read only the following inputs for Phase 2B:

1. `phase1D/05_constraint_pack/grand_synthesis_constraint_pack.md`
   - Role: main creative constraint pack
   - Status: required

2. `phase1D/05_constraint_pack/hermes_phase2B_grand_synthesis_prompt.md`
   - Role: execution prompt and output format contract
   - Status: required

3. Compressed summary of `phase1D/02_corpus_synthesis/authorial_craft_distillation_index.md`
   - Role: condensed craft heuristics only
   - Status: allowed only as compressed summary, not as unrestricted full-context expansion

## 2. Forbidden Hermes Inputs

Hermes must not read:

- the 18 single-book deep reading reports in full
- all historical review reports
- raw source text under `novel_training_set/`
- Phase 2A undecided candidates
- any raw novel training-set prose excerpt
- Phase 1 JSON assets as creative source material unless separately authorized
- Phase 0B schema files as creative prompts

## 3. Input Rationale

The Phase 1D Final Gate explicitly warns against feeding all 18 book reports into Hermes. Phase 2B therefore uses a high-density constraint pack plus a controlled prompt, not a broad document dump.

## 4. Lock Rule

If Hermes execution requires any input outside this manifest, execution must stop and return for Owner approval.
