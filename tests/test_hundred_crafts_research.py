import json
import sys
import unittest
from pathlib import Path

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))

from nrl_research_assets import build_research_asset_catalog
from nrl_projects import build_project_status


CANDIDATE_ROOT = (
    ROOT
    / "system/research_assets/project_candidates/hundred-crafts-night-procession"
)


class HundredCraftsResearchTests(unittest.TestCase):
    def _read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_twelve_domain_source_map_is_schema_valid(self) -> None:
        schema = self._read(
            ROOT
            / "system/research_assets/schemas/candidate_craft_source_map.schema.json"
        )
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(source_map, schema)

    def test_expanded_source_ecology_is_schema_valid_and_covers_all_domains(self) -> None:
        schema = self._read(
            ROOT
            / "system/research_assets/schemas/candidate_source_ecology.schema.json"
        )
        ecology = self._read(
            CANDIDATE_ROOT / "source-ecology-and-regional-atlas.v0.2.json"
        )
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(ecology, schema)
        self.assertEqual(
            {item["tier"] for item in ecology["source_tiers"]},
            {"A", "B", "C", "D", "E"},
        )
        mapped_domains = {
            domain_id
            for lens in ecology["regional_lenses"]
            for domain_id in lens["craft_domain_ids"]
        }
        self.assertEqual(
            mapped_domains,
            {domain["domain_id"] for domain in source_map["domains"]},
        )

    def test_p0_regional_evidence_cards_are_schema_valid_and_honest(self) -> None:
        schema = self._read(
            ROOT
            / "system/research_assets/schemas/candidate_regional_evidence_cards.schema.json"
        )
        cards = self._read(
            CANDIDATE_ROOT / "regional-evidence-cards.p0.v0.1.json"
        )
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(cards, schema)
        self.assertFalse(cards["prose_authorized"])
        self.assertEqual(len(cards["routes"]), 4)
        card_ids = []
        for route in cards["routes"]:
            self.assertEqual(route["status"], "triangulated")
            self.assertGreaterEqual(len(route["cards"]), 4)
            self.assertTrue(any(card["source_tier"] == "C" for card in route["cards"]))
            self.assertTrue(route["route_synthesis"]["remaining_debt"])
            for card in route["cards"]:
                card_ids.append(card["card_id"])
                if card["source_tier"] in {"D", "E"}:
                    self.assertEqual(card["claim_status"], "discovery_lead")
        self.assertEqual(len(card_ids), len(set(card_ids)))

    def test_p1_regional_evidence_cards_are_schema_valid_and_honest(self) -> None:
        schema = self._read(
            ROOT
            / "system/research_assets/schemas/candidate_regional_evidence_cards_p1.schema.json"
        )
        cards = self._read(
            CANDIDATE_ROOT / "regional-evidence-cards.p1.v0.1.json"
        )
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.validate(cards, schema)
        self.assertFalse(cards["prose_authorized"])
        self.assertEqual(len(cards["routes"]), 5)
        self.assertEqual(
            {route["regional_lens_id"] for route in cards["routes"]},
            {
                "shanxi_shaanxi_gansu",
                "lingnan_pearl_river",
                "southwest_highlands",
                "northeast_forests",
                "plateau_oasis_frontier",
            },
        )
        status_by_lens = {
            route["regional_lens_id"]: route["status"] for route in cards["routes"]
        }
        self.assertEqual(status_by_lens["lingnan_pearl_river"], "triangulated")
        self.assertEqual(status_by_lens["plateau_oasis_frontier"], "triangulated")
        for lens_id in {
            "shanxi_shaanxi_gansu",
            "lingnan_pearl_river",
            "southwest_highlands",
            "northeast_forests",
            "plateau_oasis_frontier",
        }:
            self.assertEqual(status_by_lens[lens_id], "triangulated")
        for route in cards["routes"]:
            self.assertGreaterEqual(len(route["cards"]), 3)
            self.assertTrue(route["route_synthesis"]["remaining_debt"])
            if route["status"] == "triangulated":
                self.assertGreaterEqual(len(route["cards"]), 8)
                authoritative = sum(
                    card["source_tier"] in {"A", "B"} for card in route["cards"]
                )
                self.assertGreaterEqual(authoritative / len(route["cards"]), 0.5)

    def test_domains_and_sources_are_unique_and_authoritative(self) -> None:
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        domain_ids = [item["domain_id"] for item in source_map["domains"]]
        self.assertEqual(len(domain_ids), 12)
        self.assertEqual(len(set(domain_ids)), 12)
        source_ids = []
        for domain in source_map["domains"]:
            self.assertGreaterEqual(len(domain["sources"]), 2)
            for source in domain["sources"]:
                self.assertTrue(source["url"].startswith("https://"))
                self.assertIn(
                    source["quality"],
                    {
                        "primary_institution",
                        "official_catalogue",
                        "museum_research",
                        "scholarly",
                    },
                )
                source_ids.append(source["source_id"])
        self.assertEqual(len(source_ids), len(set(source_ids)))

    def test_pilot_claims_resolve_to_source_map(self) -> None:
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        pilot = self._read(CANDIDATE_ROOT / "pilot-three-crafts-synthesis.v0.1.json")
        known_sources = {
            source["source_id"]
            for domain in source_map["domains"]
            for source in domain["sources"]
        }
        self.assertEqual(len(pilot["pilot_domains"]), 3)
        for domain in pilot["pilot_domains"]:
            for fact in domain["verified_facts"]:
                self.assertTrue(set(fact["source_ids"]) <= known_sources)
            for inference in domain["fictional_inferences"]:
                self.assertEqual(
                    inference["fiction_status"], "invented_for_candidate"
                )
                self.assertTrue(set(inference["derived_from"]) <= known_sources)

    def test_initialized_project_still_does_not_authorize_prose(self) -> None:
        contract = self._read(CANDIDATE_ROOT / "research_contract.v0.1.json")
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        pilot = self._read(CANDIDATE_ROOT / "pilot-three-crafts-synthesis.v0.1.json")
        history = self._read(CANDIDATE_ROOT / "world-history-skeleton.v0.1.json")
        self.assertTrue(contract["project_initialized"])
        self.assertFalse(contract["prose_authorized"])
        self.assertFalse(source_map["project_initialization_authorized"])
        self.assertFalse(source_map["prose_authorized"])
        self.assertFalse(pilot["prose_authorized"])
        self.assertFalse(pilot["gate_result"]["project_initialization_allowed"])
        self.assertFalse(pilot["gate_result"]["prose_allowed"])
        self.assertFalse(history["historical_claim"])
        self.assertFalse(history["prose_authorized"])
        self.assertFalse(history["next_gate"]["project_initialization_allowed"])
        self.assertFalse(history["next_gate"]["prose_allowed"])

    def test_world_history_has_causal_expansion_and_no_tradition_binary(self) -> None:
        history = self._read(CANDIDATE_ROOT / "world-history-skeleton.v0.1.json")
        self.assertEqual(len(history["eras"]), 5)
        self.assertEqual(len(history["expansion_layers"]), 5)
        for era in history["eras"]:
            self.assertTrue(era["institutional_gain"])
            self.assertTrue(era["hidden_cost"])
            self.assertTrue(era["transition_cause"])
        self.assertIn(
            "传统和现代都只是工具",
            "".join(history["foundational_axioms"]),
        )
        self.assertIn(
            "不把现代工程写成破坏传统的单一反派。",
            history["guardrails"],
        )

    def test_civilization_library_resolves_domains_sources_and_routes(self) -> None:
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        p0 = self._read(CANDIDATE_ROOT / "regional-evidence-cards.p0.v0.1.json")
        p1 = self._read(CANDIDATE_ROOT / "regional-evidence-cards.p1.v0.1.json")
        library = self._read(
            CANDIDATE_ROOT / "civilization-mechanism-library.v0.1.json"
        )
        known_domains = {item["domain_id"] for item in source_map["domains"]}
        known_refs = {
            source["source_id"]
            for domain in source_map["domains"]
            for source in domain["sources"]
        }
        known_refs |= {
            card["card_id"]
            for payload in (p0, p1)
            for route in payload["routes"]
            for card in route["cards"]
        }
        known_routes = {
            route["route_id"]
            for payload in (p0, p1)
            for route in payload["routes"]
        }
        mechanisms = library["mechanisms"]
        self.assertEqual(len(mechanisms), 12)
        self.assertEqual(
            {item["craft_domain_id"] for item in mechanisms}, known_domains
        )
        self.assertEqual(
            len({item["mechanism_id"] for item in mechanisms}), len(mechanisms)
        )
        for mechanism in mechanisms:
            self.assertTrue(set(mechanism["source_refs"]) <= known_refs)
            self.assertTrue(mechanism["fiction_boundary"])
        self.assertEqual(len(library["regional_adapters"]), 9)
        self.assertTrue(
            all(
                item["evidence_route"] in known_routes
                for item in library["regional_adapters"]
            )
        )
        self.assertTrue(library["project_initialized"])
        self.assertFalse(library["prose_authorized"])

    def test_series_blueprint_is_causal_bounded_and_research_linked(self) -> None:
        p0 = self._read(CANDIDATE_ROOT / "regional-evidence-cards.p0.v0.1.json")
        p1 = self._read(CANDIDATE_ROOT / "regional-evidence-cards.p1.v0.1.json")
        library = self._read(
            CANDIDATE_ROOT / "civilization-mechanism-library.v0.1.json"
        )
        blueprint = self._read(CANDIDATE_ROOT / "series-blueprint.v0.3.json")
        known_routes = {
            route["route_id"]
            for payload in (p0, p1)
            for route in payload["routes"]
        }
        known_mechanisms = {
            item["mechanism_id"] for item in library["mechanisms"]
        }
        known_protocols = {
            item["protocol_id"] for item in library["cross_mechanism_protocols"]
        }
        volumes = blueprint["volumes"]
        self.assertEqual([item["volume"] for item in volumes], list(range(1, 16)))
        used_mechanisms = {
            mechanism
            for volume in volumes
            for mechanism in volume["primary_mechanisms"]
        }
        self.assertTrue(known_mechanisms <= used_mechanisms)
        self.assertTrue(used_mechanisms <= known_mechanisms | known_protocols)
        for volume in volumes:
            self.assertTrue(set(volume["evidence_routes"]) <= known_routes)
            self.assertTrue(volume["irreversible_change"])
            self.assertTrue(volume["new_debt"])
            self.assertTrue(volume["blocking_research"])
        scale = blueprint["positioning"]["scale"]
        self.assertEqual(scale["planned_volumes"], 15)
        self.assertLess(scale["planned_total_chinese_characters_range"][0], scale["planned_total_chinese_characters_range"][1])
        self.assertTrue(blueprint["project_initialized"])
        self.assertFalse(blueprint["prose_authorized"])
        self.assertTrue(blueprint["continuous_mainline"]["mid_series_escalation"])
        self.assertNotIn("named_burden", used_mechanisms)
        self.assertTrue(blueprint["gate_result"]["blocking_debt"])

    def test_compiled_library_and_blueprint_are_queryable(self) -> None:
        library_catalog = build_research_asset_catalog(
            {"asset_type": "candidate_civilization_library"}
        )
        self.assertEqual(library_catalog["summary"]["returned"], 1)
        library = library_catalog["items"][0]
        self.assertEqual(library["mechanism_count"], 12)
        self.assertEqual(library["regional_adapter_count"], 9)
        self.assertTrue(library["project_initialization_authorized"])
        self.assertFalse(library["prose_authorized"])

        blueprint_catalog = build_research_asset_catalog(
            {"asset_type": "candidate_series_blueprint"}
        )
        self.assertEqual(blueprint_catalog["summary"]["returned"], 1)
        blueprint = blueprint_catalog["items"][0]
        self.assertEqual(blueprint["volume_count"], 15)
        self.assertEqual(blueprint["review_state"], "initialized_designing")
        self.assertTrue(blueprint["project_initialization_authorized"])
        self.assertFalse(blueprint["prose_authorized"])

    def test_project_returns_to_owner_gate_during_semantic_rework(self) -> None:
        status = build_project_status("hundred-crafts-night-procession")
        self.assertEqual(status["status"], "owner_gate")
        self.assertTrue(status["design_contracts_present"])
        self.assertEqual(status["assets"], 38)
        self.assertFalse(status["content_authorized"])
        self.assertFalse(status["ready_for_prose"])
        self.assertTrue(status["continuity_test_passed"])
        self.assertEqual(status["next_action"], "await explicit production readiness decision")

    def test_candidate_assets_do_not_reference_raw_novel_corpus(self) -> None:
        for path in CANDIDATE_ROOT.glob("*.json"):
            self.assertNotIn("novel_training_set/", path.read_text(encoding="utf-8"))

    def test_expert_enrichment_keeps_untranscribed_video_as_leads(self) -> None:
        source_map = self._read(CANDIDATE_ROOT / "twelve-crafts-source-map.v0.1.json")
        enrichment = self._read(
            CANDIDATE_ROOT / "expert-source-enrichment.v0.1.json"
        )
        known_sources = {
            source["source_id"]
            for domain in source_map["domains"]
            for source in domain["sources"]
        }
        self.assertFalse(enrichment["prose_authorized"])
        self.assertEqual(len(enrichment["tracks"]), 3)
        for track in enrichment["tracks"]:
            self.assertIn(track["authoritative_addition"]["source_id"], known_sources)
            self.assertTrue(track["blocking_debt"])
            self.assertTrue(track["questions_for_practitioner"])
            for lead in track["audiovisual_leads"]:
                self.assertFalse(lead["subtitle_available"])
                self.assertIn("lead_only", lead["evidence_status"])
        self.assertFalse(enrichment["gate_result"]["sufficient_for_prose"])

    def test_concept_stress_test_has_required_longform_dimensions(self) -> None:
        stress = self._read(CANDIDATE_ROOT / "concept-stress-test.v0.1.json")
        self.assertEqual(len(stress["power_system"]["competency_axes"]), 6)
        self.assertEqual(len(stress["core_ensemble"]), 5)
        self.assertEqual(len(stress["competing_solutions"]), 4)
        self.assertEqual(len(stress["fifteen_volume_mechanism_evolution"]), 15)
        chapters = stress["first_thirty_chapter_summary"]
        self.assertEqual([item["chapter"] for item in chapters], list(range(1, 31)))
        self.assertTrue(all(item["irreversible_change"] for item in chapters))
        self.assertTrue(stress["gate_result"]["fieldwork_debt_blocks_project_initialization"])
        self.assertFalse(stress["gate_result"]["prose_allowed"])

    def test_medical_adviser_contract_blocks_unsupported_health_content(self) -> None:
        contract = self._read(CANDIDATE_ROOT / "medical-adviser-contract.v0.1.json")
        self.assertFalse(contract["prose_authorized"])
        self.assertEqual(contract["gate_scope"], "volume_9_and_any_health_claim")
        self.assertGreaterEqual(len(contract["required_specialists"]), 3)
        self.assertIn("现实医疗建议", "".join(contract["hard_prohibitions"]))
        self.assertTrue(contract["approval_record"]["required_before_volume_9_detail_outline"])
        self.assertFalse(contract["approval_record"]["approved"])
        catalog = build_research_asset_catalog(
            {"asset_type": "candidate_safety_contract"}
        )
        self.assertEqual(catalog["summary"]["returned"], 1)
        self.assertEqual(catalog["items"][0]["review_state"], "expert_pending")
        self.assertFalse(catalog["items"][0]["prose_authorized"])

    def test_cultural_fieldwork_contract_separates_evidence_from_prose_permission(self) -> None:
        contract = self._read(CANDIDATE_ROOT / "cultural-fieldwork-contract.v0.1.json")
        self.assertFalse(contract["prose_authorized"])
        self.assertEqual(
            contract["status"],
            "web_evidence_ready_practitioner_verification_pending",
        )
        self.assertGreaterEqual(len(contract["evidence"]), 5)
        self.assertTrue(contract["fiction_boundary"]["required_disclosure_in_design"])
        self.assertGreaterEqual(
            len(contract["approval_record"]["remaining_debt"]),
            3,
        )
        catalog = build_research_asset_catalog(
            {"asset_type": "candidate_cultural_fieldwork_contract"}
        )
        self.assertEqual(catalog["summary"]["returned"], 1)
        self.assertEqual(catalog["items"][0]["review_state"], "practitioner_pending")
        self.assertFalse(catalog["items"][0]["prose_authorized"])

    def test_candidate_craft_domains_are_queryable_in_research_catalog(self) -> None:
        catalog = build_research_asset_catalog(
            {"category": "木作与古建营造"}
        )
        candidate_items = [
            item
            for item in catalog["items"]
            if item["asset_type"] == "candidate_craft_research"
        ]
        self.assertEqual(len(candidate_items), 1)
        item = candidate_items[0]
        self.assertEqual(item["candidate_id"], "hundred-crafts-night-procession")
        self.assertEqual(item["domain_id"], "timber_architecture")
        self.assertGreaterEqual(item["source_count"], 2)
        self.assertEqual(item["field_validation_status"], "strengthened")
        self.assertIn("古建修复", item["blocking_debt"])
        self.assertFalse(item["project_initialization_authorized"])
        self.assertFalse(item["prose_authorized"])

    def test_source_ecology_is_queryable_without_authorizing_prose(self) -> None:
        catalog = build_research_asset_catalog(
            {"asset_type": "candidate_source_ecology"}
        )
        self.assertEqual(catalog["summary"]["returned"], 1)
        item = catalog["items"][0]
        self.assertEqual(item["source_tier_count"], 5)
        self.assertGreaterEqual(item["source_channel_count"], 10)
        self.assertGreaterEqual(item["regional_lens_count"], 9)
        self.assertFalse(item["project_initialization_authorized"])
        self.assertFalse(item["prose_authorized"])

    def test_regional_routes_are_queryable_across_collection_waves(self) -> None:
        catalog = build_research_asset_catalog(
            {"asset_type": "candidate_regional_evidence"}
        )
        self.assertEqual(catalog["summary"]["returned"], 9)
        p0_items = [
            item for item in catalog["items"]
            if item["collection_status"] == "p0_seed_collection"
        ]
        p1_items = [
            item for item in catalog["items"]
            if item["collection_status"] == "p1_seed_collection"
        ]
        self.assertEqual(len(p0_items), 4)
        self.assertEqual(len(p1_items), 5)
        self.assertTrue(all(item["review_state"] == "triangulated" for item in p0_items))
        self.assertEqual(
            sum(item["review_state"] == "triangulated" for item in p1_items), 5
        )
        self.assertEqual(
            sum(item["review_state"] == "triangulation_pending" for item in p1_items), 0
        )
        self.assertTrue(all(item["card_count"] >= 3 for item in catalog["items"]))
        self.assertTrue(all(item["remaining_debt"] for item in catalog["items"]))
        self.assertTrue(all(not item["prose_authorized"] for item in catalog["items"]))


if __name__ == "__main__":
    unittest.main()
