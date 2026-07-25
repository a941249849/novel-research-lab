import json
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from nrl import load_adapters, load_state
from nrl_agent_ops import build_production_runtime_status
from nrl_architecture import build_architecture_reconciliation
from nrl_model_router import build_model_routing_status, validate_model_team_contract
from nrl_production_runtime import build_production_preflight
from nrl_production_calibration import build_model_team_attestation_status
from nrl_system_status import build_system_status


class CodexModelTeamV027Tests(unittest.TestCase):
    def setUp(self):
        self.state = load_state()
        self.adapters = load_adapters()

    def test_active_adapters_remove_hermes_and_keep_antigravity_as_backup(self):
        self.assertNotIn("hermes", self.adapters)
        self.assertEqual(
            self.adapters["antigravity"]["execution_policy"],
            "independent_review_and_provider_fallback_only",
        )

    def test_three_codex_models_have_distinct_production_responsibilities(self):
        contract = validate_model_team_contract()
        self.assertTrue(contract["valid"], contract["errors"])
        routes = {item["role"]: item for item in build_model_routing_status()["routes"]}
        self.assertEqual(routes["showrunner"]["model"], "gpt-5.6-sol")
        self.assertEqual(routes["reviewer"]["model"], "gpt-5.6-sol")
        self.assertEqual(routes["writer"]["model"], "gpt-5.6-terra")
        self.assertEqual(routes["editor"]["model"], "gpt-5.6-terra")
        self.assertEqual(routes["observer"]["model"], "gpt-5.6-luna")
        self.assertEqual(routes["mechanical"]["model"], "gpt-5.6-luna")

    def test_operational_attestation_resolves_the_legacy_sol_only_decision(self):
        status = build_model_team_attestation_status()
        self.assertTrue(status["valid"], status["errors"])
        self.assertGreaterEqual(status["writer_model_counts"]["gpt-5.6-sol"], 10)
        self.assertGreaterEqual(status["writer_model_counts"]["gpt-5.6-terra"], 20)

    def test_runtime_status_has_model_team_and_no_active_hermes_role(self):
        with mock.patch(
            "nrl_system_status.build_antigravity_execution_status",
            return_value={
                "effective_state": "blocked_bridge_unavailable",
                "bridge_available": False,
                "can_dispatch_registered_reviews": False,
            },
        ), mock.patch(
            "nrl_system_status.build_antigravity_bridge_status",
            return_value={"available": False},
        ):
            status = build_system_status(self.state, self.adapters)
        self.assertTrue(status["production_ready"])
        self.assertNotIn("hermes_role", status)
        self.assertNotIn("hermes_execution", status)
        self.assertNotIn("hermes", status["agent_roles"])
        self.assertEqual(
            {item["model"] for item in status["codex_model_team"]},
            {"gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"},
        )
        self.assertEqual(status["antigravity_role"], "backup_review_and_provider_fallback")

    def test_architecture_contract_contains_model_roles_not_hermes(self):
        architecture = build_architecture_reconciliation(self.state, self.adapters)
        roles = architecture["agent_role_contract"]
        self.assertNotIn("Hermes", {item["agent"] for item in roles})
        self.assertEqual(
            {item["agent"] for item in roles if item.get("agent_family") == "Codex"},
            {"Codex Sol", "Codex Terra", "Codex Luna"},
        )
        antigravity = next(item for item in roles if item["agent"] == "Antigravity")
        self.assertEqual(antigravity["status"], "backup")

    def test_production_runtime_does_not_require_hermes_or_live_antigravity(self):
        status = build_production_runtime_status(self.state, self.adapters)
        self.assertNotIn("hermes", status)
        self.assertIn("codex_model_team", status)
        self.assertEqual(status["antigravity"]["production_dependency"], False)

        with mock.patch("nrl_production_runtime._load_registry", return_value={"chapters": []}), \
             mock.patch("nrl_production_runtime.build_production_readiness", return_value={"ready": True}), \
             mock.patch("nrl_production_runtime.build_volume1_dry_run", return_value={"valid": True}), \
             mock.patch("nrl_production_runtime.build_direct_writer_calibration_status", return_value={"valid": True}), \
             mock.patch("nrl_production_runtime.build_model_team_attestation_status", return_value={"valid": True}), \
             mock.patch("nrl_production_runtime.validate_creation_asset_store", return_value={"valid": True}), \
             mock.patch("nrl_production_runtime.find_codex_binary", return_value="codex"), \
             mock.patch("nrl_production_runtime.build_antigravity_bridge_status", return_value={"available": False}), \
             mock.patch("nrl_production_runtime.load_decisions", return_value=[{"decision_type": "accept_review", "authorized_scope": ["borrowed-heaven-production-blueprint-v01"]}]), \
             mock.patch("nrl_production_runtime.ACTIVE_BLUEPRINT_PATH") as active:
            active.exists.return_value = False
            preflight = build_production_preflight(self.adapters)
        self.assertTrue(preflight["valid"], json.dumps(preflight, ensure_ascii=False))
        self.assertNotIn("legacy_agent_protocol_canaries_valid", preflight["checks"])
        self.assertTrue(preflight["checks"]["codex_model_team_contract_valid"])
        self.assertTrue(preflight["checks"]["codex_model_team_attestation_valid"])
        self.assertTrue(preflight["checks"]["antigravity_backup_configured"])


if __name__ == "__main__":
    unittest.main()
