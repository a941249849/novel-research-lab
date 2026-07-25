# NRL Evidence Pack v0.10 Independent Architecture Review

## Verdict
**ACCEPT_WITH_WARNINGS**

---

## Architectural Findings

### 1. Static Validation Gates (Medium Severity)
* **Description**: The validation gates listed in [VALIDATION_GATES](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py#L65-L72) (such as `schema_validation`, `source_evidence`, `reference_integrity`, and `naming_collision`) are currently defined as static metadata returned by [_validation_gates](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py#L164-L165). There is no active enforcement logic within the runtime Python layers of [nrl_corpus_pipeline.py](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py) to run these programmatic validations before promotion.
* **Impact**: Programmatic schema conformance, reference check failures, or name collisions are not proactively caught by the runtime execution; the pipeline relies strictly on descriptive metadata.

### 2. Missing Evidence Pack Validation and Promotion Commands (Low Severity)
* **Description**: While commands exist for full-corpus proof validation and promotion ([full-corpus-proof-validate](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_full_corpus_proof.py#L100) and [full-corpus-proof-promote](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_full_corpus_proof.py#L101)), there are no equivalent subcommands in [nrl.py](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl.py) to validate or promote an generated evidence pack (e.g., [naming.v0.10.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/research_assets/evidence_packs/naming.v0.10.json)) into active creation-stage contexts.
* **Impact**: Verification of generated packs must be manually done or handled as post-processing, limiting automation capability.

---

## Answers to Review Questions

### 1. Does `evidence-pack --next --write` correctly convert the next Corpus-to-Creation plan into a reusable research evidence package without generating prose or final creative assets?
* **Yes**. Running [cmd_evidence_pack](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl.py#L330-L341) with the `--write` flag correctly calls [write_evidence_pack](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py#L347-L356) and produces the JSON package [naming.v0.10.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/research_assets/evidence_packs/naming.v0.10.json) containing only structural research evidence paths, metadata, schemas, and gate definitions. `"content_generation_allowed"` is explicitly set to `False`.

### 2. Does the evidence package preserve the intended architecture boundary: Codex local runtime, Antigravity external review, Hermes paused until final writing authorization?
* **Yes**. The boundaries are preserved in the `agent_review_policy` structure inside [build_evidence_pack](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py#L339):
  - `codex` is set to `"local_validation_orchestration"`.
  - `antigravity` is set to `"manual_handoff"`.
  - `hermes` is set to `"paused_not_removed"`.
* Furthermore, `"execute_hermes"` and `"execute_antigravity"` are explicitly registered under `blocked_actions` to prevent unauthorized execution.

### 3. Are there any signs that this implementation reads or copies raw `novel_training_set/` content into the evidence pack?
* **No**. The system selects evidence exclusively from structured Phase 1 metadata and mechanism libraries (e.g., [core7_mechanism_inventory.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/research_assets/evidence_packs/naming.v0.10.json#L46)). Programmatic checks within [test_corpus_pipeline_v03.py](file:///Users/liuneng/Documents/Novel%20Research%20Lab/tests/test_corpus_pipeline_v03.py#L54) enforce this boundary, and `raw_corpus_allowed` is set to `False` in [evidence_requirements](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py#L324).

### 4. Are the Owner Gate and full-corpus proof promotion dependencies explicit enough to prevent accidental content progression?
* **Yes**. In the generated package [naming.v0.10.json](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/research_assets/evidence_packs/naming.v0.10.json#L303-L313), the `promotion_dependencies.full_corpus_proof` blocks promotion by setting `"promotion_allowed": false` and `"status": "blocked_on_owner_gate"`.
* Additionally, [cmd_advance](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl.py#L718) enforces that if `owner_gate_required` is `True`, execution halts with `"manual_owner_decision_required"` unless there is an authorized decision matching the active job configuration in [build_promotion_readiness](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_full_corpus_proof.py#L119).

---

## Recommended Next Engineering Step

Codex should implement **active validator classes** inside [nrl_corpus_pipeline.py](file:///Users/liuneng/Documents/Novel%20Research%20Lab/system/runtime/nrl_corpus_pipeline.py) for the programmatically defined gates:
1. Implement a Draft-07 JSON Schema validator using `jsonschema` to validate the creation asset payload during planning.
2. Add a naming collision check function verifying that normalized names in the evidence pack do not conflict with the existing project asset store.
3. Introduce a CLI subcommand: `python3 system/runtime/nrl.py evidence-pack validate --family <family>` to trigger these checks.
