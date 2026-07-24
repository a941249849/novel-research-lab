import sys
import unittest
from pathlib import Path
from unittest import mock


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "system/runtime"))
REPO_ROOT = Path(__file__).resolve().parents[1]

from nrl_production_runtime import (
    STAGES,
    analyze_prose_metrics,
    build_rolling_state_snapshot,
    build_observer_prompt_payload,
    compile_chapter_context_payload,
    requires_external_chapter_audit,
    validate_acceptance,
    validate_chapter_sequence,
    validate_settlement_payload,
    validate_stage_transition,
)
import nrl_production_runtime as runtime


class ProductionChapterRuntimeV020Tests(unittest.TestCase):
    def test_writer_prompt_guards_repetitive_props_and_injury_continuity(self):
        source = (REPO_ROOT / "system/runtime/nrl_production_runtime.py").read_text(encoding="utf-8")
        self.assertIn("同一章‘残印’和‘封布’各不超过三次", source)
        self.assertIn("失能肢体和既有伤势不得在无明确治疗事件时恢复", source)

    def test_flat_observer_facts_are_grouped_before_schema_validation(self):
        payload = runtime.normalize_observation_payload(
            {
                "chapter_id": "chapter-0028",
                "draft_sha256": "a" * 64,
                "facts": [
                    {"asset_id": "character_lu_chenyuan", "field_path": "character.choice"},
                    {"asset_id": "state_ledger_revealed_account_errors", "field_path": "state_ledger.result"},
                    {"asset_id": "foreshadowing_cinder_seal_rain", "field_path": "foreshadowing.hook"},
                ],
            }
        )
        self.assertEqual(len(payload["facts"]["characters"]), 1)
        self.assertEqual(len(payload["facts"]["information"]), 1)
        self.assertEqual(len(payload["facts"]["hooks"]), 1)
        self.assertEqual(set(payload["facts"]), set(runtime.OBSERVATION_FACT_CATEGORIES))

    def test_observer_changes_alias_is_normalized_without_extra_property(self):
        payload = runtime.normalize_observation_payload(
            {"chapter_id": "chapter-0029", "draft_sha256": "b" * 64, "changes": []}
        )
        self.assertNotIn("changes", payload)
        self.assertEqual(set(payload["facts"]), set(runtime.OBSERVATION_FACT_CATEGORIES))

    def test_observer_fact_deltas_gain_known_hash_binding(self):
        payload = runtime.normalize_observation_payload(
            {"fact_deltas": []}, chapter_id="chapter-0068", draft_sha256="a" * 64
        )
        self.assertEqual(payload["chapter_id"], "chapter-0068")
        self.assertEqual(payload["draft_sha256"], "a" * 64)
        self.assertNotIn("fact_deltas", payload)
        self.assertEqual(set(payload["facts"]), set(runtime.OBSERVATION_FACT_CATEGORIES))

    def test_observer_known_bindings_override_provider_typos(self):
        payload = runtime.normalize_observation_payload(
            {
                "chapter_id": "chapter-9999",
                "draft_sha256": "b" * 64,
                "facts": {key: [] for key in runtime.OBSERVATION_FACT_CATEGORIES},
            },
            chapter_id="chapter-0074",
            draft_sha256="a" * 64,
        )
        self.assertEqual(payload["chapter_id"], "chapter-0074")
        self.assertEqual(payload["draft_sha256"], "a" * 64)

    def test_observer_normalizer_drops_non_schema_top_level_fields(self):
        payload = runtime.normalize_observation_payload({
            "chapter_id": "chapter-0070", "draft_sha256": "a" * 64,
            "accepted_revision_sha256": "b" * 64,
            "facts": {key: [] for key in runtime.OBSERVATION_FACT_CATEGORIES},
        })
        self.assertEqual(set(payload), {"chapter_id", "draft_sha256", "facts"})

    def test_provider_added_heading_is_stripped_without_touching_prose(self):
        text = "第二十五章 纸背留痕\n\n门外有人说这是第二十五章旧契。"
        self.assertEqual(runtime._strip_leading_chapter_heading(text), "门外有人说这是第二十五章旧契。")
        self.assertFalse(runtime._contains_chapter_heading("门外有人说这是第二十五章旧契。"))

    def test_short_draft_recovery_requests_enough_text_to_cross_minimum(self):
        draft = "\n\n".join(("前" * 1000, "中" * 1000, "后" * 600))
        with mock.patch.object(runtime, "ask_codex_writer", return_value="补" * 500):
            recovered, evidence = runtime._recover_short_draft("chapter-0025", "rules", draft)
        self.assertTrue(evidence["valid"])
        self.assertGreaterEqual(analyze_prose_metrics(recovered)["chinese_character_count"], 3000)

    def test_length_recovery_inserts_before_closing_beat(self):
        draft = "开头\n\n中段\n\n收束一\n\n收束二"
        result = runtime._insert_length_recovery(draft, "补足场景")
        self.assertEqual(result, "开头\n\n中段\n\n补足场景\n\n收束一\n\n收束二")

    def test_recovery_reflow_changes_only_paragraph_boundaries(self):
        source = ("动作落定。" * 120) + "钩子留下。"
        result = runtime._reflow_oversized_paragraphs(source, max_chars=120)
        self.assertEqual(result.replace("\n", ""), source)
        self.assertGreater(len(result.split("\n\n")), 1)

    def test_short_recovery_candidate_beats_later_oversized_draft(self):
        def metrics(text):
            return {
                "chinese_character_count": 2292 if text == "short" else 5025,
                "flags": [],
            }
        with mock.patch.object(runtime, "analyze_prose_metrics", side_effect=metrics):
            selected = runtime._best_short_recovery_candidate("", "short")
            selected = runtime._best_short_recovery_candidate(selected, "oversized")
        self.assertEqual(selected, "short")


    def test_sol_reviewer_accepts_schema_bound_audit(self):
        record = {"stage": "draft_generated", "artifacts": {"context": "context.json", "rule_stack": "rules.json", "trace": "trace.json", "draft": "draft.md"}}
        audit = {"chapter_id": "chapter-0001", "artifact_kind": "draft", "artifact_sha256": "a" * 64, "context_sha256": "b" * 64, "verdict": "ACCEPT", "dimensions": {key: ["checked"] for key in ("canon", "character", "state", "causality", "pacing", "life_force", "anti_ai_taste", "originality", "semantic_realization", "progression_permissions", "history_coherence")}, "issues": []}
        packet = REPO_ROOT / "system/production_runtime/chapters/chapter-0001/test-audit-packet.md"
        packet.write_text("packet", encoding="utf-8")
        with mock.patch.object(runtime, "build_chapter_audit_packet", return_value={"template": audit, "packet_path": str(packet.relative_to(REPO_ROOT))}), mock.patch.object(runtime, "ask_codex_structured", return_value=audit), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "validate_stage_transition", return_value={"valid": True, "errors": []}), mock.patch.object(runtime, "_save_registry"), mock.patch.object(runtime, "_write_json"):
            result = runtime.dispatch_chapter_audit("chapter-0001")
        packet.unlink()
        self.assertTrue(result["valid"])
        self.assertEqual(result["review_provider"], "codex")
        self.assertEqual(result["review_model"], "gpt-5.6-terra")
        self.assertIn("continuity_audit_execution", record["artifacts"])

    def test_failed_external_audit_persists_a_recoverable_attempt_record(self):
        import nrl_production_runtime as runtime

        record = {"stage": "draft_generated", "artifacts": {}}
        packet = REPO_ROOT / "system/production_runtime/chapters/chapter-0001/test-failed-audit-packet.md"
        packet.write_text("packet", encoding="utf-8")
        with mock.patch.object(runtime, "build_chapter_audit_packet", return_value={"template": {}, "packet_path": str(packet.relative_to(REPO_ROOT))}), mock.patch.object(runtime, "ask_codex_structured", side_effect=RuntimeError("codex unavailable")), mock.patch.object(runtime, "ask_antigravity_writer", side_effect=RuntimeError("provider unavailable")), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "_save_registry"), mock.patch.object(runtime, "_write_json") as write_json:
            result = runtime.dispatch_chapter_audit("chapter-0001")
        packet.unlink()
        self.assertFalse(result["valid"])
        self.assertIn("attempt_path", result)
        self.assertEqual(write_json.call_args.args[1]["status"], "provider_failed")
        self.assertIn("continuity_audit_attempt", record["artifacts"])

    def test_sol_audit_failure_falls_back_to_antigravity(self):
        import json

        record = {"stage": "draft_generated", "artifacts": {}}
        audit = {
            "chapter_id": "chapter-0005", "artifact_kind": "draft",
            "artifact_sha256": "a" * 64, "context_sha256": "b" * 64,
            "verdict": "ACCEPT", "dimensions": {key: ["checked"] for key in (
                "canon", "character", "state", "causality", "pacing",
                "life_force", "anti_ai_taste", "originality",
                "semantic_realization", "progression_permissions",
                "history_coherence",
            )}, "issues": [],
        }
        packet = REPO_ROOT / "system/production_runtime/chapters/chapter-0001/test-fallback-audit-packet.md"
        packet.write_text("packet", encoding="utf-8")
        with mock.patch.object(runtime, "build_chapter_audit_packet", return_value={"template": audit, "packet_path": str(packet.relative_to(REPO_ROOT))}), mock.patch.object(runtime, "ask_codex_structured", side_effect=RuntimeError("usage limit")), mock.patch.object(runtime, "ask_antigravity_writer", return_value=json.dumps(audit)), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "validate_stage_transition", return_value={"valid": True, "errors": []}), mock.patch.object(runtime, "_save_registry"), mock.patch.object(runtime, "_write_json"):
            result = runtime.dispatch_chapter_audit("chapter-0005")
        packet.unlink()
        self.assertTrue(result["valid"])
        self.assertEqual(result["review_provider"], "antigravity")
        self.assertEqual(result["review_model"], "Gemini 3.5 Flash (High)")

    def test_audit_normalizer_maps_compatible_agent_issue_labels(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{
            "issue_id": "W-1", "severity": "WARN", "description": "evidence", "recommendation": "fix",
            "dimension": "anti_ai_taste",
        }]})
        self.assertEqual(result["issues"], [{
            "issue_id": "W-1", "severity": "minor", "evidence": "evidence", "required_fix": "fix",
        }])
        self.assertEqual(
            runtime.normalize_continuity_audit_payload({"issues": [{"severity": "MINOR"}]})["issues"][0]["severity"],
            "minor",
        )
        rejected = runtime.normalize_continuity_audit_payload({
            "verdict": "REJECT", "issues": [{"severity": "FATAL"}]
        })
        self.assertEqual(rejected["verdict"], "REWORK_REQUIRED")
        self.assertEqual(rejected["issues"][0]["severity"], "blocking")
        unknown = runtime.normalize_continuity_audit_payload({
            "issues": [{"severity": "SEVERE"}]
        })
        self.assertEqual(unknown["issues"][0]["severity"], "blocking")

    def test_audit_normalizer_supplies_only_a_deterministic_missing_issue_id(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{
            "severity": "minor", "evidence": "evidence", "required_fix": "fix",
        }]})
        self.assertEqual(result["issues"][0]["issue_id"], "agent-issue-001")

    def test_audit_normalizer_supplies_neutral_missing_optional_text(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({"issues": [{"severity": "minor"}]})
        self.assertIn("No evidence", result["issues"][0]["evidence"])
        self.assertIn("No corrective action", result["issues"][0]["required_fix"])

    def test_audit_normalizer_converts_text_only_issue_to_major_finding(self):
        import nrl_production_runtime as runtime

        result = runtime.normalize_continuity_audit_payload({
            "issues": ["The final paragraphs repeat the same scene loop and must be consolidated."]
        })
        self.assertEqual(result["issues"], [{
            "issue_id": "agent-issue-001",
            "severity": "major",
            "evidence": "The final paragraphs repeat the same scene loop and must be consolidated.",
            "required_fix": "Correct the reviewer-described issue while preserving established state.",
        }])

    def test_stage_transition_requires_exact_next_stage_and_artifact(self):
        record = {"stage": "chapter_intent", "artifacts": {"intent": "intent.json"}}
        valid = validate_stage_transition(record, "context_compiled", "context.json")
        self.assertTrue(valid["valid"])
        skipped = validate_stage_transition(record, "draft_generated", "draft.md")
        self.assertFalse(skipped["valid"])
        missing = validate_stage_transition(record, "context_compiled", "")
        self.assertFalse(missing["valid"])
        revision = {"stage": "revision_generated", "artifacts": {"revision": "revision.md"}}
        self.assertTrue(
            validate_stage_transition(revision, "final_observed", "observation.json")["valid"]
        )
        self.assertFalse(
            validate_stage_transition(revision, "state_settled", "settlement.json")["valid"]
        )

    def test_accepted_chapter_is_immutable(self):
        record = {"stage": STAGES[-1], "artifacts": {"settlement": "settlement.json"}}
        result = validate_stage_transition(record, STAGES[-1], "new.json")
        self.assertFalse(result["valid"])
        self.assertIn("immutable", " ".join(result["errors"]))

    def test_prose_metrics_flag_repetitive_ai_patterns_without_auto_verdict(self):
        text = (
            "然而，他抬起头。不是因为害怕，而是因为命运。\n\n"
            "然而，他握紧手。不是因为愤怒，而是因为选择。\n\n"
            "然而，他向前走。不是因为勇敢，而是因为责任。"
        )
        result = analyze_prose_metrics(text)
        self.assertGreaterEqual(result["transition_word_hits"], 3)
        self.assertGreaterEqual(result["rhetorical_template_hits"], 3)
        self.assertTrue(result["flags"])
        self.assertNotIn("literary_verdict", result)

    def test_prose_metrics_do_not_treat_closing_quotes_as_sentence_starters(self):
        text = "“先关门。”\n\n“把灯递来。”\n\n“雨已经停了。”\n\n“账页还在。”"
        result = analyze_prose_metrics(text)
        self.assertNotIn("sentence_opening_repetition", result["flags"])

    def test_prose_metrics_block_fragmented_ai_tail_loop(self):
        body = "炉火压住了墙根的寒气，众人依次确认手里的灯仍由本人保管。" * 30
        tail = "\n\n".join(f"第{index}格又亮了一次。" for index in range(30))
        result = analyze_prose_metrics(body + "\n\n" + tail)
        self.assertIn("tail_fragmentation_loop", result["flags"])
        self.assertGreaterEqual(result["tail_short_paragraph_ratio"], 0.7)

    def test_prose_metrics_block_prompt_context_leak(self):
        text = "巷口的灯火被冷风压低。\n\n" + '{"contract_path":"runtime.json","required_asset_ids":["asset-a"]}'
        result = analyze_prose_metrics(text)
        self.assertIn("prompt_context_leak", result["flags"])
        self.assertIn('"contract_path"', result["prompt_leak_markers"])

    def test_prose_metrics_block_generation_completion_leak(self):
        result = analyze_prose_metrics("灯火落进槽中。源代码提交确认完毕。测试通过。正文结束。")
        self.assertIn("generation_meta_leak", result["flags"])
        self.assertIn("测试通过", result["generation_meta_markers"])

    def test_prose_metrics_block_latin_word_leak_in_chinese_prose(self):
        result = analyze_prose_metrics("湿滑 of the 石面上，she 仍站在界线外。")
        self.assertIn("latin_token_leak", result["flags"])
        self.assertEqual(result["latin_token_markers"], ["of", "the", "she"])

    def test_prose_metrics_block_repeated_and_oversized_blocks(self):
        repeated = "灯火压低，债链落在石面，持灯人拒绝替另一户开口。" * 25
        result = analyze_prose_metrics(repeated + "\n\n" + repeated)
        self.assertIn("duplicate_text_span", result["flags"])
        self.assertIn("oversized_paragraph_loop", result["flags"])

    def test_prose_metrics_block_termination_token_loop(self):
        result = analyze_prose_metrics("结束。停止。收束。完。终。" * 4)
        self.assertIn("termination_token_loop", result["flags"])

    def test_generated_prose_errors_are_reapplied_after_recovery(self):
        import nrl_production_runtime as runtime

        text = ("正常正文" * 1000) + "\n\n测试通过。正文结束。"
        errors = runtime._generated_prose_errors(text, analyze_prose_metrics(text))
        self.assertIn("prose contains generation or completion metadata", errors)

    def test_external_literary_audit_runs_only_at_five_chapter_checkpoints(self):
        self.assertFalse(requires_external_chapter_audit("chapter-0016", "initial"))
        self.assertTrue(requires_external_chapter_audit("chapter-0020", "initial"))
        self.assertFalse(requires_external_chapter_audit("chapter-0020", "final"))

    def test_context_compiler_selects_only_requested_assets_and_emits_trace(self):
        intent = {
            "chapter_id": "chapter-0001",
            "dramatic_purpose": "force a choice",
            "must_keep": ["cost"],
            "must_avoid": ["free power"],
            "expected_state_deltas": [],
            "required_asset_ids": ["character-a"],
            "active_hook_ids": ["hook-a"],
            "scene_constraints": ["one location"],
        }
        assets = [
            {"asset_id": "character-a", "family": "characters"},
            {"asset_id": "artifact-b", "family": "artifacts"},
        ]
        result = compile_chapter_context_payload(
            intent,
            assets,
            {"story_bible": "a" * 64, "volume_outline": "b" * 64},
            [],
        )
        self.assertTrue(result["valid"])
        self.assertEqual([item["asset_id"] for item in result["context"]["assets"]], ["character-a"])
        self.assertEqual(result["trace"]["excluded_asset_count"], 1)
        intent["required_asset_ids"] = ["missing"]
        self.assertFalse(
            compile_chapter_context_payload(intent, assets, {}, [])["valid"]
        )

    def test_story_window_assets_override_legacy_volume_wide_asset_list(self):
        intent = {
            "chapter_id": "chapter-0048",
            "required_asset_ids": ["character-a", "unrelated-ledger"],
            "active_hook_ids": ["hook-a"],
        }
        assets = [
            {"asset_id": "character-a", "relationships": []},
            {"asset_id": "unrelated-ledger", "relationships": []},
            {"asset_id": "hook-a", "relationships": []},
        ]
        result = compile_chapter_context_payload(
            intent, assets, {}, [], story_beat={"required_asset_ids": ["character-a"]}
        )
        self.assertTrue(result["valid"])
        self.assertEqual(result["trace"]["selected_asset_ids"], ["character-a", "hook-a"])
        self.assertEqual(result["trace"]["legacy_intent_asset_count"], 2)

    def test_rolling_state_replaces_full_settlement_history(self):
        settlements = [
            {
                "chapter_id": f"chapter-{number:04d}",
                "accepted_revision_sha256": str(number) * 64,
                "state_deltas": [{
                    "asset_id": "character-a",
                    "field_path": "character.health",
                    "before": number - 1,
                    "after": number,
                    "evidence": f"evidence-{number}",
                }],
            }
            for number in range(1, 6)
        ]
        snapshot = build_rolling_state_snapshot(settlements)
        self.assertEqual(snapshot["source_chapter_count"], 5)
        self.assertEqual(snapshot["latest_fields"][0]["value"], 5)
        self.assertEqual([item["chapter_id"] for item in snapshot["recent_chapters"]], ["chapter-0004", "chapter-0005"])
        compiled = compile_chapter_context_payload(
            {
                "chapter_id": "chapter-0006", "dramatic_purpose": "test",
                "must_keep": ["state"], "must_avoid": ["drift"],
                "required_asset_ids": ["character-a"], "active_hook_ids": [],
                "scene_constraints": ["bounded"],
            },
            [{"asset_id": "character-a", "family": "characters"}],
            {}, settlements,
        )
        self.assertNotIn("prior_settlements", compiled["context"])
        self.assertEqual(compiled["context"]["rolling_state"]["source_chapter_count"], 5)

    def test_observer_prompt_is_hash_bound_and_excludes_raw_corpus(self):
        payload = build_observer_prompt_payload(
            "chapter-0001", "a" * 64, "正文", {"chapter_id": "chapter-0001"}
        )
        self.assertIn("a" * 64, payload)
        self.assertIn("chapter-0001", payload)
        self.assertNotIn("novel_training_set", payload)

    def test_writer_context_keeps_only_selected_asset_state(self):
        context = {
            "chapter_id": "chapter-0048",
            "assets": [{"asset_id": "character-a", "constraints": ["cost"]}],
            "rolling_state": {
                "source_chapter_count": 47,
                "latest_fields": [
                    {"asset_id": "character-a", "field_path": "health", "value": 2},
                    {"asset_id": "unrelated-ledger", "field_path": "pressure", "value": 99},
                ],
                "recent_chapters": [{
                    "chapter_id": "chapter-0047",
                    "changes": [
                        {"asset_id": "character-a", "field_path": "health", "after": 2},
                        {"asset_id": "unrelated-ledger", "field_path": "pressure", "after": 99},
                    ],
                }],
            },
        }
        compact = runtime._compact_chapter_context(context)
        self.assertEqual([item["asset_id"] for item in compact["rolling_state"]["latest_fields"]], ["character-a"])
        self.assertEqual(len(compact["rolling_state"]["recent_chapters"][0]["changes"]), 1)

    def test_writer_context_caps_latest_fields_and_drops_evidence(self):
        context = {
            "chapter_id": "chapter-0078",
            "writer_asset_ids": ["character-a"],
            "assets": [{"asset_id": "character-a", "constraints": []}],
            "rolling_state": {
                "source_chapter_count": 77,
                "latest_fields": [
                    {
                        "asset_id": "character-a",
                        "field_path": f"field-{index:02d}",
                        "value": index,
                        "chapter_id": f"chapter-{index:04d}",
                        "evidence": "不应进入写作提示" * 100,
                    }
                    for index in range(12)
                ],
                "recent_chapters": [],
            },
        }
        compact = runtime._compact_chapter_context(context)
        latest = compact["rolling_state"]["latest_fields"]
        self.assertEqual(len(latest), 8)
        self.assertEqual(latest[0]["field_path"], "field-04")
        self.assertTrue(all("evidence" not in item for item in latest))

    def test_writer_context_bounds_recent_chapter_deltas(self):
        context = {
            "chapter_id": "chapter-0080",
            "writer_asset_ids": ["character-a"],
            "assets": [{"asset_id": "character-a", "constraints": []}],
            "rolling_state": {
                "source_chapter_count": 79,
                "latest_fields": [],
                "recent_chapters": [
                    {
                        "chapter_id": f"chapter-{chapter:04d}",
                        "accepted_revision_sha256": "a" * 64,
                        "changes": [
                            {
                                "asset_id": "character-a",
                                "field_path": f"field-{index:02d}",
                                "after": "状态" * 100,
                                "evidence": "不应进入写作提示",
                            }
                            for index in range(20)
                        ],
                    }
                    for chapter in (78, 79)
                ],
            },
        }
        compact = runtime._compact_chapter_context(context)
        recent = compact["rolling_state"]["recent_chapters"]
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0]["chapter_id"], "chapter-0079")
        self.assertEqual(len(recent[0]["changes"]), 12)
        self.assertTrue(all("evidence" not in item for item in recent[0]["changes"]))
        self.assertNotIn("accepted_revision_sha256", recent[0])

    def test_observer_context_drops_literary_constraints_but_keeps_asset_ids(self):
        context = {
            "chapter_id": "chapter-0002",
            "writer_asset_ids": ["character-a"],
            "story_beat": {"expected_state_deltas": ["character-a changes"]},
            "assets": [{
                "asset_id": "character-a", "display_name": "甲", "family": "characters",
                "constraints": ["very long literary constraint"],
            }],
            "rolling_state": {"latest_fields": [], "recent_chapters": []},
        }
        compact = runtime._compact_observer_context(context)
        self.assertEqual(compact["assets"][0]["asset_id"], "character-a")
        self.assertNotIn("constraints", compact["assets"][0])

    def test_bundled_writer_observation_is_hash_bound_locally(self):
        facts = [{
            "fact_id": "fact-1", "asset_id": "character_a", "field_path": "health",
            "before": 3, "after": 2, "evidence": "正文中伤口重新裂开",
        }]
        observation = runtime.build_bundled_observation("chapter-0048", "正文", facts)
        self.assertEqual(observation["chapter_id"], "chapter-0048")
        self.assertEqual(len(observation["draft_sha256"]), 64)
        self.assertEqual(observation["facts"]["characters"][0]["fact_id"], "fact-1")

    def test_pipeline_reuses_bundled_observation_without_second_model_call(self):
        intent = {"chapter_id": "chapter-0001"}
        records = iter([
            {"chapter_id": "chapter-0001", "stage": "revision_generated", "artifacts": {"bundled_observation": "candidate.json"}},
            {"chapter_id": "chapter-0001", "stage": "final_observed", "artifacts": {}},
            {"chapter_id": "chapter-0001", "stage": "final_audited", "artifacts": {}},
            {"chapter_id": "chapter-0001", "stage": "state_settled", "artifacts": {}},
            {"chapter_id": "chapter-0001", "stage": "chapter_accepted", "artifacts": {}},
        ])
        with mock.patch.object(runtime, "_read_json", return_value=intent), \
             mock.patch.object(runtime, "_load_registry", side_effect=lambda: {"chapters": [next(records)]}), \
             mock.patch.object(runtime, "ingest_bundled_observation", return_value={"valid": True}), \
             mock.patch.object(runtime, "dispatch_chapter_observation") as observer, \
             mock.patch.object(runtime, "record_deterministic_chapter_audit", return_value={"valid": True}), \
             mock.patch.object(runtime, "build_observed_settlement_candidate", return_value={"candidate": "candidate.json"}), \
             mock.patch.object(runtime, "settle_chapter_state"), \
             mock.patch.object(runtime, "accept_chapter"):
            result = runtime.run_controlled_chapter_pipeline("intent.json")
        self.assertTrue(result["valid"])
        observer.assert_not_called()

    def test_audit_packet_inlines_bound_artifacts_without_raw_corpus(self):
        import nrl_production_runtime as runtime

        context = {"chapter_id": "chapter-0001", "assets": [], "must_keep": ["cost"]}
        rules = {"hard_rules": ["do not invent assets"]}
        trace = {"chapter_id": "chapter-0001"}
        observation = {"chapter_id": "chapter-0001", "facts": {}}
        record = {
            "stage": "draft_generated",
            "artifacts": {
                "context": "context.json", "rule_stack": "rules.json", "trace": "trace.json",
                "draft": "revision.md",
            },
        }
        with mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "runtime_path", side_effect=lambda value: REPO_ROOT / "system/production_runtime/chapters/chapter-0001" / Path(value).name), mock.patch.object(runtime, "_read_json", side_effect=[context, rules, trace, observation]), mock.patch.object(runtime, "_sha256", return_value="a" * 64):
            packet = runtime.build_chapter_audit_packet("chapter-0001")
        text = (REPO_ROOT / packet["packet_path"]).read_text(encoding="utf-8")
        (REPO_ROOT / packet["packet_path"]).unlink()
        self.assertIn("Compact Context", text)
        self.assertIn("Observed Facts", text)
        self.assertNotIn("novel_training_set", text)

    def test_settlement_must_bind_revision_and_resolve_blocking_audit_issues(self):
        revision_hash = "a" * 64
        audit = {
            "verdict": "ACCEPT_WITH_WARNINGS",
            "issues": [
                {"issue_id": "audit-1", "severity": "blocking"},
                {"issue_id": "audit-2", "severity": "minor"},
            ],
        }
        stale = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "b" * 64,
            "state_deltas": [],
            "resolved_audit_ids": ["audit-1"],
        }
        self.assertFalse(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )
        stale["accepted_revision_sha256"] = revision_hash
        stale["resolved_audit_ids"] = []
        self.assertFalse(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )
        stale["resolved_audit_ids"] = ["audit-1"]
        self.assertTrue(
            validate_settlement_payload(stale, "chapter-0001", revision_hash, audit)["valid"]
        )

    def test_acceptance_requires_settlement_bound_to_current_revision(self):
        record = {
            "chapter_id": "chapter-0001",
            "stage": "state_settled",
            "artifacts": {"revision": "revision.md", "settlement": "settlement.json"},
        }
        self.assertFalse(
            validate_acceptance(record, {"accepted_revision_sha256": "a" * 64}, "b" * 64)["valid"]
        )
        self.assertTrue(
            validate_acceptance(record, {"accepted_revision_sha256": "b" * 64}, "b" * 64)["valid"]
        )

    def test_chapter_sequence_requires_immediate_predecessor_acceptance(self):
        self.assertTrue(validate_chapter_sequence([], "chapter-0001")["valid"])
        chapters = [{"chapter_id": "chapter-0001", "stage": "state_settled"}]
        self.assertFalse(validate_chapter_sequence(chapters, "chapter-0002")["valid"])
        chapters[0]["stage"] = "chapter_accepted"
        self.assertTrue(validate_chapter_sequence(chapters, "chapter-0002")["valid"])
        self.assertFalse(validate_chapter_sequence(chapters, "chapter-0003")["valid"])

    def test_rework_required_audit_cannot_be_settled_by_claiming_resolution(self):
        audit = {
            "verdict": "REWORK_REQUIRED",
            "issues": [{"issue_id": "audit-1", "severity": "blocking"}],
        }
        settlement = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "a" * 64,
            "state_deltas": [],
            "resolved_audit_ids": ["audit-1"],
        }
        self.assertFalse(
            validate_settlement_payload(settlement, "chapter-0001", "a" * 64, audit)["valid"]
        )

    def test_settlement_delta_must_match_an_observed_fact(self):
        audit = {"verdict": "ACCEPT", "issues": []}
        settlement = {
            "chapter_id": "chapter-0001",
            "accepted_revision_sha256": "a" * 64,
            "state_deltas": [{
                "fact_id": "fact-1", "asset_id": "character-a", "field_path": "sanity",
                "operation": "set", "before": 10, "after": 9,
            }],
            "resolved_audit_ids": [],
        }
        observation = {"facts": {"characters": [{
            "fact_id": "fact-1", "asset_id": "character-a", "field_path": "sanity",
            "before": 10, "after": 8, "evidence": "scene consequence",
        }]}}
        self.assertFalse(
            validate_settlement_payload(
                settlement, "chapter-0001", "a" * 64, audit, observation=observation
            )["valid"]
        )
        observation["facts"]["characters"][0]["after"] = 9
        self.assertTrue(
            validate_settlement_payload(
                settlement, "chapter-0001", "a" * 64, audit, observation=observation
            )["valid"]
        )

    def test_observed_settlement_candidate_uses_only_observed_facts(self):
        import nrl_production_runtime as runtime

        record = {
            "stage": "final_audited",
            "artifacts": {"observation": "observation.json", "revision": "revision.md"},
        }
        observation = {"facts": {"characters": [{
            "fact_id": "fact-1", "asset_id": "character-a", "field_path": "character.status",
            "before": "before", "after": "after", "evidence": "text",
        }]}}
        with mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}), mock.patch.object(runtime, "_chapter_record", return_value=record), mock.patch.object(runtime, "_read_json", return_value=observation), mock.patch.object(runtime, "_sha256", return_value="a" * 64), mock.patch.object(runtime, "_write_json") as write_json:
            result = runtime.build_observed_settlement_candidate("chapter-0001")
        candidate = write_json.call_args.args[1]
        self.assertEqual(result["state_delta_count"], 1)
        self.assertEqual(candidate["state_deltas"][0]["fact_id"], "fact-1")
        self.assertEqual(candidate["state_deltas"][0]["after"], "after")

    def test_controlled_pipeline_is_idempotent_for_an_accepted_chapter(self):
        import nrl_production_runtime as runtime

        intent = {"chapter_id": "chapter-0001"}
        record = {"chapter_id": "chapter-0001", "stage": "chapter_accepted"}
        with mock.patch.object(runtime, "_read_json", return_value=intent), mock.patch.object(runtime, "_load_registry", return_value={"chapters": [record]}):
            result = runtime.run_controlled_chapter_pipeline("intent.json")
        self.assertTrue(result["valid"])
        self.assertEqual(result["completed"], [])


if __name__ == "__main__":
    unittest.main()
