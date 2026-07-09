# NRL Corpus-to-Creation Ingestion v0.14 Plan

1. Add TDD coverage for validated review ingestion, raw-path rejection,
   evidence-ID alignment, naming schema requirements, and contamination
   rejection.
2. Implement the structured review ingest command and research catalog index.
3. Align Agent job registry packets with pipeline evidence IDs and invalidate
   stale review jobs when packet contracts change.
4. Enrich the naming schema and creation-store validator with project
   originality guardrails.
5. Refresh Studio/runtime snapshots, run full verification, and commit only
   product/runtime changes. Preserve user-generated raw evidence outside the
   commit unless it is an explicit promoted structured artifact.
