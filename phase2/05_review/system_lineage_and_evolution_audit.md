# System Lineage & Evolution Audit

- phase: Phase 2A-2R.1
- task_name: System Lineage & Evolution Audit
- generated_at: 2026-07-08
- executor: Codex
- status: PASS
- scope: system source lineage, evolution, correction record

## 1. Audit Boundary

This audit records system lineage and evolution only.

It does not:

- call Hermes
- generate new project candidates
- write novel prose
- start 18-book full extraction
- modify `phase0B`
- modify Phase 1 formal assets

Primary inputs reviewed:

- `phase0C_original_vision_reconciliation/00_original_vision_summary.md`
- `phase0C_original_vision_reconciliation/01_current_phase0B_phase1_mapping.md`
- `phase0C_original_vision_reconciliation/02_missing_capabilities_gap.md`
- `phase0C_original_vision_reconciliation/03_revised_engineering_blueprint.md`
- `phase0C_original_vision_reconciliation/04_v1_v15_v2_roadmap.md`
- `phase0C_original_vision_reconciliation/05_antigravity_execution_status_note.md`
- `system_master_spec_v0.1.md`
- `phase0B/04_agent_role_contract.md`
- `phase0B/05_skill_catalog_v1.md`
- Phase 1 / Phase 2 key review reports
- `phase2/01_original_design/02_grand_synthesis/phase2A_2R_grand_synthesis_brief.md`
- `phase2/01_original_design/02_grand_synthesis/creative_space_generation_policy.md`
- `phase2/05_review/phase2A_2R_grand_synthesis_review.md`

Note: `system_master_spec_v0.1.md` explicitly records "two deep industry research reports" as original inspiration, but this audit did not locate those two original report files by filename in the current local input set. They are therefore recorded as acknowledged lineage sources, not as independently re-reviewed source documents.

## 2. Original Lineage Sources

Novel Research Lab did not originate as a narrow YAML candidate generator. Its lineage is a combined writing-system research stack:

| Original source | Lineage role | Current system influence |
|---|---|---|
| GitHub writing Agent / Skill systems | Showed that writing can be decomposed into callable roles and skills rather than a single prompt | `phase0B/04_agent_role_contract.md`; `phase0B/05_skill_catalog_v1.md`; Codex / Hermes / Antigravity role split |
| InkOS / writing Skill engineering thought | Reinforced local-file, skill-driven, resumable writing infrastructure | CLI pipeline, physical phase directories, schema-bound skills, local reports, Drive sync discipline |
| Story Bible / World Building | Inspired persistent world, character, faction, and law-of-world containers | BookDNA, world_lore, level_system, later v1.5 tree World Bible target |
| Tree of Outlines / Recursive Plot Expansion | Inspired top-down outline to fine-outline to chapter expansion | NarrativeDNA, planning layer, future rolling long-form outline engine |
| State Machine / True-Public Ledger | Inspired state consistency and hidden/public identity tracking | StateLedger, `true_profile`, `public_mask`, inventory, faction reputation, DoubleTrackLedgerValidator |
| Draft-Review-Rewrite / Critic Loop | Inspired multi-agent critique and revision cycles | v1.5 Draft-Critic loop, Antigravity review gates, originality review process |
| Two deep research reports | Established market/system diagnosis: existing systems over-rely on one-shot prompting and weak persistence | System Master Spec's "Original Master Vision"; roadmap emphasis on persistent memory, audit, orchestration |
| Chinese web-novel training set | Provided first research domain and mechanism evidence base | scanner, skeleton extractor, manifest, Core7 extraction, mechanism inventory, category manifest |

## 3. Module Impact Map

### Research Layer

Lineage:

- Chinese web-novel training set
- GitHub / Skill-style extraction workflow
- local CLI engineering discipline

Current modules:

- `scripts/scan_novels.py`
- `scripts/extract_skeletons.py`
- `phase1/00_manifest/novel_manifest.csv`
- `phase1/01_skeletons/`

Evolution:

- Phase 1A scanned and sliced 18 local novels for controlled engineering validation.
- Phase 1B promoted only Core7 formal assets.
- The remaining 11 books remain stub assets and are explicitly barred from formal mechanism-source use.

### Knowledge Base Layer

Lineage:

- Story Bible / World Building
- Character Bible
- World Bible

Current modules:

- BookDNA
- NarrativeDNA
- StateLedger
- Core7 formal JSON assets

Evolution:

- v1 simplified the full Bible system into flat schemas.
- v1.5 keeps the tree World Bible, dynamic relation graph, and richer character/faction structures as later work.

### Mechanism Library Layer

Lineage:

- mechanism abstraction from classic works
- originality transformer thought
- market/time validated web-novel patterns

Current modules:

- `phase1/04_mechanism_library/core7_mechanism_inventory.json`
- `phase1/04_mechanism_library/category_manifest.json`
- Core7 mechanism notes
- cross-book feature notes

Evolution:

- Phase 1B converted Core7 extraction into 35 formal mechanisms across 9 categories.
- Phase 2A initially over-constrained the creative step through mechanism recipes.
- Phase 2A-2R corrected this by defining mechanism library as fuel, not menu.

### Planning Layer

Lineage:

- Tree of Outlines
- Recursive Plot Expansion
- long-form web-novel pacing research

Current modules:

- NarrativeDNA
- Phase 2A design brief
- Phase 2A-2R Grand Synthesis brief
- Creative Space Generation Policy

Evolution:

- v1 supports structured outline and candidate-level planning.
- v2 must support rolling multi-volume outline expansion and long-form continuity.

### State Tracking Layer

Lineage:

- State Machine
- True/Public Ledger
- hidden identity / public mask design

Current modules:

- StateLedger schema
- `DoubleTrackLedgerValidator`
- public mask / true profile / inventory / faction reputation fields

Evolution:

- v1 static ledger validation has landed.
- v1.5/v2 need temporal logic, multi-mask isolation, and long-term state inheritance across chapters.

### Writing / Revision Layer

Lineage:

- Draft-Review-Rewrite
- Critic Loop
- writing skill systems

Current modules:

- Hermes creative role definition
- ChapterDraftGenerator skill definition
- review gates

Evolution:

- v1 defines first-chapter generation, but Phase 2 has not authorized prose generation.
- v1.5 owns the Draft-Critic revision loop.
- v2 owns rolling long-form generation.

### Audit Layer

Lineage:

- originality / anti-copy review
- Critic Loop
- structured review reports

Current modules:

- OriginalityAuditor
- Codex validation reports
- Antigravity review reports
- boundary and red-line reports

Evolution:

- Phase 2A-2 validation correctly caught boundary-string hygiene without blocking structural progress.
- Phase 2A-2R upgrades the audit target from word-level fear to structure-level anti-copying.

## 4. What Entered v1

Entered v1 / Phase 1:

- Local CLI pipeline
- novel metadata scan
- skeleton extraction
- Draft-07 schema validation
- flat BookDNA / NarrativeDNA / StateLedger stubs
- Core7 formal promotion path
- Core7 mechanism inventory
- category manifest
- static originality and boundary checks
- human review gates
- Codex / Hermes / Antigravity role separation
- Drive synchronization of reports and key artifacts

## 5. Deferred to v1.5 / v2

Deferred to v1.5:

- tree World Bible
- dynamic character relation graph
- dynamic faction conflict
- power scaling formulas
- foreshadowing ledger
- Draft-Critic revision loop
- style matching / prose refinement engine
- temporal continuity checks

Deferred to v2:

- long-term vector / graph memory
- rolling multi-chapter / multi-volume outline expansion
- long-form production loop
- asynchronous multi-agent message bus
- visual creation dashboard
- robust state inheritance across many chapters

Not currently planned:

- compiler-grade "heavenly law" physics runtime.

## 6. Corrections Made During Actual Execution

### Correction 1: From Antigravity prototype to Codex local pipeline

Phase 0C identified that Antigravity had temporarily bootstrapped research, docs, and demo work. Phase 1A corrected this by moving pipeline work into local scripts and reproducible reports.

### Correction 2: From 18-book ambition to Core7 controlled promotion

The system scanned 18 books for engineering readiness, but formal extraction was restricted to Core7. This protected quality and prevented stub assets from becoming false formal sources.

### Correction 3: From schema-first creation to creative-space reopening

Phase 2A controlled candidates were mechanically valid but creatively narrowed. Phase 2A-2R corrected this by restoring a high-concept, large-world, large-fate creative stage before schema convergence.

### Correction 4: From word-level over-sanitization to structure-level originality

Early candidate validation treated source-specific words as high-risk hygiene signals. Phase 2A-2R clarified that originality should primarily police copied character paths, bridge sequences, causality chains, and single-book cloning, while still banning direct use of core proper nouns in final setting assets.

## 7. Has the System Deviated From the Original Vision?

Conclusion: no strategic deviation; yes, temporary tactical narrowing.

The system still matches the original master vision:

- It remains a research + creation system, not a simple writing prompt.
- It preserves the "classic corpus -> abstraction -> library -> original design" chain.
- It keeps local engineering, structured schemas, state ledgers, review gates, and multi-agent roles.
- It explicitly treats v1 as MVA, not final system.

The temporary deviation was Phase 2A's creative narrowing: the system became too obedient to mechanism recipes and YAML fields. Phase 2A-2R is the correction that brings it back toward the original grand synthesis ambition.

## 8. Does the System Still Follow "Research, Analyze, Build Library, Then Create"?

Yes.

Observed sequence:

1. Phase 0A/0C: research, schema gap discovery, original vision reconciliation.
2. Phase 1A: engineering pipeline and skeleton extraction.
3. Phase 1B: Core7 analysis, formal promotion, mechanism notes.
4. Phase 1B.5: mechanism inventory and category manifest.
5. Phase 1C: Owner acceptance before Phase 2.
6. Phase 2A: controlled design only, no prose.
7. Phase 2A-2R: creative-space methodology correction, still no prose.

The system has not jumped directly to novel drafting.

## 9. Why Phase 2A-2R Is a Healthy Correction, Not a Direction Reversal

Phase 2A-2R is healthy because it restores the hierarchy intended by the original architecture:

- The mechanism library is fuel, not the menu.
- Schema is an organizing and validation tool, not the origin of inspiration.
- Anti-copy review is structure-level, not mere fear of genre vocabulary.
- Chinese web-novel market and reader validation are part of the research base, not an afterthought.
- Big world, big conflict, big growth, big fate, and long-form vitality are returned to the center.

This does not undo Phase 1 or Phase 2A validation. It uses their outputs correctly: as controlled knowledge assets and safety rails, not as a creative cage.

## 10. Final Audit Decision

PASS.

Novel Research Lab remains aligned with its original lineage and master vision. Phase 2A-2R should be recorded as an intentional system-health correction: it preserves engineering rigor while reopening the creative amplitude required for a long-form grand synthesis engine.
