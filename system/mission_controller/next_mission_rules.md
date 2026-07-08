# Next Mission Rules

- component: Mission Controller v0
- status: specification_only
- generated_at: 2026-07-08

## 1. Rule Format

Each rule follows:

- condition
- allowed next mission
- blocked next mission
- required gate

Mission Controller v0 is a router. It records rules; it does not execute agents.

## 2. Hermes Output Completion

Condition:

- Hermes output exists at the contracted path.

Allowed next mission:

- Codex Validation

Blocked next mission:

- Antigravity Review
- Owner Gate
- next phase entry
- prose generation

Required gate:

- Codex validation must happen first.

## 3. Codex Validation PASS

Condition:

- Codex validation status is `PASS`.

Allowed next mission:

- Antigravity Review

Blocked next mission:

- Owner Gate without Antigravity Review
- next phase entry

Required gate:

- Antigravity Review.

## 4. Codex Validation PASS_WITH_WARNINGS

Condition:

- Codex validation status is `PASS_WITH_WARNINGS`.

Allowed next mission:

- Antigravity Review with warning list attached.

Blocked next mission:

- direct Owner Gate
- direct next phase entry
- Hermes rework unless Owner or Codex explicitly requests warning cleanup first

Required gate:

- Antigravity Review must see the warning list.

## 5. Codex Validation FAIL

Condition:

- Codex validation status is `FAIL`.

Allowed next mission:

- Fix Preparation
- artifact correction task
- Hermes rework prompt preparation, if failure belongs to Hermes output

Blocked next mission:

- Antigravity Review
- Owner Gate
- next phase entry

Required gate:

- Codex re-validation after fixes.

## 6. Antigravity Review ACCEPT

Condition:

- Antigravity review status is `ACCEPT` or `ACCEPT_BIBLE_FOR_NEXT_PHASE`.

Allowed next mission:

- Owner Gate

Blocked next mission:

- direct next phase entry unless Owner Gate has already accepted

Required gate:

- Owner decision.

## 7. Antigravity Review ACCEPT_WITH_FIXES

Condition:

- Antigravity review status is `ACCEPT_WITH_FIXES`.

Allowed next mission:

- Fix Preparation
- Owner Gate only if explicitly requested with fix list attached

Blocked next mission:

- direct next phase entry
- prose generation

Required gate:

- Fix list must be captured before next phase preparation.

## 8. Antigravity Review REQUEST_REWORK

Condition:

- Antigravity review status is `REQUEST_REWORK`.

Allowed next mission:

- Hermes Rework Prompt Preparation

Blocked next mission:

- Owner Gate acceptance
- next phase entry

Required gate:

- reworked Hermes output followed by Codex Validation.

## 9. Owner Gate ACCEPT

Condition:

- Owner Gate status is `ACCEPT`.

Allowed next mission:

- next phase Entry Pack Preparation

Blocked next mission:

- skipping entry pack
- direct content generation unless the accepted gate explicitly authorizes that exact content task

Required gate:

- next phase entry manifest and input/output contracts.

## 10. Owner Gate HOLD

Condition:

- Owner Gate status is `HOLD`.

Allowed next mission:

- no progression
- status clarification
- owner decision update

Blocked next mission:

- Hermes execution
- Antigravity execution
- next phase entry
- prose generation

Required gate:

- Owner must update the gate.

## 11. Global Prohibitions

Any phase must block:

- unauthorized prose
- first chapter
- chapter outline
- detailed volume outline
- full character cards
- free reads of `novel_training_set/`
- free reads of 18 single-book reports
- use of dropped concepts
- bypassing Codex validation
- bypassing Antigravity review
- bypassing Owner Gate

## 12. Current Phase SYS-1 Application

Current state:

- Phase 2C Hermes Bible: completed
- Codex Validation: `PASS_WITH_WARNINGS`
- Antigravity Bible Review: `ACCEPT_BIBLE_FOR_NEXT_PHASE`
- Owner Gate required: true

Rule triggered:

- Antigravity Review ACCEPT -> Owner Gate

Next recommended mission:

- Phase 2D Entry Preparation after Owner Gate acknowledgement.
