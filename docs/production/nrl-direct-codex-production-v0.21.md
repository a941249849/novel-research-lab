# NRL Direct Codex Production v0.21

## Decision

Codex is the only production control plane. As of the v0.27 role migration,
Hermes is retired from active production rather than retained as enrichment.

## Model Routing

- Sol: showrunner planning, high-risk arc decisions, causal review, and window
  adjudication.
- Terra: primary prose, bounded revision, and scene-bridge editing.
- Luna: schema-bound observation and low-risk mechanical candidates.
- Antigravity: isolated backup for independent review or Codex provider
  failure; it receives inline hash-bound packets and has no project directory
  mounted.

## Final-Text Lifecycle

```text
intent -> compiled context -> draft -> initial review -> optional substantive
revision -> final-text observation -> final review -> settlement -> acceptance
```

Warnings alone do not force a rewrite. Every settlement is bound to observations
extracted from the exact final text being accepted.

## Calibration Gate

Before production resumes, run a non-publishing, bounded calibration across the
three model routes and score output for contract compliance, continuity,
causality, anti-template signals, reviewer verdict, latency, and retry rate.
The routing table may change only from recorded calibration evidence.

The current calibration generated nine isolated samples and completed a
non-gating internal screen. Its verdict is `RECALIBRATE`: Sol is provisionally
the only primary prose route, while Terra and Luna are not allowed to take over
that role. Antigravity CLI review is recorded as blocked when its executable is
present but an actual agent call fails; that failure cannot be treated as a
review result. The production gate remains closed until a working independent
review records acceptance.

```bash
python3 system/runtime/nrl.py direct-writer-calibration-run
python3 system/runtime/nrl.py direct-writer-calibration-review-packet
python3 system/runtime/nrl.py direct-writer-calibration-status
```
