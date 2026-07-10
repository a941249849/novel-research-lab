# NRL Controlled Prose Audit v0.16

## Role

Act as an independent literary reviewer. Review the bounded Hermes scene test
for `《借天改命账》`; do not rewrite it or generate additional prose.

## Allowed Inputs

- `system/agent_ops/inbox/hermes-controlled-prose-test-v016.md`
- `system/agent_ops/inbox/hermes-final-asset-bundle-v015.json`
- `system/agent_ops/inbox/antigravity-final-assets-audit-v016.md`

Do not read `novel_training_set/` or any other corpus material.

## Required Output

Return Markdown only using exactly these headings:

```text
# Antigravity Controlled Prose Audit v0.16
## Verdict
## Strengths
## Blocking Issues
## Revision Priorities
## Production Recommendation
```

The verdict must start with `ACCEPT`, `ACCEPT_WITH_WARNINGS`, or
`REWORK_REQUIRED`. Assess only: literary naturalness, visible cost, emotional
anchor, community agency, sensory fantasy translation, originality risk, and
reader-facing jargon. Do not approve full chapter or serial production.
