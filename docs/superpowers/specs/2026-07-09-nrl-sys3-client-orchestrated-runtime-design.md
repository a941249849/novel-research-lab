# SYS-3: NRL v0.2 Client-Orchestrated Runtime And Constraint Compiler Design

- status: design_spec_revised_pending_user_review
- date: 2026-07-09
- project: Novel Research Lab
- scope: product architecture, runtime control, and constraint compiler upgrade design
- current implementation level: L1 manual_handoff
- target implementation level: L2 client_handoff plus runtime constraint compilation

## 1. Problem Statement

Novel Research Lab currently has many correct system concepts: Mission Controller, phase state, task contracts, handoff folders, validation reports, Antigravity review gates, Hermes creative generation gates, and Owner Gate. However, the actual operating experience is still dominated by manual copying between ChatGPT web, Codex, Hermes, and Antigravity.

The result is a system that appears to have multi-agent architecture but behaves like a structured manual workflow. This creates three user-visible failures:

1. The user cannot easily tell which component is authoritative.
2. Agent collaboration is documented but not operationally orchestrated.
3. The user becomes the transport layer, carrying prompts, files, outputs, and decisions across tools.

The current contradiction is not the literary concept itself. The contradiction is that the runtime does not yet provide a readable, driver-level control surface for the multi-agent process, and it does not yet compile research assets into executable creative constraints.

## 2. Design Goal

SYS-3 upgrades NRL from a manual handoff system into a client-orchestrated multi-agent runtime with a constraint compilation layer.

The target is not full API automation. The user does not currently have direct API access for every desired model or tool. Antigravity is valuable because it exposes Gemini model capabilities through its client. Hermes is valuable because it can serve as an isolated creative generation context. Therefore the immediate target is L2 client_handoff:

```text
Codex / NRL Host
-> generates task package
-> prepares exact client handoff
-> assists or automates client opening where possible
-> receives output artifact
-> registers output
-> runs validation or gate checks
-> updates the next allowed action
```

The user may still need to log in, confirm a send action, or save a client output. Those actions should be the exception, not the core workflow.

SYS-3 must also prevent a second failure mode: automatically handing large research reports to Hermes or Antigravity without converting them into compact, executable constraints. Research reports are source material for compilation. They are not direct creative prompts.

## 3. Operating Levels

### L1: manual_handoff

This is the current level.

Runtime writes a task file, the user manually gives it to Hermes or Antigravity, the user manually saves the result, and Codex ingests the result.

L1 is reliable and low risk, but it makes the user the workflow engine.

### L2: client_handoff

This is the SYS-3 target.

Runtime remains the authority. It prepares the task package, opens or stages the target client where possible, tracks what must be sent, validates that the returned artifact is present, and records the outcome. The external client still provides the model capability, but it is no longer the dispatcher.

L2 accepts the practical constraint that some model access exists only through local or web clients.

### L3: api_adapter

This is a future target, not SYS-3.

Runtime directly calls model APIs or CLIs. It handles request execution, timeout mapping, output capture, retries, and artifact registration.

L3 should only be introduced when the user has stable API keys, executable CLIs, or official integration surfaces.

## 4. Authority Model

NRL must stop treating web ChatGPT or any external chat window as the dispatcher. The authority model is:

```text
Mission Controller state
-> Mission Registry
-> Agent Task Contract
-> Runtime command or Studio action
-> Artifact output
-> Validation / Review / Owner Gate
```

Any suggestion from ChatGPT web, Hermes, Antigravity, or another client is non-authoritative until it is converted into a task package or recorded artifact inside NRL.

## 5. Agent Roles

### Codex / NRL Host

Codex is the host adapter and runtime operator.

Responsibilities:

- read and maintain local project state
- generate mission packages
- prepare handoff artifacts
- validate required inputs
- ingest external outputs
- run Codex validation where authorized
- update registry records where authorized
- present the current state and next action
- prevent blocked actions

Codex must not become the literary author, replace Antigravity review, or bypass Owner Gate.

Codex validation is mechanical and contractual. It checks files, schemas, required sections, forbidden actions, expected paths, artifact hashes, and gate eligibility. It should not quietly replace Antigravity's literary judgment.

### Hermes Client Adapter

Hermes is the creative generation adapter.

Its value is not only model identity. Even if it uses a model family overlapping with Codex, it provides an isolated creative execution lane with its own prompt, input contract, output path, and self-check.

Hermes should be used for:

- controlled original concept synthesis
- Story Bible drafts
- Outline Tree drafts
- future prose only after explicit Owner authorization

Hermes must not decide phase transitions, freely read the training set, bypass prompt contracts, or write unauthorized prose.

### Antigravity Client Adapter

Antigravity is the deep review adapter.

Its value is access to Gemini model behavior through the Antigravity client, especially as a heterogeneous judgment source for alternative reasoning, literary risk assessment, originality risk, and long-form structural review.

Antigravity should be used for:

- literary life-force review
- originality and structural anti-copy review
- mechanism-pileup risk review
- long-form potential assessment
- reader follow-through and "want to continue" judgment
- protagonist fate-arc traction review
- readiness recommendation
- next-phase risk identification

Antigravity must not become the author, rewrite the Bible, mutate artifacts directly, or replace Owner decisions.

### Web GPT

Web GPT is a discussion and retrospective surface only.

It may help the user think, summarize, challenge assumptions, or reconstruct previous reasoning. It must not be treated as the current task dispatcher. Its outputs become actionable only when Codex converts them into local NRL artifacts or task packages.

### Owner

The Owner remains the final direction gate.

Owner Gate should be narrow and explicit. A single "continue" must not authorize all future creative work. Owner decisions should approve a specific transition, review result, rework request, adapter upgrade, or phase entry.

Owner Gate decisions must be recorded as structured authorization tickets, not only chat messages.

Minimum Owner Gate decision shape:

```json
{
  "decision_id": "owner_gate_phase2d_review_acceptance_001",
  "decision_type": "accept_review | request_rework | authorize_next_phase | authorize_adapter_upgrade",
  "authorized_scope": [
    "prepare_phase2e_entry",
    "generate_next_mission_package"
  ],
  "forbidden_scope": [
    "write_novel_prose",
    "generate_first_chapter",
    "create_full_character_cards"
  ],
  "expires_after_mission": "phase2e_entry_preparation",
  "owner_note": ""
}
```

## 6. Runtime Components

### Mission Controller

The Mission Controller is the source of current phase truth.

It should answer:

- What phase is active?
- What is the selected project?
- What is the current status?
- What action is blocked?
- Which agent may act next?
- Which gate is required before progress?

### Mission Registry

The Mission Registry records current and historical mission packages.

It should answer:

- What mission is waiting?
- Which agent owns it?
- What inputs are required?
- What output path is expected?
- What status has been registered?
- What artifact completed it?

Mission Registry must use an explicit mission status state machine.

Minimum mission status values:

```text
planned
package_generated
client_staged
awaiting_user_confirmation
awaiting_external_output
output_detected
ingest_started
ingest_failed
validation_passed
validation_failed
review_required
owner_gate_pending
completed
blocked
```

No status transition may imply creative progress unless the corresponding artifact exists and the required validation or gate has been recorded.

### Handoff Attempt Record

Every external Hermes or Antigravity attempt must be recorded separately from the mission itself.

Minimum fields:

```text
handoff_attempt_id
mission_id
target_agent
adapter_mode
input_artifact_hashes
expected_output_path
created_at
stale_after
ingest_command
validation_contract
status
```

This prevents duplicate client runs, stale outputs, wrong-output ingestion, and confusion when multiple review versions exist.

### Adapter Registry

The Adapter Registry describes how each agent can be reached.

Initial modes:

- `local`: Codex can execute directly.
- `manual_handoff`: user must move the task manually.
- `client_handoff`: runtime can stage a client interaction but cannot guarantee full execution.
- `api`: runtime can execute through a stable API.
- `cli`: runtime can execute through a stable local command.

SYS-3 introduces `client_handoff` as the practical bridge between current manual workflows and future API automation.

### Client Handoff Runner

The Client Handoff Runner prepares tool-specific execution packets.

For each external client, it should produce:

- target agent
- current mission
- exact prompt or task packet
- allowed input paths
- forbidden input paths
- expected output path
- copy-ready task content
- save-location instruction
- post-run ingest command
- blocked actions

Where possible, it may open the relevant local app or browser page. If the client does not expose automation hooks, the runner should stop at a clear handoff screen and require the user to confirm the external action.

### Constraint Pack / Context Compiler Runner

The Constraint Pack / Context Compiler Runner is a first-class SYS-3 component.

It converts high-density research assets into agent-safe execution packets. It prevents the system from merely automating the delivery of oversized reports to Hermes or Antigravity.

Inputs may include:

- full corpus distillation whitepaper
- authorial craft distillation index
- mechanism library summaries
- originality red lines
- selected project state
- Story Bible and Outline Tree artifacts
- current mission contract

Outputs must be compact and executable:

- agent-safe context packet
- must_keep_beats
- must_avoid_elements
- protected state reads
- originality red lines
- review criteria
- expected output contract
- source artifact list

The compiler must not pass raw training-set files, full single-book reports, or unrestricted research archives into Creation-phase prompts. If a report cannot be converted into constraints, it remains reference material, not runtime input.

### Minimal Studio

Minimal Studio is the human-readable cockpit for NRL.

It should not become a writing editor or knowledge graph in SYS-3. Its first screen should show:

- current phase and status
- selected project
- next mission
- responsible agent
- adapter mode
- blocked actions
- required inputs and existence checks
- expected output path
- validation / review / Owner Gate chain
- handoff actions
- ingest actions
- runtime health

Minimal Studio is a read-only cockpit plus command launcher. It must not maintain independent project state. All state mutations must go through Mission Controller commands. Studio may display files, statuses, gate records, and command results, but it is not a second source of truth.

The success criterion is that the user can understand the system state without asking web GPT what to do next.

## 7. Data Flow

### Hermes Flow

```text
Owner-authorized creative mission
-> Constraint Pack / Context Compiler builds agent-safe creative packet
-> Codex generates Hermes task package
-> Client Handoff Runner stages Hermes client task
-> User confirms or completes client execution if required
-> Hermes output saved to expected path
-> Codex ingests output
-> Codex validation runs
-> Antigravity review is prepared if validation allows it
-> Owner Gate decides transition
```

### Antigravity Flow

```text
Validated artifact requiring review
-> Constraint Pack / Context Compiler builds review packet
-> Codex generates Antigravity review package
-> Client Handoff Runner stages Antigravity client task
-> User confirms or completes client execution if required
-> Antigravity review saved to expected path
-> Codex ingests review
-> Owner Gate is required
-> next phase preparation may start only after Owner authorization
```

### Web GPT Flow

```text
Discussion or retrospective in web GPT
-> user or Codex extracts decision-relevant insight
-> Codex writes or updates local artifact only after approval
-> Mission Controller remains source of truth
```

Web GPT never directly advances phase state.

### Constraint Compilation Flow

```text
Research / Bible / Outline / State artifacts
-> Codex verifies allowed input paths
-> Constraint Pack / Context Compiler selects relevant material
-> compiler emits compact runtime packet
-> packet is attached to Hermes or Antigravity task package
-> output is judged against the packet contract
```

This flow is the bridge between "research and distillation" and "generation and review". Without it, SYS-3 would only improve transport while leaving creative constraints informal.

## 8. Error Handling

### Missing Client Capability

If a client cannot be opened or automated, runtime must fall back to copy-ready manual handoff. It should still keep the task package, expected output path, and ingest command explicit.

### Missing Output

If the expected output file is missing, ingest must fail with the required path and must not update mission status.

### Wrong Agent Output

If a Hermes output is placed under Antigravity outputs, or an Antigravity review is placed under Hermes outputs, ingest must reject it or require explicit Owner correction.

### Stale Handoff Output

If an output was produced from an older handoff attempt whose input hashes or mission status no longer match current state, ingest must reject it or require explicit Owner correction.

### Contract Violation

If an output contains unauthorized prose, unauthorized source reads, phase decisions made by the wrong agent, or missing required sections, Codex validation should mark it as failed or warning-level, depending on severity.

### Constraint Compilation Failure

If the compiler cannot produce a compact agent-safe packet, the mission must stop before client handoff. The fallback is not to pass larger reports directly to the agent. The fallback is to request a narrower mission or a better source artifact.

### Client Drift

If a client UI changes or an automation hook breaks, NRL should degrade to manual handoff without changing the mission authority model.

## 9. Safety Rules

The following actions remain blocked unless a specific Owner Gate authorizes them:

- novel prose
- first chapter
- detailed chapter-by-chapter prose outline
- full character cards
- free reads of `novel_training_set/`
- bypassing Codex validation
- bypassing Antigravity review
- bypassing Owner Gate
- upgrading an adapter from `manual_handoff` or `client_handoff` to `api` or `cli`

SYS-3 does not weaken current creative safety boundaries. It reduces transport friction while keeping phase gates intact.

## 10. Non-Goals

SYS-3 does not build:

- full API automation for every model
- a general-purpose writing editor
- a full knowledge graph
- a vector database or long-term memory engine
- automatic novel drafting
- automatic phase transitions
- automatic Owner Gate decisions
- unrestricted training-set reading
- full research-to-generation automation without compiled constraints

These may be considered in later phases only after the runtime control surface is stable.

## 11. Testing And Verification

SYS-3 implementation should be verified through the current Phase 2D state, without advancing novel content.

Minimum verification cases:

1. Runtime can show current status and next mission.
2. Runtime can check required input files for the next mission.
3. Runtime can generate an Antigravity client handoff packet.
4. Runtime can show that Antigravity is a client or manual adapter, not an API adapter.
5. Runtime refuses to mark the review complete without an output artifact.
6. Runtime can ingest a review artifact at the expected path.
7. Runtime moves the system to an Owner Gate state after Antigravity review ingest.
8. Runtime does not authorize prose, first chapter, full character cards, or detailed chapter outline.
9. Studio first screen can explain current phase, next agent, blocked actions, expected output, and gate chain.
10. Runtime records a handoff attempt with input artifact hashes and expected output path.
11. Runtime rejects a stale or wrong-path external output.
12. Runtime can generate a compact Constraint Pack / Context Compiler packet for a mission.
13. Runtime can show that Studio reads runtime state and does not own independent state.
14. Runtime can record an Owner Gate decision ticket with authorized and forbidden scopes.
15. Codex mechanical validation and Antigravity literary review are shown as separate gate types.

The replay case is `《借天改命账》` Phase 2D. It is a runtime verification case, not a license to continue content generation.

## 12. Rollout Plan

### Step 1: Freeze Content Progress

Pause novel content advancement while SYS-3 is designed and implemented. Current Phase 2D remains pending Antigravity review.

### Step 2: Add Adapter Level Semantics

Extend the adapter model conceptually from `manual_handoff` and `local` to include `client_handoff`, while preserving current manual behavior as fallback.

### Step 3: Add Mission Control Commands

Add runtime commands for registry view, required input checks, gate status, transition checks, and client handoff packet generation.

### Step 4: Add Mission Status And Handoff Attempts

Add mission status transitions and handoff attempt records before adding richer client automation. This makes every external run traceable and prevents stale outputs from silently advancing state.

### Step 5: Add Owner Gate Decision Records

Represent Owner decisions as structured authorization tickets with explicit allowed scope, forbidden scope, and expiry.

### Step 6: Add Constraint Pack / Context Compiler Runner

Compile research, Bible, Outline Tree, state, and review criteria into compact agent-safe packets. This runner is required before richer Hermes or Antigravity execution, because it prevents raw document dumping.

### Step 7: Add Minimal Studio

Expose the same runtime state in a local cockpit. Studio should read from existing files and commands rather than inventing parallel state.

### Step 8: Replay Phase 2D

Use the current Antigravity Outline Tree Review as a test of the new client handoff process.

### Step 9: Decide Adapter Upgrade Order

After L2 works, decide whether Hermes or Antigravity should receive deeper automation first. The likely first target is Hermes if a stable creative-generation client or API route exists, because its outputs have stricter structure and can benefit more from repeatable execution.

## 13. Success Criteria

SYS-3 succeeds when:

- the user no longer needs web GPT to know the next operational step
- Codex / NRL is visibly the runtime host
- Hermes and Antigravity are operational adapters, not loose chat destinations
- manual copying is reduced to unavoidable client confirmation or login steps
- every external output returns to a known artifact path
- every external run has a handoff attempt record
- every creative or review packet is compiled from allowed inputs
- validation, review, and Owner Gate remain explicit
- Owner Gate is represented as a structured authorization record
- the system can explain why a blocked action is blocked
- the user can open Studio or run CLI commands and understand the current state

## 14. Core Product Decision

The current system direction is correct at the conceptual level but incomplete at the runtime level.

The correction is not to abandon Codex, Hermes, or Antigravity. The correction is to stop designing around product names and instead design around runtime capabilities:

- host
- creative generation
- deep review
- discussion
- owner gate

Under this model, Antigravity remains valuable because it gives access to Gemini model judgment through the client. Hermes remains valuable because it gives an isolated creative lane. Codex remains the host because it controls local files, state, validation, and runtime behavior.

SYS-3 should make that architecture operational and should close the missing link between research distillation and executable generation constraints.

## 15. Required Patch Checklist

SYS-3 v0.2 incorporates the external review patches as design requirements:

```text
PATCH-1: Add Mission Status State Machine
PATCH-2: Add Handoff Attempt Record
PATCH-3: Add Owner Gate Decision Record
PATCH-4: Add Constraint Pack / Context Compiler Runner
PATCH-5: Add Studio Single Source of Truth Rule
PATCH-6: Clarify Antigravity as Heterogeneous Review Source
PATCH-7: Define Codex Mechanical Validation vs Antigravity Literary Review Boundary
PATCH-8: Add Phase 2D Replay Acceptance Tests
```

These patches do not authorize novel content advancement. They prepare the runtime so the current Phase 2D Antigravity review and later creative phases can be driven by explicit state, compiled constraints, and auditable gates.
