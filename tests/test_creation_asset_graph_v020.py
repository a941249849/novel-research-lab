import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
NRL = RUNTIME_DIR / "nrl.py"
STORE_PATH = REPO_ROOT / "system/creation_assets/project_assets.v0.2.json"
sys.path.insert(0, str(RUNTIME_DIR))

from nrl_creation_assets import build_creation_asset_graph_status


class CreationAssetGraphV020Tests(unittest.TestCase):
    def load_store(self):
        return json.loads(STORE_PATH.read_text(encoding="utf-8"))

    def test_cli_reports_all_nine_families_and_rereviewed_asset_baseline(self):
        result = subprocess.run(
            [sys.executable, str(NRL), "asset-graph-status"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.20")
        self.assertEqual(data["family_count"], 9)
        self.assertTrue(data["exact_family_coverage"])
        self.assertEqual(
            {item["family"] for item in data["families"]},
            {
                "characters",
                "npcs",
                "factions",
                "artifacts",
                "techniques",
                "naming",
                "emotional_bonds",
                "foreshadowing",
                "state_ledger",
            },
        )
        self.assertTrue(
            all({"total", "active", "seed"}.issubset(item) for item in data["families"])
        )
        self.assertTrue(all(item["total"] > 0 for item in data["families"]))
        self.assertEqual(data["advisory_review"]["verdict"], "ACCEPT_WITH_WARNINGS")
        self.assertFalse(data["advisory_review"]["named_unresolved_risks"])
        self.assertTrue(data["readiness"]["production_ready"])
        self.assertFalse(data["readiness"]["prose_generation_allowed"])

    def test_unresolved_reference_makes_graph_invalid(self):
        store = copy.deepcopy(self.load_store())
        store["assets"][0]["relationships"].append(
            {"target_id": "missing_asset", "relation_type": "depends_on"}
        )
        status = build_creation_asset_graph_status(store, advisory_review_text="")
        self.assertFalse(status["graph_valid"])
        self.assertFalse(status["schema_validation"]["valid"])
        self.assertEqual(
            status["summary"]["cross_asset_references"]["unresolved_count"], 1
        )
        self.assertIn(
            "unresolved_cross_asset_references", status["readiness"]["blockers"]
        )

    def test_final_asset_authorization_does_not_allow_prose(self):
        status = build_creation_asset_graph_status(
            self.load_store(),
            decisions=[
                {
                    "decision_id": "asset-only",
                    "decision_type": "authorize_final_asset_generation",
                    "authorized_scope": ["final_creation_asset_registry_v0.20"],
                }
            ],
            advisory_review_text="""
## 1. VERDICT
`ACCEPT`

## 3. CROSS_ASSET_INTEGRITY
No named unresolved risks.

## 5. REQUIRED_REMEDIATIONS
None.

## 6. PROSE_GATE_RECOMMENDATION
A separate controlled-prose decision is required.
""",
        )
        self.assertTrue(status["authorization"]["asset_authorization_present"])
        self.assertFalse(
            status["authorization"]["controlled_prose_authorization_present"]
        )
        self.assertFalse(status["authorization"]["prose_generation_allowed"])
        self.assertFalse(status["readiness"]["prose_generation_allowed"])

    def test_named_advisory_risk_blocks_an_accept_verdict(self):
        status = build_creation_asset_graph_status(
            self.load_store(),
            decisions=[],
            advisory_review_text="""
## 1. VERDICT
`ACCEPT`

## 3. CROSS_ASSET_INTEGRITY
- **State Ownership Overlap**: Shared keys still lack a single writer.

## 5. REQUIRED_REMEDIATIONS
1. Establish a single-writer rule.

## 6. PROSE_GATE_RECOMMENDATION
Keep prose blocked.
""",
        )
        self.assertTrue(status["graph_valid"])
        self.assertFalse(status["readiness"]["production_ready"])
        self.assertIn(
            "named_advisory_risks_unresolved", status["readiness"]["blockers"]
        )


if __name__ == "__main__":
    unittest.main()
