import copy
import json
import os
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from nrl_creation_schemas import FAMILIES, build_creation_schema_registry, validate_creation_asset_store


V1_SCHEMA_DIR = REPO_ROOT / "system/creation_assets/schemas/v1"


def _asset(family: str, asset_id: str, display_name: str, **payload):
    payload_key = {
        "characters": "character",
        "npcs": "npc",
        "factions": "faction",
        "artifacts": "artifact",
        "techniques": "technique",
        "naming": "naming",
        "emotional_bonds": "emotional_bond",
        "foreshadowing": "foreshadowing",
        "state_ledger": "state_ledger",
    }[family]
    return {
        "asset_id": asset_id,
        "family": family,
        "display_name": display_name,
        "lifecycle_state": "seed",
        "source_refs": ["design/story_bible.md"],
        "relationships": [],
        "constraints": ["Must remain consistent with the project design contract."],
        payload_key: payload,
    }


def v1_store():
    assets = [
        _asset(
            "characters",
            "character_lead",
            "Lead",
            narrative_role="point-of-view lead",
            goals=["complete a public task"],
            conflicts=["must choose between speed and trust"],
            arc={"starting_state": "isolated", "change_pressure": "shared risk", "target_state": "reliable partner"},
            capabilities=["field observation"],
            related_asset_ids=["faction_workshop"],
        ),
        _asset(
            "npcs",
            "npc_partner",
            "Partner",
            narrative_role="recurring collaborator",
            agenda="protect the workshop community",
            recurrence={"entry_condition": "public task begins", "return_condition": "community risk rises", "exit_condition": "arc is resolved"},
            knowledge_state="knows the local rules",
            related_asset_ids=["character_lead"],
        ),
        _asset(
            "factions",
            "faction_workshop",
            "Workshop",
            purpose="protect a shared craft and its members",
            interests=["continuity", "fair exchange"],
            pressure_sources=["outside extraction"],
            operating_rules=["members may challenge leadership"],
            related_asset_ids=["npc_partner"],
        ),
        _asset(
            "artifacts",
            "artifact_tool",
            "Tool",
            narrative_function="reveals hidden workmanship",
            acquisition="earned through a public repair",
            costs=["requires time and witness"],
            limitations=["cannot settle moral conflict"],
            evolution={"trigger": "earned trust", "next_state": "restored"},
            related_asset_ids=["technique_repair"],
        ),
        _asset(
            "techniques",
            "technique_repair",
            "Repair Method",
            narrative_function="turns observation into a costly repair",
            prerequisites=["field observation"],
            costs=["visible fatigue"],
            limitations=["requires material evidence"],
            progression={"trigger": "solves a shared problem", "next_state": "reliable practice"},
            related_asset_ids=["artifact_tool"],
        ),
        _asset(
            "naming",
            "naming_register",
            "Naming Register",
            semantic_domains=["craft", "weather"],
            formation_rules=["use concrete material nouns"],
            prohibited_collisions=["existing protagonist names"],
            examples=["rain kiln"],
        ),
        _asset(
            "emotional_bonds",
            "bond_lead_partner",
            "Lead and Partner",
            bond_type="earned alliance",
            participant_ids=["character_lead", "npc_partner"],
            current_state="guarded cooperation",
            change_triggers=["shared repair", "broken promise"],
            boundaries=["no unearned forgiveness"],
        ),
        _asset(
            "foreshadowing",
            "foreshadowing_mark",
            "Maker Mark",
            surface_presentation="a recurring maker mark",
            concealed_question="who is altering the public record",
            setup_window="opening volume",
            payoff_window="later volume",
            reveal_conditions=["two independent witnesses agree"],
            related_asset_ids=["state_ledger_reputation"],
        ),
        _asset(
            "state_ledger",
            "state_ledger_reputation",
            "Community Reputation",
            state_key="community_reputation",
            value_type="ordinal",
            owners=["faction_workshop"],
            update_rules=["public repair improves trust"],
            invariants=["changes require an observed event"],
            related_asset_ids=["faction_workshop"],
        ),
    ]
    return {
        "version": "1.0",
        "project_id": "generic-project",
        "project": "Generic Project",
        "assets": assets,
    }


class CreationSchemasV1Tests(unittest.TestCase):
    def test_v1_schema_lane_has_a_valid_schema_for_each_creation_family(self):
        registry = build_creation_schema_registry({"version": "1.0"})
        self.assertEqual(registry["version"], "1.0")
        self.assertEqual(registry["schema_lane"], "v1")
        self.assertEqual({item["family"] for item in registry["families"]}, set(FAMILIES))
        self.assertTrue(registry["summary"]["all_schemas_valid"])
        self.assertTrue(all((V1_SCHEMA_DIR / f"{family}.schema.json").is_file() for family in FAMILIES))

    def test_v1_store_accepts_domain_neutral_assets_for_all_nine_families(self):
        result = validate_creation_asset_store(v1_store())
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["schema_lane"], "v1")
        self.assertEqual(result["summary"]["asset_count"], 9)
        self.assertEqual(set(result["summary"]["family_counts"]), set(FAMILIES))

    def test_v1_requires_the_project_store_envelope(self):
        store = v1_store()
        del store["project_id"]

        result = validate_creation_asset_store(store)

        self.assertFalse(result["valid"])
        self.assertIn("store_schema_validation", {error["code"] for error in result["errors"]})

    def test_v1_rejects_duplicate_ids_names_invalid_lifecycle_and_unresolved_references(self):
        store = v1_store()
        store["assets"][0]["previous_lifecycle_state"] = "retired"
        store["assets"][0]["relationships"].append(
            {"target_id": "missing_asset", "relation_type": "depends_on"}
        )
        store["assets"][0]["character"]["related_asset_ids"].append(
            "missing_payload_asset"
        )
        duplicate = copy.deepcopy(store["assets"][1])
        duplicate["asset_id"] = store["assets"][0]["asset_id"]
        duplicate["display_name"] = store["assets"][0]["display_name"]
        store["assets"].append(duplicate)

        result = validate_creation_asset_store(store)
        codes = {error["code"] for error in result["errors"]}
        self.assertFalse(result["valid"])
        self.assertTrue(
            {"duplicate_asset_id", "name_collision", "invalid_lifecycle_transition", "unresolved_reference"}.issubset(codes)
        )

    def test_legacy_v02_store_stays_on_legacy_schema_lane(self):
        legacy_path = REPO_ROOT / "system/creation_assets/project_assets.v0.2.json"
        legacy = json.loads(legacy_path.read_text(encoding="utf-8"))
        result = validate_creation_asset_store(legacy)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["schema_lane"], "legacy_v0.2")

    def test_active_project_result_reports_the_actual_runtime_store_path(self):
        with mock.patch.dict(os.environ, {"NRL_PROJECT_ID": "hundred-crafts-night-procession"}):
            result = validate_creation_asset_store()
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["schema_lane"], "v1")
        self.assertEqual(
            result["store_path"],
            "projects/hundred-crafts-night-procession/creation_assets/project_assets.json",
        )


if __name__ == "__main__":
    unittest.main()
