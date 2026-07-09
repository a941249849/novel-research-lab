## Job ID

job-v05-characters-antigravity-review

## Structural Review

The characters creation asset family is currently minimal (readiness score: 10/100), as the characters.schema.json schema is restricted to basic envelope fields and payload properties (role and growth_stage) without enforcing state-ledger connections, exposure risks, mental stability/sanity metrics, or identity mask rules. However, the source evidence pack provides sufficient structured DNA (18 research items, 12 cross-book mechanisms) to establish formal structural rules. The review focuses on establishing long-form vitality by aligning the protagonist's growth curve and identity states with the project's central theme of a heavenly debt-auditing system (《借天改命账》), transforming character progression from standard level-based growth into a dynamic debt-mitigation cycle where every advancement scales with state-ledger variables.

## Evidence Use

- Book Reviews: Style models and character growth patterns are extracted from:
  - full-review-book-01 (*一念永恒*): Models protagonist growth with a comedic/paranoid base (fear of death driving progression), transitioning into self-sacrificing protection of companions under high stress. Since it is a stub, it represents an extraction gap.
  - full-review-book-08 (*完美世界*): Models protagonist growth under severe structural deprivation (stolen bone/childhood tragedy) and his rise as an independent pathfinder ("以自身为道种") who faces ultimate isolation. Since it is a stub, it represents an extraction gap.
  - full-review-book-15 (*蛊真人*): Models protagonist growth with absolute rationality, discarding all moral constraints in favor of direct utility optimization (rational_utility_index) to exploit system rules.
- Family Characters: Leverages full-review-family-characters to define protagonist identity envelopes, growth stage criteria, and behavioral constraints.
- Cross-Book Mechanisms: Translates mechanisms CB-M1 to CB-M12 into characters structural rules:
  - CB-M1 (Weakness Start & Core Deprivation): Establishes the protagonist's starting state as an indebted commoner under a "残籍欠命登记".
  - CB-M2 (Compounding Relic with High Exposure Risk): Defines characters' reliance on the "残命灯盏" where usage increases exposure parameters.
  - CB-M3 (Cognitive Iceberg Maps): Drives protagonist's growth stages to correspond to discoveries of higher-level celestial ledgers (e.g., "州府寿库").
  - CB-M4 (Limit Promise & External Countdown): Imposes strict temporal commitments (e.g., 三年之约) that cause physical or soul backlash upon failure.
  - CB-M5 (Multi-Persona Identity Masking): Dictates protagonist's ability to use aliases (e.g., "厉飞雨" or "格尔曼") to isolate threat exposure below specific thresholds.
  - CB-M6 (Auxiliary Profession Status): Integrates secondary roles (such as ledger clerk or auditor) to resolve conflicts without relying solely on combat.
  - CB-M7 (Existential Faction Collisions): Structures conflicts as systemic resistance to "收债官" from the "命籍衙" rather than personal vendettas.
  - CB-M8 (Self-Absence Redemption): Sets the narrative climax where the protagonist sacrifices/erases his own existence to resolve the ultimate debt.
  - CB-M9 (Ancient Epoch Ruins): Governs how protagonist interacts with ancient ruins to recover forgotten ledger tools and old-world debt records.
  - CB-M10 (Defective Mentor Sanctuary): Pairs the protagonist with a burdened guide ("旧账老人") who introduces instruction at the cost of additional debt risk.
  - CB-M11 (Acting Assimilation & Contamination Balance): Models the requirement that the protagonist must balance sanity by playing social roles to build trust (community_trust_level).
  - CB-M12 (Ensemble Companion Cohort Ingestion): Restricts the protagonist from ascending alone, forcing him to pull a cohort of companions through the ledger system.
- Target Mechanisms:
  - mechanism-dpcq-m1 (公开测评羞辱): Models the initial public humiliation/testing event that establishes the protagonist's starting deficit (the stone tablet test).
  - mechanism-dpcq-m2 (期限承诺驱动): Models the 三年之约 as a concrete temporal commitment that forces rapid progression.

## Originality Risk

- Direct Character and Role Cloning: High risk of reproducing recognizable character names, roles, or relationships from the training corpus, such as "白小纯" (*Yinian Yongheng*), "石昊" (*Wanmei Shijie*), "方源" (*Guzhenren*), or "药老" (*Doupo*).
- Archetype Repetition: High risk of generating standard cultivation protagonists (e.g., arrogant young masters, simple revenge-driven cultivators) without a systemic theme.
- Mitigation: All protagonist growth stages and roles must be structurally bound to the debt-auditing system. Character progression must be mapped to accounting-themed mechanics (e.g., "记账人", "查账使", "改账仙尊") rather than copying standard cultivation level names. The schema must enforce a collision blacklist blocking any proprietary character names, unique relics, or progression titles from the 18 training-set novels.

## Required Fixes

- Expand characters.schema.json to require properties like debt_balance, exposure_rate, and sanity_level under the character payload to enforce connection to state-ledger variables (CB-M2, CB-M5).
- Add a structured identity_masks property to the schema to define the protagonist's alias limit and exposure parameters (CB-M5).
- Define a growth_policy that restricts growth stage transitions to depend on specific debt-clearing or audit-resolution states rather than simple level metrics (CB-M4).
- Complete the full extraction of stubs book-01 (*一念永恒*) and book-08 (*完美世界*) to resolve the evidence gap before final planning.
- Implement a strict collision blacklist blocking all proprietary character names, titles, and relics from the 18 training-set novels to enforce the originality policy.

## Promotion Recommendation

Promote the characters asset family to seed status (target: system/creation_assets/project_assets.v0.2.json::characters). This promotion applies only to the structural rules, validation schemas, and growth policy, not to final character sheets, technique trees, or dialog lines.
