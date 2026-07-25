## Job ID

job-v05-factions-antigravity-review

## Structural Review

The factions creation asset family is currently minimal (readiness score: 12/100) as the `factions.schema.json` is restricted only to basic fields (`interest` and `pressure_level`) without enforcing systemic faction relationships, administrative roles, member cohorts, or debt liabilities. However, the source evidence pack provides sufficient structured DNA (18 research items, 12 cross-book mechanisms) to establish formal structural rules. The review focuses on establishing long-form vitality by aligning all faction behaviors and conflicts with the core project theme of a heavenly debt-auditing system (《借天改命账》), transforming factions from generic antagonistic clans into legalistic institutional actors—specifically "命籍衙" (Fate Registries) and "收债官" (Debt Collectors)—whose actions are driven by and recorded in state-ledger parameters.

## Evidence Use

- Book Reviews: Style models and structural patterns are extracted from:
  - `full-review-book-02` (*不死不灭*): Models ideological faction splits across epochs, focusing on the ultimate clash between太古神魔 (ancient gods and demons) and the celestial order. Since it is a stub, it represents an extraction gap.
  - `full-review-book-03` (*人道至尊*): Models systemic ethnic and species-level oppression under the cosmic 万族神朝 (Ten Thousand Clans Divine Court), treating weaker populations as food and resources.
  - `full-review-book-07` (*大主宰*): Models joint defense alliances against external threat invasions (域外邪族) and strict ancestral rules (浮屠古族) enforcing family separations. Since it is a stub, it represents an extraction gap.
  - `full-review-book-09` (*将夜*): Models absolute ideological and theological control by the Xiling Divine Hall (西陵神殿) enforcing compliance with the divine order of Haotian. Since it is a stub, it represents an extraction gap.
  - `full-review-book-11` (*武动乾坤*): Models infiltration by external corruption (异魔) turning local sects into colluders, forcing the formation of alliance networks. Since it is a stub, it represents an extraction gap.
  - `full-review-book-12` (*永生*): Models major sects exploiting lower-tier disciples for willpower and resource accumulation under the absolute rule of the 造化天庭 (Creation Heavenly Court). Since it is a stub, it represents an extraction gap.
  - `full-review-book-14` (*牧神记*): Models the state-level reformist movement of the Yankang Empire (延康国) challenging the monopoly of the ancient Heavenly Court (古神天庭), integrating factions into public welfare and education.
  - `full-review-book-15` (*蛊真人*): Models survival-driven clan structures (古月一族) and the supreme Heavenly Court (天庭) controlling human destiny through Fate Gu.
  - `full-review-book-17` (*遮天*): Models Forbidden Zones (生命禁区) executing periodic cleansings (黑暗动乱) to harvest life span, while Holy Lands and Divine Dynasties monopolize resources.
  - `full-review-book-18` (*雪中悍刀行*): Models military-political tension between the central court (离阳王朝) and the frontier (北凉府), combined with higher-level entities (仙人) manipulating human fate.
- Family Factions: Leverages `full-review-family-factions` to categorize faction types (e.g., interests, power structures, internal exploitation, and external existential defense) and structure faction evolution phases.
- Cross-Book Mechanisms: Translates mechanisms `CB-M1` to `CB-M12` (excluding `CB-M5`, `CB-M6`, `CB-M7`, `CB-M8`, `CB-M9`) into faction rules:
  - `CB-M1`: Factions enforce starting deprivation and registration constraints (such as the "残籍欠命登记") to lock the protagonist into the local administrative grid.
  - `CB-M2`: Compounding relic usage triggers faction surveillance and threat exposure, matching asset growth with increased pursuit risk.
  - `CB-M3`: Map transitions expose higher-level tax collectors ("州府寿库"), altering the faction context and resolving lower-level mysteries.
  - `CB-M4`: Factions enforce explicit external deadlines, tax collections, or life-force calls to drive narrative momentum.
  - `CB-M10`: Unstable, debt-ridden mentors ("旧账老人") bring latent faction enforcers to the protagonist's sanctuary, creating risk.
  - `CB-M11`: Faction integration is bound to role-playing and sanity balances in the state ledger.
  - `CB-M12`: High-level faction migration or ascension requires managing and safeguarding the companion cohort.

## Originality Risk

- Direct Tropes Cloning: High risk of copying recognizable faction names or structures, such as a soul-hunting faction (*Hundian* from *Doupo Cangqiong*), life-harvesting forbidden zones (*Shengming Jinqu* from *Zhetian*), a destiny-controlling heavenly court (*Tianting* from *Gu Zhenren*), or a centralized military frontier (*Beiliang* from *Snowy Path Hero*).
- Generic Clan Structures: Risk of falling back into standard cultivation clans or sects that compete for resources without systemic, thematic meaning.
- Mitigation: All factions must be structurally bound to the ledger-auditing theme, representing them as "命籍衙" (Fate Registries) and "收债官" (Debt Collectors). Factions enforce legalistic "命税" (life-span tax) rather than arbitrary violence, and their actions must be driven by and recorded in the state ledger using custom properties (e.g., `provincial_troop_loyalty`, `court_provocation_meter`) rather than mimicking the specific plot points of the source materials.

## Required Fixes

- Expand `factions.schema.json` to include `tax_enforcement_role`, `associated_ledger_states`, and `cohort_capacity` properties to link faction interactions directly to state-ledger variables (such as `community_trust_level` and `protagonist_exposure_rate`) (CB-M2, CB-M3).
- Define a `threat_exposure_coefficient` in the schema to model how faction hostility scales with the protagonist's asset accumulation and exposure (CB-M2).
- Require a structured lifecycle policy for factions defining establishment, alliance shifts, territorial expansion, and retirement/dissolution conditions (CB-M3, CB-M12).
- Resolve the evidence gap by completing extraction for stubs `book-02` (*不死不灭*), `book-07` (*大主宰*), `book-09` (*将夜*), `book-11` (*武动乾坤*), and `book-12` (*永生*).
- Add a collision blacklist blocking any proprietary faction names, structures, or terminology from the 18 training-set novels.

## Promotion Recommendation

Promote the `factions` asset family to seed status (target: `system/creation_assets/project_assets.v0.2.json::factions`). This promotion applies only to the structural rules, validation schemas, and state-ledger integration models, not to final faction lists, dossiers, or specific plot outlines.
