# Novel Research Lab Mission Controller v0 Specification

- phase: Phase SYS-1
- component: Mission Controller v0
- status: specification_only
- generated_at: 2026-07-08

## 1. Positioning

Mission Controller v0 is a stage orchestrator and task router for Novel Research Lab.

It is not:

- an author
- a reviewer
- a literary judge
- an automatic writer
- an Agent runtime
- an InkOS clone

Its job is to make the existing Novel Research Lab workflow explicit, repeatable, and gate-aware.

## 2. Problem It Solves

Novel Research Lab has already run a full manually orchestrated loop:

```text
training-set research
-> mechanism distillation
-> Grand Synthesis
-> original project selection
-> Original Bible
-> Codex validation
-> Antigravity review
-> Owner Gate
-> next story phase preparation
```

The problem is not creative capability. The problem is coordination memory:

- What phase is the project in?
- Which artifacts are authoritative?
- Which agent may act next?
- Which actions are blocked?
- Which gate result allows or blocks the next mission?
- What should the next task package contain?

Mission Controller v0 records and routes those answers.

## 3. What It Does Not Solve

Mission Controller v0 does not:

- write fiction
- decide literary quality
- replace Antigravity review
- replace Owner decisions
- automatically call Hermes
- automatically call Codex
- automatically call Antigravity
- implement a UI
- implement a multi-agent runtime
- implement long-term memory
- implement a database
- rewrite prior phase artifacts

It only specifies the minimum state and routing layer needed for future automation.

## 4. Relationship To InkOS And Similar Systems

Mission Controller may borrow engineering ideas from InkOS / Claude-Book / Novel Engine / writing skill systems:

- explicit state files
- structured task contracts
- stage gates
- tool-role separation
- reproducible artifacts
- output contracts

It must not copy those systems as product shape or architecture.

Novel Research Lab is not an InkOS clone. NRL's route is its own:

```text
training-set research
-> mechanism distillation
-> Grand Synthesis
-> original project selection
-> Original Bible
-> Codex validation
-> Antigravity review
-> Owner Gate
-> Outline Tree
-> State Ledger
-> long-form writing loop
```

Mission Controller exists to serve that route.

## 5. Novel Research Lab Specificity

Novel Research Lab is built around:

- corpus research before creation
- mechanism distillation before project selection
- structure-level originality checks
- Codex engineering validation
- Antigravity literary-system review
- Owner Gate decisions
- controlled Hermes creative generation
- strict prevention of unauthorized prose, chapters, outlines, or raw corpus reuse

Mission Controller v0 must preserve these boundaries.

## 6. Agent Roles

### Codex

Codex handles:

- file management
- schemas
- validation
- manifests
- state updates
- prompt preparation
- Drive sync
- engineering reports

Codex must not replace Hermes creative generation or Antigravity literary judgment.

### Hermes

Hermes handles controlled creative generation only after an authorized prompt and output contract exist.

Hermes must not decide phase transitions, read unauthorized inputs, or write unauthorized prose.

### Antigravity

Antigravity handles:

- deep review
- literary life-force judgment
- originality risk judgment
- long-form potential judgment
- recommendation on next-phase readiness

Antigravity must not replace Owner Gate decisions.

### Owner

Owner handles:

- final direction selection
- phase acceptance / hold / rework decisions
- authorization to enter the next phase

## 7. Core Responsibilities

Mission Controller v0 should:

1. read current project state
2. identify the current phase and subphase
3. identify authoritative artifacts
4. determine the next recommended mission
5. generate the next task package specification
6. validate required file existence and broad structure
7. record Codex validation status
8. record Antigravity review status
9. record Owner Gate status
10. block unauthorized phase jumps
11. block unauthorized prose, first chapter, chapter outline, detailed volume outline, role cards, or raw corpus reads

## 8. Gate Model

Mission Controller v0 must treat gates as explicit state transitions:

- Hermes output is not sufficient to advance.
- Codex validation is required after Hermes output.
- Antigravity review is required after passing or warning-level Codex validation.
- Owner Gate is required before entering the next story phase.
- Failure or rework states must route to repair/rework tasks, not onward.

## 9. v0 Scope

v0 includes only:

- Markdown specifications
- a JSON Schema for phase state
- one current state JSON file
- task contracts
- next mission rules
- one replay case based on the Phase 2B -> Phase 2C flow

v0 does not include executable routing code.

## 10. v1 / v2 Deferred Scope

v1 may add:

- a CLI state reader
- automated required-file checks
- schema validation command
- task package template generation
- Drive sync status update helper

v2 may add:

- a lightweight local dashboard
- a richer artifact registry
- automated gate-history queries
- agent invocation adapters
- state transition logs

Deferred until explicitly authorized:

- complex UI
- full Agent runtime
- automatic Hermes execution
- automatic Antigravity execution
- automatic fiction generation

## 11. Non-Negotiable Safety Rule

Mission Controller must always block:

- unauthorized novel prose
- unauthorized first chapter
- unauthorized chapter outline
- unauthorized detailed volume outline
- unauthorized character cards
- free reads of `novel_training_set/`
- bypassing Codex validation
- bypassing Antigravity review
- bypassing Owner Gate
