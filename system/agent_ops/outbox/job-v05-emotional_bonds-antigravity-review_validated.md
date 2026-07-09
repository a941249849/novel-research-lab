## Job ID

job-v05-emotional_bonds-antigravity-review

## Structural Review

The `emotional_bonds` creation asset family is currently minimal (readiness score: 10/100) and lacks formal structures for tracking emotional debt, multi-persona trust splits, companion lifespan decay, and collective state buffering. The current `emotional_bonds.schema.json` is highly deficient, restricted only to basic envelope fields and two basic payload properties (`bond_type` and `trust_state`) without enforcing ledger integrations, exposure risks, or retribution triggers. However, the source evidence pack provides sufficient structured DNA (18 research items, 11 cross-book mechanisms) to establish structural rules. The review focuses on establishing long-form vitality by aligning all future relationship dynamics and bond transitions with the core project theme of a heavenly debt-auditing system (《借天改命账》), transforming emotional bonds from static affinities into dynamic credit-debt relationships that dictate character actions and story milestones.

## Evidence Use

- Book Reviews: Style models are extracted from the following target sources:
  - `full-review-book-03` (*人道至尊*): Models bloodline and ancestral memory resonance, translating historical race survival into shared lineage karma and collective debt mitigation.
  - `full-review-book-04` (*仙逆*): Models time-locked soul preservation bonds (e.g., Li Muwan's residual soul in the heaven-rebellion bead), linking companion survival directly to critical path deadlines.
  - `full-review-book-08` (*完美世界*): Models tragic self-sacrifice and filial/fraternal debt (e.g., Xiao Shitou's sacrifice), where companions surrender their own life-force to pay down the protagonist's karmic deficit.
  - `full-review-book-09` (*将夜*): Models co-dependent, boundary-blurring bonds (e.g., Ning Que and桑桑) where the companion's status transition (from mortal to heavenly host) alters the global threat ledger.
  - `full-review-book-13` (*求魔*): Models master-disciple and fraternal tragedy (e.g., Ninth Peak brotherhood), where emotional bonds remain solid despite memory manipulation and existential doom.
  - `full-review-book-18` (*雪中悍刀行*): Recognised as containing only placeholder pacing metrics, representing an extraction gap (e.g., northern cavalry camaraderie and parent-child legacy做局).
- Family Emotional Bonds: Leverages `full-review-family-emotional_bonds` to define core bond categories, trust states, and relationship-decay parameters.
- Cross-Book Mechanisms: Translates mechanisms `CB-M1` to `CB-M12` (excluding `CB-M9` which is world ruins) into emotional bond rules:
  - `CB-M1`: Early-stage bonds are forged through "vulnerable mutual reliance" in high-debt starting zones.
  - `CB-M2`: Compounding relic risks force companions to act as information barriers or suffer shared exposure backlash.
  - `CB-M3`: Shifting world laws require purchasing companion lifespans from higher-level tax authorities ("州府寿库").
  - `CB-M4`: Companion soul stabilization is tied to temporal deadlines (`relic_dream_timer`).
  - `CB-M5`: Multi-persona identity masks split a companion's trust states between the protagonist's different active personas.
  - `CB-M6`: Bookkeeping/auditing skills are used to service companion debts and elevate collective social standing.
  - `CB-M7`: Existential faction conflicts force companions onto opposite sides of the tax-enforcement divide (collector vs. debtor).
  - `CB-M8`: Emotional sacrifices drive the "self-absence redemption" loop, converting high trust into ultimate systemic relief.
  - `CB-M10`: Defective mentors (`旧账老人`) introduce volatile trust dynamics due to their own hidden liabilities.
  - `CB-M11`: Mental contamination is buffered by maintaining local social anchors (`community_trust_level`).
  - `CB-M12`: Persistent companion groups share a state buffer to prevent power-scaling obsolescence.

## Originality Risk

- Direct Relationship Cloning: High risk of replicating iconic relationship formulas from the training corpus, such as a mentor in a ring swallowing energy (*Doupo*), a wife's soul trapped in a bead (*Xianni*), an interdependent maid who turns out to be a hostile god (*Jiangye*), or a tragic master-disciple structure (*Qiumo*).
- Sentimentality Overload: Risk of using generic melodrama and unmotivated sacrifice, which fails to align with the systematic auditing theme.
- Mitigation: All emotional bonds must be structurally bound to the ledger-auditing theme, representing emotional debt as actual financial/karmic balances on the state ledger. Love, loyalty, and betrayal must be translated into quantifiable risk modifiers, life-force taxes, or threat-reduction coefficients (e.g., "姻缘债", "护道盟约").

## Required Fixes

- Expand `emotional_bonds.schema.json` to include `persona_trust_map` properties to track partitioned trust levels across the protagonist's multiple active personas (CB-M5).
- Integrate `lifespan_decay_rate` and `preservation_deadline` properties to model time-locked companion survival dynamics (CB-M4).
- Add `karmic_debt_modifier` and `exposure_backlash_coefficient` to link relationship depth to state-ledger risk levels (CB-M2).
- Establish a formal transition policy defining how trust states (e.g., `devoted`, `suspicious`, `adversarial`) alter NPC behavior trees and faction alignments (CB-M7).
- Complete extraction of stub files for book-14 (*Mu Shen Ji*) and book-18 (*Xue Zhong Han Dao Xing*) to fully capture their respective mentorship and group camaraderie metrics before final family planning.
- Implement a collision blacklist blocking exact names or identical backstory configurations of relationships from the 18 training-set novels.

## Promotion Recommendation

Promote the `emotional_bonds` asset family to seed status (target: `system/creation_assets/project_assets.v0.2.json::emotional_bonds`). This promotion applies only to the structural rules, validation schemas, and state-ledger transition models, not to final dialogue trees, character rosters, or relationship story arcs.
