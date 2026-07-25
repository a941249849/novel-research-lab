import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))

from nrl_volume1_plan import (
    LEDGER_IDS,
    build_initial_state_contract,
    build_volume1_manifest,
    validate_initial_state_contract,
    validate_volume1_manifest,
)


class Volume1ProductionPlanTests(unittest.TestCase):
    def test_manifest_is_exactly_six_ten_chapter_clusters(self):
        manifest = build_volume1_manifest()
        result = validate_volume1_manifest(manifest)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(manifest["chapters"][0]["chapter_id"], "chapter-0001")
        self.assertEqual(manifest["chapters"][-1]["chapter_id"], "chapter-0060")
        self.assertEqual([item["cluster"] for item in manifest["chapters"]].count(1), 10)

    def test_manifest_rejects_out_of_order_chapters(self):
        manifest = build_volume1_manifest()
        manifest["chapters"][1]["chapter_id"] = "chapter-0099"
        self.assertFalse(validate_volume1_manifest(manifest)["valid"])

    def test_state_contract_covers_all_ledgers_and_requires_peers(self):
        contract = build_initial_state_contract()
        self.assertTrue(validate_initial_state_contract(contract)["valid"])
        self.assertEqual(set(contract["states"]), set(LEDGER_IDS))
        contract["states"][LEDGER_IDS[0]]["peers"] = []
        self.assertFalse(validate_initial_state_contract(contract)["valid"])


if __name__ == "__main__":
    unittest.main()
