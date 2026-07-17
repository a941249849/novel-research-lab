# NRL Multi-Project Runtime v0.28

## Decision

Novel Research Lab is a reusable Corpus-to-Creation engine. `《借天改命账》` is
the first accepted project produced by that engine, not the system identity,
template, or permanent planning target.

## Storage Contract

Shared, immutable engine assets remain under `system/`:

- corpus proof, Book DNA, Narrative DNA, and cross-book distillation;
- creation and production JSON Schemas;
- model-team routing and calibration evidence;
- Mission Controller and adapter contracts.

Every new project's mutable state lives under:

```text
projects/<project_id>/
  project_state.json
  design/
  creation_assets/
  production_runtime/
    chapters/
    intents/
    plans/
    state/
    story_windows/
    window_reviews/
  validation/
  releases/
```

The project registry is `system/projects/registry.v1.json`. Commands select a
project explicitly with `--project <project_id>`; the option is accepted before
or after the command.

## First-Project Migration

`borrowed-heaven` uses `storage_mode: legacy_v0`. Its 100 accepted chapters and
review evidence remain in their original paths because those paths and hashes
are already part of the production evidence chain. This mode is reserved for
that project. It cannot be assigned to a new project.

New projects always use `planning_profile: generic_v1` and isolated storage.
The old Borrowed Heaven planners are guarded by
`planning_profile: borrowed_heaven_v1`, so they cannot write their characters,
mechanics, or plot contracts into another project.

## Commands

```bash
python3 system/runtime/nrl.py projects
python3 system/runtime/nrl.py project-init --project-id <id> --title '<title>' --genre '<genre>'
python3 system/runtime/nrl.py project-status --project <id>
python3 system/runtime/nrl.py project-validate --project <id>
python3 system/runtime/nrl.py production-preflight --project <id>
```

Initialization never authorizes prose. A new project starts at
`concept_selection` with an empty creation-asset store and chapter registry.
Story Bible, project assets, long-form contracts, volume plans, and Owner prose
authorization must be project-specific before production can open.
