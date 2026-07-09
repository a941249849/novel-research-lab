# NRL Runtime Autonomy Convergence v0.13 Design Spec

## Purpose

NRL already has a working local Antigravity CLI bridge:

```text
Codex Runtime -> agy -p -> response file -> NRL validation
```

However, the control plane still declares Antigravity as
`manual_handoff` with `can_execute: false`. This is a stale capability model:
the bridge is available and has been used, but the runtime, job queue, system
status, and Studio continue to describe a pre-bridge workflow.

v0.13 makes the bridge a formal, restricted Runtime adapter. It does not
authorize content production, phase advancement, Hermes execution, or direct
unvalidated state mutation.

## Scope

v0.13 delivers a closed, auditable Antigravity review loop for registered NRL
Agent jobs:

```text
registered review job
  -> generated packet
  -> guarded CLI dispatch
  -> bridge response captured in controlled inbox
  -> explicit validation
  -> optional existing promotion gate
```

It also makes every surface report the same capability truth:

- Antigravity is `cli_bridge` only when `agy --version` succeeds.
- The adapter may execute registered structural-review jobs, not arbitrary
  prompts or shell commands.
- A bridge response is `output_received`, never `validated` or `promoted` by
  implication.
- Hermes remains `paused_not_removed` and cannot execute.

## Non-Goals

- No prose, chapter planning, final character sheets, or novel asset dossier.
- No Phase 2F advance.
- No Hermes adapter or Hermes execution.
- No Studio button that dispatches Antigravity.
- No direct read, quote, or exposure of `novel_training_set/` prose.
- No automatic promotion of the existing 18 full-corpus response files.
- No background daemon, polling worker, or arbitrary shell-execution API.

## Adapter Contract

`system/runtime/agent_adapters.json` remains a declared adapter registry. The
Antigravity entry is migrated from `manual_handoff` to `cli_bridge`:

```json
{
  "mode": "cli_bridge",
  "supported_modes": ["manual_handoff", "client_handoff", "api", "cli", "cli_bridge"],
  "can_execute": true,
  "execution_policy": "registered_review_jobs_only"
}
```

The registry is not sufficient evidence by itself. At every status or dispatch
decision, Runtime calls `build_antigravity_bridge_status()` and derives an
effective state:

| Declared adapter | Bridge probe | Effective state | Dispatch allowed |
| --- | --- | --- | --- |
| `cli_bridge` | available | `ready` | yes, for allowlisted jobs |
| `cli_bridge` | unavailable | `blocked_bridge_unavailable` | no |
| any other mode | any | `manual_handoff` | no |

`system-status`, production-runtime status, architecture reconciliation, and
Studio must expose both the declared mode and effective state. The human-facing
role is `CLI 协作文学审查`, not `人工外部文学审查`.

## Guarded Dispatch Contract

Add a single Runtime command:

```bash
python3 system/runtime/nrl.py agent-dispatch --job-id <job-id>
```

The command is an allowlisted operation, not a general prompt runner. It must:

1. Load the job from `system/agent_ops/job_queue.v0.5.json`.
2. Require `owner_agent == "antigravity"` and
   `job_type == "antigravity_structural_review"`.
3. Require job state `ready_for_antigravity`.
4. Require the effective `cli_bridge` state to be `ready`.
5. Require the generated packet at `input_packet_path` and reject an empty
   packet or one containing a raw corpus path.
6. Write the request copy to `.agent-handoff/antigravity/requests/` and invoke
   the existing `ask_antigravity()` bridge.
7. Capture bridge output at the job's exact `expected_output_path` under
   `system/agent_ops/inbox/`.
8. Set job state to `external_running` before invocation and to
   `output_received` only after a zero-return bridge call writes a non-empty
   inbox file.
9. On bridge failure, set job state to `blocked`, preserve the bridge log path,
   and record a non-sensitive failure reason.

The dispatch result includes `job_id`, `state`, `request_file`, `output_file`,
`bridge_log_path`, and timestamps. It must never return raw response text.

## Validation and Promotion Boundary

The existing `agent-validate --job-id` command remains the only operation that
may change `output_received` to `validated`. Existing promotion code remains
the only operation that may move a validated review into a creation-asset
store. Dispatch must not call validation or promotion internally.

The v0.8 full-corpus proof flow remains separate because it requires one
machine-verifiable receipt for each source file and four phase ranges. The 18
local response files are evidence candidates, not automatically trusted input.
A later data-curation release must explicitly map, merge, validate, and review
them before any research-asset promotion.

## Runtime and Studio Data

Add a reusable `build_antigravity_execution_status(state, adapters)` contract
owned by the Agent Ops/bridge boundary. It returns:

```json
{
  "declared_mode": "cli_bridge",
  "bridge_available": true,
  "effective_state": "ready",
  "can_dispatch_registered_reviews": true,
  "blocked_reason": null,
  "allowed_job_types": ["antigravity_structural_review"]
}
```

Consumers use this contract rather than independently interpreting the adapter
file. Studio stays read-only: it shows the effective state, current job state,
bridge availability, and the fact that dispatch happens through Codex Runtime.
It does not add an execute button.

## Failure Handling

- Missing `agy`: return a structured blocked state; do not alter a ready job.
- Invalid job id, owner, type, state, packet path, or raw corpus reference:
  reject before spawning `agy` and leave the job unchanged.
- Non-zero `agy` exit: preserve response/log metadata, mark job `blocked`, and
  expose a concise failure reason.
- Empty zero-exit response: mark job `blocked`; do not create an
  `output_received` transition.
- A repeated dispatch for `external_running`, `output_received`, `validated`,
  or `promoted` job is rejected and cannot overwrite evidence.

## Tests and Acceptance

Use a fake `agy` executable in isolated `NRL_ROOT` fixtures. Tests must prove:

1. A configured, available CLI bridge reports `cli_bridge / ready` and a
   missing binary reports `blocked_bridge_unavailable`.
2. A valid registered review job transitions
   `ready_for_antigravity -> external_running -> output_received`, writes only
   the controlled request and inbox paths, and records the bridge log.
3. Invalid job state, non-Antigravity owner, unsupported job type, missing
   packet, and raw-corpus packet all fail without spawning the fake CLI or
   mutating queue state.
4. `agent-dispatch` does not validate, promote, advance phase state, call
   Hermes, or return generated review text.
5. `system-status`, production runtime data, Studio data, architecture role
   contract, and built Studio contain the new effective CLI collaboration
   state rather than stale `manual_external_literary_review` wording.
6. Existing full-corpus proof promotion remains blocked without its separate
   Owner decision.
7. Existing Python runtime tests, Studio build, Astryx doctor,
   `validate-state`, `system-check`, and `git diff --check` pass.

## Delivery Sequence

1. Commit this spec.
2. Create and commit a TDD implementation plan.
3. Implement the bridge capability contract and status convergence.
4. Implement guarded Agent-job dispatch and its state transitions.
5. Update Studio/runtime wording and add regression coverage.
6. Run full verification, commit, and push.

After v0.13, the next system release is `Corpus-to-Creation Operating System
v0.14`: original-project synthesis, Story Bible asset contracts, and the
nine-family operating workflow. Hermes remains outside that release until its
explicit authorization gate.
