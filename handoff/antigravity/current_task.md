# Novel Research Lab Agent Handoff

## Mission

- mission_id: phase2d_antigravity_outline_tree_review
- mission_name: Phase 2D Antigravity Outline Tree Review
- phase: Phase 2D
- responsible_agent: antigravity
- adapter_mode: manual_handoff
- adapter_can_execute: false
- owner_gate_required: False

## Required Inputs

- phase2C/01_prompt/phase2C_bible_output_contract.md
- phase2C/02_hermes_bible/borrowed_heaven_life_account_bible.md
- phase2C/03_codex_validation/phase2C_antigravity_bible_review_report.md
- phase2C/03_codex_validation/phase2C_bible_validation_report.md
- phase2D/00_entry/phase2D_entry_manifest.md
- phase2D/00_entry/phase2D_input_manifest.md
- phase2D/00_entry/phase2D_launch_readiness_report.md
- phase2D/00_entry/phase2D_outline_tree_requirements.md
- phase2D/00_entry/phase2D_output_contract.md
- phase2D/00_owner_gate/phase2D_owner_gate_acknowledgement.md
- phase2D/01_outline_tree/borrowed_heaven_volume1_outline_tree.md
- phase2D/02_codex_validation/phase2D_outline_tree_validation_report.md
- system/mission_controller/agent_task_contract.md
- system/mission_controller/current_phase_state.json
- system/mission_controller/next_mission_rules.md

## Expected Outputs

- handoff/antigravity/outputs/phase2D_antigravity_outline_tree_review.md

## Blocked Actions

- write novel prose
- write first chapter
- generate full character cards
- bypass Codex validation
- bypass Antigravity review
- freely read novel_training_set
- generate detailed chapter-by-chapter prose outline

## Runtime Instruction

This handoff is for manual external-agent execution. The runtime has not called the agent. Place the completed external output in the expected output directory, then run:

```text
python3 system/runtime/nrl.py ingest --agent antigravity --file <path>
```
