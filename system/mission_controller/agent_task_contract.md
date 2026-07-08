# Agent Task Contract

- component: Mission Controller v0
- status: specification_only
- generated_at: 2026-07-08

## 1. Purpose

This document defines the task-package contract Mission Controller should use when routing work to Codex, Hermes, Antigravity, and Owner Gate.

Every task package should include:

- mission name
- current phase
- selected project, if any
- allowed inputs
- required outputs
- output path
- boundary restrictions
- gate expected after completion
- blocked actions

## 2. Codex Task Contract

### Purpose

Codex tasks are for engineering and orchestration support:

- file management
- scripts
- validation
- manifests
- state updates
- Drive sync
- prompt preparation
- output contracts
- replay records
- schema checks

### Required Task Fields

A Codex task package should specify:

- input artifact paths
- output artifact paths
- validation checks
- sync target
- current gate state
- exact prohibited actions

### Codex Must Not

Codex must not:

- lead literary creativity
- freely generate novel settings
- write novel prose
- write first chapters
- write chapter outlines
- write detailed volume outlines
- replace Antigravity literary judgment
- replace Owner direction decisions
- call Hermes unless explicitly authorized
- call Antigravity unless explicitly authorized

## 3. Hermes Task Contract

### Purpose

Hermes tasks are for controlled creative generation:

- Grand Synthesis candidates
- Bible first draft
- Outline Tree first draft
- later chapter drafts only after future explicit authorization

### Required Task Fields

A Hermes task package must specify:

- exact prompt file
- allowed input files
- forbidden input files
- required output path
- required output structure
- boundary self-check
- stop rule if input is missing or unauthorized

### Hermes Must Not

Hermes must not:

- freely read training-set files
- read `novel_training_set/` unless explicitly authorized
- bypass the prompt
- bypass the output contract
- write unauthorized prose
- write unauthorized first chapters
- write unauthorized chapter outlines
- decide that a phase is complete
- decide to enter the next phase
- use dropped concepts as hidden material

## 4. Antigravity Task Contract

### Purpose

Antigravity tasks are for deep review:

- literary life-force judgment
- originality risk judgment
- long-form potential judgment
- structural anti-copy review
- readiness recommendation
- next-phase risk identification

### Required Task Fields

An Antigravity task package should specify:

- artifact under review
- relevant contract / prompt / validation report
- review criteria
- required decision labels
- handoff expectations
- blocked actions

### Antigravity Must Not

Antigravity must not:

- rewrite the Bible
- freely generate new settings
- write novel prose
- write first chapters
- write chapter outlines
- replace Owner final decisions
- mutate project artifacts unless explicitly authorized

## 5. Owner Gate Contract

### Purpose

Owner Gate handles final direction decisions:

- accept phase
- hold phase
- request fixes
- request rework
- select project
- authorize entry into next phase

### Required Gate Fields

An Owner Gate record should include:

- decision
- accepted artifacts
- rejected / parked artifacts
- next authorized phase
- blocked actions
- timestamp
- owner notes, if any

### Owner Gate Decisions

Supported v0 decisions:

- `ACCEPT`
- `ACCEPT_WITH_FIXES`
- `HOLD`
- `REQUEST_FIXES`
- `REQUEST_REWORK`
- `SELECT_PROJECT`
- `AUTHORIZE_NEXT_PHASE_PREPARATION`

## 6. Global Blocked Actions

All agent task packages should block:

- unauthorized prose
- first chapter
- chapter outline
- detailed volume outline
- full character cards
- raw training-set reads
- bypassing Codex validation
- bypassing Antigravity review
- bypassing Owner Gate
