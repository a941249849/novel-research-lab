## Job ID

job-v05-npcs-antigravity-review

## Structural Review

The npcs creation asset family is currently minimal (readiness score: 12/100), as the npcs.schema.json schema is restricted to basic envelope fields and lacks dedicated fields for faction alignments, information states, and state-ledger integrations. However, the source evidence pack provides sufficient structured DNA (18 research items, 11 cross-book mechanisms) to establish structural rules. The review focuses on aligning NPC roles with the heavenly debt-auditing system (《借天改命账》), dividing NPCs into debt collectors, debtors, and protectors whose relationships scale dynamically with state-ledger parameters.

## Evidence Use

- Book Reviews: Style models are extracted from full-review-book-03 (existential faction collisions and ancestral heritage in *Ren Dao Zhi Zun*), full-review-book-10 (time-bound pressure enforcers and resource-compensating mentors in *Doupo*), full-review-book-13 (tragically flawed mentors and systemic adversaries driving self-absence redemption in *Qiu Mo*), and full-review-book-17 (anti-siege combatants and scaling cohorts in *Zhetian*). The stub files full-review-book-14 (*Mu Shen Ji*) and full-review-book-18 (*Xue Zhong Han Dao Xing*) are recognized as containing only placeholder pacing metrics, representing an extraction gap.
- Family NPCs: Leverages full-review-family-npcs to define roles such as debt enforcers, ledger keepers, and local townspeople.
- Cross-Book Mechanisms: Translates mechanisms CB-M1 to CB-M12 (excluding CB-M9) into NPC behavioral rules. CB-M1 and CB-M4 define initial oppressors (e.g., debt collectors from "命籍衙") enforcing countdown pressure. CB-M2 and CB-M5 establish NPCs as threat vectors monitoring the protagonist's "残命灯盏" exposure, requiring information barriers. CB-M3 and CB-M7 shape high-level NPCs as systemic exploiters ("收债官"). CB-M10 and CB-M11 define unstable mentors and community trust anchors, while CB-M12 structures a persistent companion cohort.

## Originality Risk

- Direct Character Cloning: High risk of reproducing names and identities from the training corpus, such as "药老", "纳兰嫣然", "厉飞雨", "徐凤年", or "九幽".
- Archetype Repetition: Risk of generating standard face-slapping antagonists (e.g., arrogant young masters) without systemic motivations.
- Mitigation: All generated NPCs must be bound to the ledger-auditing theme, translating generic cultivation opponents into legalistic auditing agents (e.g., "命籍判官", "讨债执事") who operate under consistent rules of life-force tax.

## Required Fixes

- Expand npcs.schema.json to include faction_id and information_state properties to manage persona-based information barriers under CB-M5.
- Integrate ledger_debt_balance and trust_metric properties into the schema to tie NPC behaviors to state-ledger variables.
- Detail the recurrence_policy with a structured lifecycle policy defining map transitions, power scaling, and retirement conditions.
- Complete full extraction of stubs book-14 and book-18 to resolve the evidence gap before final planning.
- Implement a collision blacklist blocking any proprietary character names or titles from the 18 training-set novels.

## Promotion Recommendation

Promote the npcs asset family to seed status (target: system/creation_assets/project_assets.v0.2.json::npcs). This promotion applies only to the structural rules and validation schemas, not to final character rosters or dialogue scenes.
