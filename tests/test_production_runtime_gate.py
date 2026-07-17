import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "system/runtime"))

from nrl_production_runtime import (
    build_chapter_writer_prompt,
    build_production_preflight,
    has_bounded_intent_authorization,
    has_bounded_prose_authorization,
)


class ProductionRuntimeGateTests(unittest.TestCase):
    def test_asset_authorization_does_not_unlock_prose(self):
        self.assertFalse(
            has_bounded_prose_authorization(
                [
                    {
                        "decision_type": "authorize_final_asset_generation",
                        "authorized_scope": ["apply_project_reconciliation_v0.19"],
                    }
                ]
            )
        )

    def test_dedicated_prose_authorization_unlocks_runtime(self):
        self.assertTrue(
            has_bounded_prose_authorization(
                [
                    {
                        "decision_type": "authorize_controlled_prose_test",
                        "authorized_scope": ["bounded_chapter_runtime_v0.20"],
                    }
                ]
            )
        )

    def test_chapter_scope_does_not_unlock_another_chapter(self):
        decision = {
            "decision_type": "authorize_controlled_prose_test",
            "authorized_scope": ["bounded_chapter_runtime_v0.20:chapter-0002"],
        }
        self.assertTrue(has_bounded_prose_authorization([decision], "chapter-0002"))
        self.assertFalse(has_bounded_prose_authorization([decision], "chapter-0003"))

    def test_longform_cluster_one_scope_is_bounded_to_first_ten_chapters(self):
        decision = {
            "decision_type": "authorize_controlled_prose_test",
            "authorized_scope": ["longform_cluster1_v024:chapter-0003"],
        }
        self.assertTrue(has_bounded_prose_authorization([decision], "chapter-0003"))
        self.assertFalse(has_bounded_prose_authorization([decision], "chapter-0011"))

    def test_volume_one_longform_scope_allows_only_the_authorized_chapter(self):
        decision = {
            "decision_type": "authorize_controlled_prose_test",
            "authorized_scope": ["longform_volume1_v025:chapter-0011"],
        }
        self.assertTrue(has_bounded_prose_authorization([decision], "chapter-0011"))
        self.assertFalse(has_bounded_prose_authorization([decision], "chapter-0012"))
        self.assertFalse(has_bounded_prose_authorization([decision], "chapter-0101"))

    def test_intent_authorization_is_not_prose_authorization(self):
        decision = {
            "decision_type": "authorize_next_phase",
            "authorized_scope": ["bounded_chapter_intent_v0.20"],
        }
        self.assertTrue(has_bounded_intent_authorization([decision]))
        self.assertFalse(has_bounded_prose_authorization([decision]))

    def test_writer_prompt_is_blocked_by_production_preflight_before_prose_gate(self):
        with mock.patch(
            "nrl_production_runtime.build_production_preflight",
            return_value={"valid": False, "checks": {"production_blueprint_owner_accepted": False}},
        ):
            with self.assertRaisesRegex(RuntimeError, "production preflight is blocked"):
                build_chapter_writer_prompt("chapter-0003")

    def test_preflight_only_exempts_the_current_writer_chapter(self):
        import nrl_production_runtime as runtime
        registry = {"chapters": [{"chapter_id": "chapter-0003", "stage": "context_compiled"}, {"chapter_id": "chapter-0004", "stage": "chapter_intent"}]}
        with mock.patch.object(runtime, "_load_registry", return_value=registry), mock.patch.object(runtime, "build_production_readiness", return_value={"ready": True}), mock.patch.object(runtime, "build_volume1_dry_run", return_value={"valid": True}), mock.patch.object(runtime, "build_model_team_attestation_status", return_value={"valid": True}), mock.patch.object(runtime, "validate_creation_asset_store", return_value={"valid": True}), mock.patch.object(runtime, "find_codex_binary", return_value="codex"), mock.patch.object(runtime, "build_antigravity_bridge_status", return_value={"available": True}), mock.patch.object(runtime, "ACTIVE_BLUEPRINT_PATH") as active:
            active.exists.return_value = False
            result = build_production_preflight({"codex": {"can_execute": True}, "antigravity": {"execution_policy": "independent_review_and_provider_fallback_only"}}, allowed_pending_chapter_id="chapter-0003")
        self.assertFalse(result["checks"]["no_unaccepted_chapters"])


if __name__ == "__main__":
    unittest.main()
