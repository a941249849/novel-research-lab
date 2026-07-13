# NRL v0.22 Chapter 1 Context Audit

Audit the compiled non-prose Chapter 1 production context. Read only:

- `system/creation_assets/baselines/borrowed_heaven_canonical_baseline_v0.21.json`
- `system/production_runtime/chapters/chapter-0001/intent.json`
- `system/production_runtime/chapters/chapter-0001/context.json`
- `system/production_runtime/chapters/chapter-0001/rule_stack.json`
- `system/production_runtime/chapters/chapter-0001/trace.json`
- `system/creation_assets/project_assets.v0.2.json`

Do not read raw corpus. Do not edit files. Do not write, quote, or propose novel prose, scenes, or dialogue.

Return Markdown with exact sections:

1. `VERDICT`: `ACCEPT`, `ACCEPT_WITH_WARNINGS`, or `REWORK_REQUIRED`.
2. `SCOPE_AUDIT`: check intent/context against the canonical baseline, dormant-asset exclusions, protagonist stage, active hooks, and state-delta limits.
3. `CONTINUITY_AUDIT`: list only concrete cross-asset or state-ledger risks for Chapter 1.
4. `WRITER_BOUNDARY`: hard constraints Hermes must receive if a prose test is later authorized.
5. `NEXT_GATE`: exactly one of `freeze_context_packet`, `repair_context_packet`, or `keep_prose_blocked`.

The output is audit evidence only and cannot authorize prose.
