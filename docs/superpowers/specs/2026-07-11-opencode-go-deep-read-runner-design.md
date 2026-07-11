# OpenCode Go Deep-Read Runner Design

## Goal

Make the verified v0.18 corpus-reading pipeline runnable while Antigravity is unavailable, without changing its evidence contract or enabling prose generation.

## Decision

Use OpenCode Go `glm-5.2` with the `max` reasoning variant as the primary per-chunk worker. The benchmark on `book-07-f82ccdb9a2b3-chunk-003` was the only candidate that passed the existing v0.18 validator: 24 chapter-heading matches, all required analysis families, and bound source fields. DeepSeek V4 Pro is reserved for later book-level and cross-book audit; V4 Flash is not selected because the benchmark run failed during output handling.

## Runtime Contract

- `agy` remains the default runner and keeps its current behavior.
- `opencode-go` invokes the locally authenticated OpenCode CLI with an explicit `opencode-go/<model>` model ID and reasoning variant.
- The runner reads the existing packet and normalized UTF-8 bounded chunk only.
- The runtime extracts a single bound JSON response from CLI output, writes only that JSON to the planned response path, then runs the existing validator.
- Non-JSON output, ambiguous JSON, nonzero exit status, or a failed validator result is rejected and cannot increase coverage.

## Non-goals

- No raw corpus reads outside the normalized bounded files.
- No Story Bible, chapter plan, prose, Hermes, or Owner Gate transition.
- No credential material in repository files or runtime state.
