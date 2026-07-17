# NRL Codex Model Team v0.27

## Active Decision

Hermes is retired from the active Novel Research Lab architecture. It has no
writer, reviewer, gate, adapter, readiness, or fallback role. Historical files
whose names contain `hermes` remain immutable provenance and do not grant an
active capability.

## Primary Production Team

| Route | Model | Responsibility |
| --- | --- | --- |
| showrunner | `gpt-5.6-sol` | long-range planning, Story Window compilation, high-risk adjudication |
| reviewer | `gpt-5.6-sol` | causality, continuity, vitality, anti-AI-taste, window acceptance |
| writer | `gpt-5.6-terra` | chapter prose from compiled context |
| editor | `gpt-5.6-terra` | bounded revision and scene bridging |
| observer | `gpt-5.6-luna` | schema-bound fact and state extraction |
| mechanical | `gpt-5.6-luna` | low-risk structured checks and candidates |

All routes execute through the local Codex adapter. The runtime, schemas,
hashes, Owner Gate, and state settlement remain model-independent authorities.
The route is promoted by
`system/production_runtime/calibration/codex_model_team_attestation.v0.27.json`,
which binds the prior blind calibration, the accepted Volume 1 release
manifest, and 52 retained generation-cost records. Those records include 14
accepted Sol generations and 29 accepted Terra generations.

## Antigravity Boundary

Antigravity is a backup, not a normal production stage. It may run only when:

1. an independent second opinion is explicitly required; or
2. the primary Codex provider fails or reaches a usage limit.

It receives an inline, hash-bound packet in an isolated working directory. It
cannot own project state, authorize progression, modify accepted chapters, or
silently replace a failed gate.

## Runtime Consequences

- Missing Antigravity quota does not make the primary runtime unhealthy.
- Missing or installed Hermes binaries do not affect production readiness.
- Chapter checkpoint and ten-chapter window reviews use Sol first.
- Antigravity provider/model overrides apply only to fallback attempts.
- Legacy Hermes commands return `retired` and cannot generate prose.

## Verification

```bash
python3 system/runtime/nrl.py system-status
python3 system/runtime/nrl.py model-routing-status
python3 system/runtime/nrl.py production-preflight
python3 system/runtime/nrl.py system-check
python3 system/runtime/nrl.py studio-build
```
