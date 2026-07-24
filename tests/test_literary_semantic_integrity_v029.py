from __future__ import annotations

import copy
import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "system/runtime"))

from nrl_literary_semantics import (  # noqa: E402
    DIMENSIONS,
    validate_literary_semantic_assets,
    validate_project_semantic_contracts,
)
from nrl_production_runtime import (  # noqa: E402
    build_chapter_literary_semantic_contract,
    compile_chapter_context_payload,
    validate_compiled_literary_semantic_payload,
    validate_prose_entry_gate,
)
import nrl_production_runtime as production_runtime  # noqa: E402
import jsonschema  # noqa: E402


class LiterarySemanticIntegrityV029Tests(unittest.TestCase):
    def test_all_books_keep_a_protected_twelve_dimension_profile(self) -> None:
        result = validate_literary_semantic_assets()
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["profile_count"], 18)
        profiles = json.loads(
            (ROOT / "system/research_assets/deep_read/v0.29/signature_profiles.v1.json").read_text(
                encoding="utf-8"
            )
        )["profiles"]
        self.assertEqual(
            {item["book_title"] for item in profiles},
            {
                "一念永恒", "不死不灭", "人道至尊", "仙逆", "凡人修仙传", "圣墟",
                "大主宰", "完美世界", "将夜", "斗破苍穹", "武动乾坤", "永生",
                "求魔", "牧神记", "蛊真人", "诡秘之主", "遮天", "雪中悍刀行",
            },
        )
        for profile in profiles:
            self.assertEqual(set(profile["dimensions"]), set(DIMENSIONS))
            self.assertTrue(all(item["findings"] for item in profile["dimensions"].values()))
        for dimension in DIMENSIONS:
            findings = [
                json.dumps(
                    profile["dimensions"][dimension]["findings"],
                    ensure_ascii=False,
                    sort_keys=True,
                )
                for profile in profiles
            ]
            self.assertEqual(len(findings), len(set(findings)))

    def test_gu_zhen_ren_preserves_the_features_that_lossy_distillation_missed(self) -> None:
        profiles = json.loads(
            (ROOT / "system/research_assets/deep_read/v0.29/signature_profiles.v1.json").read_text(
                encoding="utf-8"
            )
        )["profiles"]
        profile = next(item for item in profiles if item["book_title"] == "蛊真人")
        self.assertIn("人祖传", " ".join(profile["dimensions"]["embedded_history_and_lore"]["findings"]))
        self.assertIn("白凝冰", " ".join(profile["dimensions"]["character_highlight_architecture"]["findings"]))
        self.assertIn("空窍", " ".join(profile["dimensions"]["progression_and_thresholds"]["findings"]))
        self.assertIn("五域", " ".join(profile["dimensions"]["world_map_and_scale"]["findings"]))

    def test_validation_rejects_a_missing_dimension_or_stale_synthesis_hash(self) -> None:
        profile_path = ROOT / "system/research_assets/deep_read/v0.29/signature_profiles.v1.json"
        payload = json.loads(profile_path.read_text(encoding="utf-8"))
        missing = copy.deepcopy(payload)
        missing["profiles"][0]["dimensions"].pop(DIMENSIONS[0])
        self.assertFalse(validate_literary_semantic_assets(profile_payload=missing)["valid"])
        stale = copy.deepcopy(payload)
        stale["profiles"][0]["synthesis_sha256"] = "0" * 64
        self.assertFalse(validate_literary_semantic_assets(profile_payload=stale)["valid"])
        degraded = copy.deepcopy(payload)
        degraded["profiles"][0]["dimensions"][DIMENSIONS[0]]["findings"] = [
            "generic placeholder"
        ]
        result = validate_literary_semantic_assets(profile_payload=degraded)
        self.assertFalse(result["valid"])
        self.assertTrue(any("content drift" in item for item in result["errors"]))

    def test_project_contracts_cover_highlights_progression_map_and_history(self) -> None:
        result = validate_project_semantic_contracts("hundred-crafts-night-procession")
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["volume_count"], 15)
        self.assertEqual(result["history_dossier_count"], 15)
        self.assertEqual(result["character_count"], 5)
        self.assertTrue(result["checks"]["every_character_has_three_signature_highlights"])
        self.assertTrue(result["checks"]["every_volume_preserves_all_character_agency"])
        self.assertTrue(result["checks"]["fixed_progression_permissions"])
        self.assertTrue(result["checks"]["history_changes_present_plot"])

    def test_project_application_covers_every_dimension_and_preserves_originality(self) -> None:
        application = json.loads(
            (
                ROOT
                / "projects/hundred-crafts-night-procession/validation/literary_semantic_application.v1.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(
            {item["dimension"] for item in application["dimension_decisions"]},
            set(DIMENSIONS),
        )
        gu = [item for item in application["signature_decisions"] if item["source_book"] == "蛊真人"]
        self.assertGreaterEqual(len(gu), 3)
        self.assertTrue(all(item["decision"] in {"transform", "reject", "defer"} for item in gu))
        self.assertTrue(all(item["originality_transformation"] for item in gu))
        profiles = json.loads(
            (
                ROOT
                / "system/research_assets/deep_read/v0.29/signature_profiles.v1.json"
            ).read_text(encoding="utf-8")
        )["profiles"]
        self.assertEqual(
            {
                item["source_book"]
                for item in application["signature_dimension_dispositions"]
            },
            {item["book_title"] for item in profiles},
        )
        self.assertNotIn(
            "defer",
            {item["decision"] for item in application["signature_decisions"]},
        )

    def test_volume1_has_a_chapter_level_semantic_contract(self) -> None:
        result = validate_project_semantic_contracts("hundred-crafts-night-procession")
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["volume1_semantic_beat_count"], 66)
        self.assertTrue(result["checks"]["volume1_semantic_beats_complete"])
        self.assertTrue(result["checks"]["all_source_books_decided"])
        self.assertTrue(result["checks"]["all_signature_cells_dispositioned"])
        application = json.loads(
            (
                ROOT
                / "projects/hundred-crafts-night-procession/validation/literary_semantic_application.v1.json"
            ).read_text(encoding="utf-8")
        )
        dispositions = application["signature_dimension_dispositions"]
        self.assertEqual(len(dispositions), 18 * len(DIMENSIONS))
        self.assertEqual(
            len(
                {
                    (
                        item["source_profile_id"],
                        item["source_book"],
                        item["source_dimension"],
                    )
                    for item in dispositions
                }
            ),
            18 * len(DIMENSIONS),
        )

    def test_chapter_context_receives_hash_bound_semantic_rules(self) -> None:
        previous = os.environ.get("NRL_PROJECT_ID")
        os.environ["NRL_PROJECT_ID"] = "hundred-crafts-night-procession"
        try:
            baseline = json.loads(
                (
                    ROOT
                    / "projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json"
                ).read_text(encoding="utf-8")
            )
            semantic = build_chapter_literary_semantic_contract(
                "chapter-0003", baseline
            )
            self.assertEqual(semantic["chapter_beat"]["chapter_id"], "chapter-0003")
            self.assertEqual(
                semantic["application_summary"]["source_books_decided"], 18
            )
            compiled = compile_chapter_context_payload(
                {
                    "chapter_id": "chapter-0003",
                    "required_asset_ids": [],
                    "must_keep": [],
                    "must_avoid": [],
                    "scene_constraints": [],
                },
                [],
                {},
                [],
                literary_semantic_contract=semantic,
            )
            self.assertTrue(compiled["valid"], compiled["errors"])
            self.assertEqual(
                compiled["context"]["literary_semantic_contract"]["chapter_id"],
                "chapter-0003",
            )
            self.assertIn(
                "literary_semantic_contract",
                compiled["rule_stack"]["priority_order"],
            )
            self.assertTrue(
                any(
                    "professional agency" in item
                    for item in compiled["rule_stack"]["hard_rules"]
                )
            )
            self.assertEqual(len(semantic["dimension_contracts"]), len(DIMENSIONS))
            self.assertEqual(len(semantic["protected_function_transforms"]), 20)
            self.assertNotIn(
                "defer",
                {
                    item["decision"]
                    for item in semantic["protected_function_transforms"]
                },
            )
            mutated_context = copy.deepcopy(compiled["context"])
            mutated_context.pop("literary_semantic_contract")
            validation = validate_compiled_literary_semantic_payload(
                mutated_context,
                compiled["rule_stack"],
                compiled["trace"],
                semantic,
                "chapter-0003",
                {},
            )
            self.assertFalse(validation["valid"])
            mutated_rules = copy.deepcopy(compiled["rule_stack"])
            mutated_rules["hard_rules"] = []
            validation = validate_compiled_literary_semantic_payload(
                compiled["context"],
                mutated_rules,
                compiled["trace"],
                semantic,
                "chapter-0003",
                {},
            )
            self.assertFalse(validation["valid"])
        finally:
            if previous is None:
                os.environ.pop("NRL_PROJECT_ID", None)
            else:
                os.environ["NRL_PROJECT_ID"] = previous

    def test_project_context_compiler_fails_closed_without_semantics(self) -> None:
        previous = os.environ.get("NRL_PROJECT_ID")
        os.environ["NRL_PROJECT_ID"] = "hundred-crafts-night-procession"
        try:
            result = compile_chapter_context_payload(
                {
                    "chapter_id": "chapter-0001",
                    "required_asset_ids": [],
                    "must_keep": [],
                    "must_avoid": [],
                    "scene_constraints": [],
                },
                [],
                {},
                [],
            )
            self.assertFalse(result["valid"])
            self.assertIn("requires a literary semantic contract", result["errors"][0])
        finally:
            if previous is None:
                os.environ.pop("NRL_PROJECT_ID", None)
            else:
                os.environ["NRL_PROJECT_ID"] = previous

    def test_project_validation_rejects_an_undispositioned_signature_cell(self) -> None:
        application = json.loads(
            (
                ROOT
                / "projects/hundred-crafts-night-procession/validation/literary_semantic_application.v1.json"
            ).read_text(encoding="utf-8")
        )
        incomplete = copy.deepcopy(application)
        incomplete["signature_dimension_dispositions"].pop()
        result = validate_project_semantic_contracts(
            "hundred-crafts-night-procession",
            application_payload=incomplete,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("216 protected signature cells" in item for item in result["errors"])
        )

    def test_project_validation_rejects_implicit_activation_of_a_deferred_cell(
        self,
    ) -> None:
        application = json.loads(
            (
                ROOT
                / "projects/hundred-crafts-night-procession/validation/literary_semantic_application.v1.json"
            ).read_text(encoding="utf-8")
        )
        mutated = copy.deepcopy(application)
        deferred = next(
            item
            for item in mutated["signature_dimension_dispositions"]
            if item["decision"] == "defer"
            and not any(
                selected["source_book"] == item["source_book"]
                and selected["source_dimension"] == item["source_dimension"]
                for selected in mutated["signature_decisions"]
            )
        )
        deferred["decision"] = "transform"
        result = validate_project_semantic_contracts(
            "hundred-crafts-night-procession",
            application_payload=mutated,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "lacks an explicit selected decision" in item
                for item in result["errors"]
            )
        )

    def test_project_validation_rejects_duplicate_and_surplus_active_rules(
        self,
    ) -> None:
        application = json.loads(
            (
                ROOT
                / "projects/hundred-crafts-night-procession/validation/literary_semantic_application.v1.json"
            ).read_text(encoding="utf-8")
        )
        duplicate_selected = copy.deepcopy(application)
        duplicate_selected["signature_decisions"].append(
            copy.deepcopy(duplicate_selected["signature_decisions"][0])
        )
        result = validate_project_semantic_contracts(
            "hundred-crafts-night-procession",
            application_payload=duplicate_selected,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("duplicate selected" in item for item in result["errors"])
        )

        surplus_selected = copy.deepcopy(application)
        surplus = copy.deepcopy(surplus_selected["signature_decisions"][0])
        surplus["source_dimension"] = "undeclared_dimension"
        surplus_selected["signature_decisions"].append(surplus)
        result = validate_project_semantic_contracts(
            "hundred-crafts-night-procession",
            application_payload=surplus_selected,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(
            any(
                "signature decision is incomplete" in item
                or "exactly equal active dispositions" in item
                for item in result["errors"]
            )
        )

        duplicate_dimension = copy.deepcopy(application)
        duplicate_dimension["dimension_decisions"].append(
            copy.deepcopy(duplicate_dimension["dimension_decisions"][0])
        )
        result = validate_project_semantic_contracts(
            "hundred-crafts-night-procession",
            application_payload=duplicate_dimension,
        )
        self.assertFalse(result["valid"])
        self.assertTrue(
            any("duplicate project semantic" in item for item in result["errors"])
        )

    def test_every_revision_route_rechecks_live_prose_authorization(self) -> None:
        with mock.patch(
            "nrl_production_runtime.build_production_preflight",
            return_value={"valid": True},
        ), mock.patch(
            "nrl_production_runtime.build_production_readiness",
            return_value={"ready": False},
        ), mock.patch(
            "nrl_production_runtime.has_bounded_prose_authorization",
            return_value=True,
        ), mock.patch(
            "nrl_production_runtime.load_decisions",
            return_value=[],
        ):
            result = validate_prose_entry_gate("chapter-0001")
        self.assertFalse(result["valid"])
        self.assertIn("production_readiness", result["errors"])
        record = {
            "chapter_id": "chapter-0001",
            "stage": "continuity_audited",
            "artifacts": {},
            "source_hashes": {},
        }
        with mock.patch.object(
            production_runtime, "_load_registry", return_value={"chapters": [record]}
        ), mock.patch.object(
            production_runtime, "_chapter_record", return_value=record
        ), mock.patch.object(
            production_runtime,
            "validate_prose_entry_gate",
            return_value={"valid": False, "errors": ["production_readiness"]},
        ), mock.patch.object(production_runtime, "_ask_prose_writer") as writer:
            with self.assertRaisesRegex(RuntimeError, "revision prose gate is blocked"):
                production_runtime.dispatch_chapter_revision("chapter-0001")
            writer.assert_not_called()
        with mock.patch.object(
            production_runtime, "_load_registry", return_value={"chapters": [record]}
        ), mock.patch.object(
            production_runtime, "_chapter_record", return_value=record
        ), mock.patch.object(
            production_runtime,
            "validate_stage_transition",
            return_value={"valid": True, "errors": []},
        ), mock.patch.object(
            production_runtime,
            "validate_prose_entry_gate",
            return_value={"valid": False, "errors": ["production_readiness"]},
        ):
            with self.assertRaisesRegex(
                RuntimeError, "revision ingest prose gate is blocked"
            ):
                production_runtime.ingest_chapter_revision(
                    "chapter-0001", "unused.md"
                )

    def test_acceptance_rechecks_live_prose_authorization(self) -> None:
        record = {
            "chapter_id": "chapter-0001",
            "stage": "state_settled",
            "artifacts": {},
            "source_hashes": {},
        }
        with mock.patch.object(
            production_runtime, "_load_registry", return_value={"chapters": [record]}
        ), mock.patch.object(
            production_runtime, "_chapter_record", return_value=record
        ), mock.patch.object(
            production_runtime,
            "validate_prose_entry_gate",
            return_value={"valid": False, "errors": ["bounded_prose_authorization"]},
        ):
            with self.assertRaisesRegex(
                RuntimeError, "acceptance prose gate is blocked"
            ):
                production_runtime.accept_chapter("chapter-0001")

    def test_every_project_chapter_requires_external_initial_literary_audit(
        self,
    ) -> None:
        previous = os.environ.get("NRL_PROJECT_ID")
        os.environ["NRL_PROJECT_ID"] = "hundred-crafts-night-procession"
        try:
            self.assertTrue(
                production_runtime.requires_external_chapter_audit(
                    "chapter-0001", "initial"
                )
            )
            self.assertTrue(
                production_runtime.requires_external_chapter_audit(
                    "chapter-0004", "initial"
                )
            )
            self.assertTrue(
                production_runtime.requires_external_chapter_audit(
                    "chapter-0004", "final"
                )
            )
        finally:
            if previous is None:
                os.environ.pop("NRL_PROJECT_ID", None)
            else:
                os.environ["NRL_PROJECT_ID"] = previous

    def test_project_authorization_supports_each_declared_volume_window(
        self,
    ) -> None:
        sol_relative = (
            "projects/hundred-crafts-night-procession/validation/"
            "literary-semantic-sol-review.v0.29.md"
        )
        antigravity_relative = (
            ".agent-handoff/antigravity/responses/"
            "hundred-crafts-literary-semantic-v029.md"
        )
        sol_sha = hashlib.sha256((ROOT / sol_relative).read_bytes()).hexdigest()
        antigravity_sha = hashlib.sha256(
            (ROOT / antigravity_relative).read_bytes()
        ).hexdigest()
        with tempfile.TemporaryDirectory() as temporary:
            workspace = Path(temporary)
            baseline = workspace / "creation_assets/canonical_baseline.json"
            baseline.parent.mkdir(parents=True)
            baseline.write_text('{"version":"test"}\n', encoding="utf-8")
            baseline_sha = hashlib.sha256(baseline.read_bytes()).hexdigest()
            review_index = (
                workspace
                / "production_runtime/production_readiness/final-review-index.v0.1.json"
            )
            review_index.parent.mkdir(parents=True)
            review_index.write_text(
                json.dumps(
                    {
                        "valid": True,
                        "bound_baseline_sha256": baseline_sha,
                        "sol_verdict": "ACCEPT",
                        "antigravity_verdict": "ACCEPT",
                        "sol_review_path": sol_relative,
                        "antigravity_review_path": antigravity_relative,
                        "sol_review_sha256": sol_sha,
                        "antigravity_review_sha256": antigravity_sha,
                    }
                ),
                encoding="utf-8",
            )
            decision = {
                "decision_type": "authorize_controlled_prose_test",
                "project_id": "hundred-crafts-night-procession",
                "authorized_scope": [
                    "project_volume1_v1:hundred-crafts-night-procession:chapter-0011"
                ],
                "forbidden_scope": [
                    "hundred-crafts-night-procession:outside-window-011-020",
                    "hundred-crafts-night-procession:bulk-or-continuous-production",
                    "hundred-crafts-night-procession:raw-corpus-read",
                    "hundred-crafts-night-procession:publish",
                ],
                "expires_after_mission": (
                    "hundred-crafts-night-procession-volume1-window-011-020-v1"
                ),
                "bound_baseline_sha256": baseline_sha,
                "bound_sol_review_sha256": sol_sha,
                "bound_antigravity_review_sha256": antigravity_sha,
            }
            intent_decision = {
                **decision,
                "decision_type": "authorize_next_phase",
            }
            with mock.patch.object(
                production_runtime,
                "active_project_id",
                return_value="hundred-crafts-night-procession",
            ), mock.patch.object(
                production_runtime,
                "active_project",
                return_value={"content_authorized": True},
            ), mock.patch.object(
                production_runtime,
                "project_workspace",
                return_value=workspace,
            ), mock.patch.object(
                production_runtime,
                "validate_project_production",
                return_value={"valid": True, "errors": [], "canonical_inputs": []},
            ), mock.patch.object(
                production_runtime,
                "load_decisions",
                return_value=[intent_decision, decision],
            ), mock.patch.object(
                production_runtime,
                "volume1_windows",
                return_value=((1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 60), (61, 66)),
            ):
                self.assertTrue(
                    production_runtime.has_bounded_prose_authorization(
                        [decision], "chapter-0011"
                    )
                )
                self.assertFalse(
                    production_runtime.has_bounded_prose_authorization(
                        [decision], "chapter-0021"
                    )
                )
                readiness = production_runtime.build_production_readiness(
                    "chapter-0011"
                )
                self.assertTrue(readiness["ready"], readiness)
                self.assertEqual(readiness["target_chapter_id"], "chapter-0011")
                self.assertEqual(readiness["target_window"], [11, 20])
                self.assertEqual(
                    readiness["status"], "ready_for_formal_window_011_020"
                )
                blocked = production_runtime.build_production_readiness(
                    "chapter-0021"
                )
                self.assertFalse(blocked["ready"])
                self.assertFalse(blocked["checks"]["bounded_intent_authorized"])
                self.assertFalse(blocked["checks"]["bounded_prose_authorized"])

    def test_audit_ingest_rejects_empty_semantic_evidence_for_initial_and_final(
        self,
    ) -> None:
        base_dimensions = {
            key: ["checked"]
            for key in production_runtime.AUDIT_EVIDENCE_DIMENSIONS
        }
        for audit_kind, artifact_kind in (
            ("initial", "draft"),
            ("final", "revision"),
        ):
            for invalid_value in (
                [],
                ["   "],
                ["\u200b"],
                ["\u2060"],
                ["\ufeff"],
                ["---"],
            ):
                payload = {
                    "chapter_id": "chapter-0001",
                    "artifact_kind": artifact_kind,
                    "artifact_sha256": "a" * 64,
                    "context_sha256": "b" * 64,
                    "verdict": "ACCEPT",
                    "dimensions": copy.deepcopy(base_dimensions),
                    "issues": [],
                    "resolved_prior_issue_ids": [],
                }
                payload["dimensions"]["semantic_realization"] = invalid_value
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    suffix=".json",
                    encoding="utf-8",
                    delete=False,
                ) as handle:
                    json.dump(payload, handle, ensure_ascii=False)
                    source = handle.name
                try:
                    with mock.patch.object(
                        production_runtime,
                        "build_chapter_audit_packet",
                        return_value={
                            "audit_kind": audit_kind,
                            "template": {
                                "artifact_kind": artifact_kind,
                                "artifact_sha256": "a" * 64,
                                "context_sha256": "b" * 64,
                                "resolved_prior_issue_ids": [],
                            },
                        },
                    ):
                        with self.assertRaises(
                            (jsonschema.ValidationError, RuntimeError)
                        ):
                            production_runtime.ingest_chapter_audit(
                                "chapter-0001", source
                            )
                finally:
                    Path(source).unlink(missing_ok=True)

    def test_deterministic_audit_cannot_bypass_project_model_review(self) -> None:
        with mock.patch.object(
            production_runtime,
            "active_project_id",
            return_value="hundred-crafts-night-procession",
        ), mock.patch.object(production_runtime, "_load_registry") as load_registry:
            with self.assertRaisesRegex(RuntimeError, "legacy-only"):
                production_runtime.record_deterministic_chapter_audit(
                    "chapter-0001"
                )
            load_registry.assert_not_called()

    def test_stale_semantic_source_is_rejected_by_chapter_compiler(self) -> None:
        previous = os.environ.get("NRL_PROJECT_ID")
        os.environ["NRL_PROJECT_ID"] = "hundred-crafts-night-procession"
        try:
            baseline = json.loads(
                (
                    ROOT
                    / "projects/hundred-crafts-night-procession/creation_assets/canonical_baseline.json"
                ).read_text(encoding="utf-8")
            )
            stale = copy.deepcopy(baseline)
            target = next(
                item
                for item in stale["canonical_inputs"]
                if item["path"].endswith("volume1_semantic_beat_contract.v1.json")
            )
            target["sha256"] = "0" * 64
            with self.assertRaisesRegex(RuntimeError, "not current"):
                build_chapter_literary_semantic_contract("chapter-0003", stale)
        finally:
            if previous is None:
                os.environ.pop("NRL_PROJECT_ID", None)
            else:
                os.environ["NRL_PROJECT_ID"] = previous


if __name__ == "__main__":
    unittest.main()
