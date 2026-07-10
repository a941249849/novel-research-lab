# NRL Verifiable Deep Reading v0.18 Implementation Plan

1. Add failing tests for contiguous chunk planning, source hash binding,
   response validation, coverage calculation, resumability, and truthful status.
2. Implement `nrl_deep_read.py` with plan, status, validation, dispatch manifest,
   per-book synthesis validation, and cross-book validation.
3. Add CLI commands `deep-read-plan`, `deep-read-status`,
   `deep-read-validate-chunk`, and `deep-read-validate-all`.
4. Downgrade v0.8 product wording from full-reading proof to sampled-access
   proof without deleting historical artifacts.
5. Add deep-reading status to system-check and Studio data. Corpus depth is a
   blocking production-readiness check until v0.18 verifies.
6. Repair stale tests for expanded creation assets and current Hermes adapter
   state; keep socket tests separately identifiable when the environment blocks
   local bind.
7. Generate the 18-book chunk plan, dispatch Antigravity in resumable batches,
   validate each response, and retry invalid or incomplete chunks.
8. Build and validate 18 per-book syntheses and one cross-book distillation.
9. Rebuild research indexes, run an Antigravity project-impact review for
   `《借天改命账》`, and promote only approved changes.
10. Run a multi-scene Hermes stress test followed by Antigravity literary audit,
    full regression, Studio build, `git diff --check`, commit, and push.
