# Antigravity Full Corpus Review Sample

## Job ID

job-v07-full-corpus-antigravity-review

## Scope

This sample validates the v0.7 contract for full remaining corpus review. It is
not a production review and does not authorize prose generation.

## Corpus Coverage

- sample_book_id: sample-corpus-book-001
- review_state: reviewed_sample
- coverage_note: The review identifies structure, rhythm, and reusable narrative mechanisms without quoting source prose.

## Cross-Book Mechanisms

- mechanism_id: sample-mechanism-upgrade-pressure-loop
- mechanism_type: advancement_pressure
- abstraction: A long-form loop that ties scarcity, status pressure, cost, and delayed payoff.
- migration_policy: abstract_only

## Creation Asset Evidence

- characters: partial evidence
- npcs: seed evidence
- factions: partial evidence
- artifacts: seed evidence
- techniques: seed evidence
- naming: missing evidence
- emotional_bonds: partial evidence
- foreshadowing: partial evidence
- state_ledger: seed evidence

## Originality Risk

The main risk is copying surface genre symbols. The mitigation is to preserve
only abstract mechanisms and attach evidence references to every promoted idea.

## Recommended Next Ingestion

Validate this file, keep Hermes paused, and convert accepted evidence into
family-specific seed producers.

## JSON Manifest

```json
{
  "job_id": "job-v07-full-corpus-antigravity-review",
  "contract_version": "0.7",
  "review_scope": "full_remaining_corpus",
  "architecture_version": "0.4",
  "corpus_policy": {
    "raw_prose_quoted": false,
    "abstract_mechanisms_only": true
  },
  "book_reviews": [
    {
      "book_id": "sample-corpus-book-001",
      "title": "sample",
      "review_state": "reviewed_sample",
      "mechanism_count": 1,
      "risk_count": 1
    }
  ],
  "cross_book_mechanisms": [
    {
      "mechanism_id": "sample-mechanism-upgrade-pressure-loop",
      "mechanism_type": "advancement_pressure",
      "migration_policy": "abstract_only",
      "evidence_book_ids": ["sample-corpus-book-001"]
    }
  ],
  "asset_family_evidence": {
    "characters": {"status": "partial", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "npcs": {"status": "seed", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "factions": {"status": "partial", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "artifacts": {"status": "seed", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "techniques": {"status": "seed", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "naming": {"status": "missing", "reason": "sample keeps naming intentionally unpromoted"},
    "emotional_bonds": {"status": "partial", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "foreshadowing": {"status": "partial", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]},
    "state_ledger": {"status": "seed", "evidence_ids": ["sample-mechanism-upgrade-pressure-loop"]}
  },
  "originality_risks": [
    {
      "risk_id": "sample-risk-surface-copying",
      "severity": "medium",
      "mitigation": "Use abstract mechanism labels only."
    }
  ],
  "recommended_next_ingestion": {
    "action": "validate_full_corpus_review",
    "blocked_actions": ["write_prose", "execute_hermes"]
  }
}
```

