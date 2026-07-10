import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from nrl_final_assets import (
    build_final_asset_promotion_readiness,
    promote_final_asset_bundle,
    validate_final_asset_bundle,
    validate_final_asset_payload,
)


CANDIDATE_PATH = REPO_ROOT / "system/agent_ops/inbox/hermes-final-asset-bundle-v015.json"
STORE_PATH = REPO_ROOT / "system/creation_assets/project_assets.v0.2.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class FinalAssetPromotionV015Tests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_json(CANDIDATE_PATH)
        self.promoted_store = load_json(STORE_PATH)
        candidate_ids = {asset["asset_id"] for asset in self.bundle["assets"]}
        self.store = {
            **self.promoted_store,
            "assets": [
                asset
                for asset in self.promoted_store["assets"]
                if asset["asset_id"] not in candidate_ids
            ],
        }
        self.decision = {
            "decision_id": "owner_gate_final_assets_001",
            "decision_type": "authorize_final_asset_generation",
            "authorized_scope": ["generate_final_creation_assets"],
            "forbidden_scope": ["generate_novel_prose"],
            "expires_after_mission": "phase2f_final_asset_generation",
        }

    def test_candidate_is_exact_family_safe_and_schema_valid(self):
        result = validate_final_asset_payload(self.bundle, self.store)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["candidate_asset_count"], 9)
        self.assertEqual(result["combined_asset_count"], len(self.store["assets"]) + 9)

    def test_promoted_candidate_validation_is_idempotent(self):
        result = validate_final_asset_bundle(str(CANDIDATE_PATH))
        self.assertTrue(result["valid"], result["errors"])
        self.assertTrue(result["already_promoted"])

    def test_candidate_rejects_a_missing_family(self):
        invalid = copy.deepcopy(self.bundle)
        invalid["assets"] = invalid["assets"][:-1]
        result = validate_final_asset_payload(invalid, self.store)
        self.assertFalse(result["valid"])
        self.assertIn("exact_family_coverage", {error["code"] for error in result["errors"]})

    def test_readiness_requires_matching_owner_decision(self):
        blocked = build_final_asset_promotion_readiness(self.bundle, self.store, [])
        ready = build_final_asset_promotion_readiness(
            self.bundle, self.store, [self.decision]
        )
        self.assertFalse(blocked["promotion_allowed"])
        self.assertTrue(ready["promotion_allowed"])
        self.assertFalse(ready["content_generation_allowed"])

    def test_promotion_preserves_seed_assets_and_records_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            candidate_path = temp_root / "candidate.json"
            store_path = temp_root / "store.json"
            manifest_path = temp_root / "promotion.json"
            validation_path = temp_root / "validation.json"
            candidate_path.write_text(json.dumps(self.bundle, ensure_ascii=False), encoding="utf-8")
            store_path.write_text(json.dumps(self.store, ensure_ascii=False), encoding="utf-8")

            result = promote_final_asset_bundle(
                str(candidate_path),
                decisions=[self.decision],
                store_path=store_path,
                manifest_path=manifest_path,
                validation_path=validation_path,
                require_inbox=False,
            )

            self.assertEqual(result["status"], "promoted_final_creation_assets")
            promoted_store = load_json(store_path)
            self.assertEqual(len(promoted_store["assets"]), len(self.store["assets"]) + 9)
            self.assertEqual(load_json(manifest_path)["content_generation_allowed"], False)
            self.assertTrue(validation_path.exists())


if __name__ == "__main__":
    unittest.main()
