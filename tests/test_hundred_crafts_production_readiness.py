from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ID = "hundred-crafts-night-procession"
WORKSPACE = ROOT / "projects" / PROJECT_ID
sys.path.insert(0, str(ROOT / "system/runtime"))

import nrl_project_production as project_production  # noqa: E402
import nrl_volume1_release as volume_release  # noqa: E402
from nrl_project_production import build_production_batch_plan  # noqa: E402


class HundredCraftsProductionReadinessTests(unittest.TestCase):
    def run_cli(self, *args: str, expected: int = 0) -> dict:
        result = subprocess.run(
            [sys.executable, "system/runtime/nrl.py", "--project", PROJECT_ID, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stderr + result.stdout)
        return json.loads(result.stdout)

    def run_runtime_expression(self, source: str) -> object:
        env = {**os.environ, "NRL_PROJECT_ID": PROJECT_ID}
        result = subprocess.run(
            [sys.executable, "-c", source],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_prepared_contract_has_66_chapters_and_seven_windows(self) -> None:
        validated = self.run_cli("project-production-validate")
        self.assertTrue(validated["valid"])
        self.assertEqual(validated["chapter_count"], 66)
        self.assertEqual(validated["window_count"], 7)
        last = WORKSPACE / "production_runtime/story_windows/window-061-066.v1.json"
        payload = json.loads(last.read_text(encoding="utf-8"))
        self.assertEqual(payload["window"]["end"], 66)
        self.assertEqual(len(payload["chapters"]), 6)

    def test_formal_batch_plan_uses_project_intents_and_one_window(self) -> None:
        plan = build_production_batch_plan(1, 10, PROJECT_ID)
        self.assertEqual(plan["project_id"], PROJECT_ID)
        self.assertEqual(plan["window"], [1, 10])
        self.assertTrue(plan["review_after_batch"])
        self.assertTrue(plan["independent_review_required"])
        self.assertEqual(len(plan["intent_paths"]), 10)
        self.assertTrue(
            all(
                path.startswith(
                    f"projects/{PROJECT_ID}/production_runtime/intents/"
                )
                and path.endswith(".json")
                and "longform_volume1_v025" not in path
                for path in plan["intent_paths"]
            )
        )
        with self.assertRaisesRegex(RuntimeError, "cannot cross"):
            build_production_batch_plan(10, 11, PROJECT_ID)

    def test_causal_repairs_are_explicit_and_distinct(self) -> None:
        manifest = json.loads(
            (WORKSPACE / "production_runtime/plans/volume1_production_manifest.v1.json").read_text(encoding="utf-8")
        )
        chapters = {int(item["chapter_id"][-4:]): item for item in manifest["chapters"]}
        self.assertIn("v1.ch019.outcome", chapters[29]["requires_state_ids"])
        self.assertIn("v1.ch041.outcome", chapters[54]["requires_state_ids"])
        self.assertIn("v1.ch029.outcome", chapters[60]["requires_state_ids"])
        self.assertEqual(len({chapters[number]["material_action"] for number in (19, 29, 60)}), 3)
        self.assertEqual(chapters[33]["required_asset_ids"].count("faction_maintenance_team"), 1)

    def test_character_arcs_and_maintenance_team_lifecycle(self) -> None:
        store = json.loads((WORKSPACE / "creation_assets/project_assets.json").read_text(encoding="utf-8"))
        assets = {item["asset_id"]: item for item in store["assets"]}
        self.assertEqual(assets["faction_maintenance_team"]["lifecycle_state"], "seed")
        characters = [item for item in store["assets"] if item["family"] == "characters"]
        self.assertEqual(len(characters), 5)
        for item in characters:
            arc = item["character"]["arc"]
            self.assertTrue(arc["volume1_terminal_state"])
            self.assertTrue(arc["series_target_state"])
            self.assertTrue(arc["residual_conflict"])
            self.assertNotEqual(arc["volume1_terminal_state"], arc["series_target_state"])

    def test_legacy_owner_scopes_cannot_authorize_this_project(self) -> None:
        result = self.run_runtime_expression(
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_production_runtime import has_bounded_prose_authorization;"
            "d=[{'decision_type':'authorize_controlled_prose_test','authorized_scope':['longform_volume1_v025:chapter-0001'],'forbidden_scope':[]}];"
            "print(json.dumps(has_bounded_prose_authorization(d,'chapter-0001')))"
        )
        self.assertFalse(result)

    def test_fake_review_hashes_cannot_authorize_prose(self) -> None:
        baseline = WORKSPACE / "creation_assets/canonical_baseline.json"
        sha = hashlib.sha256(baseline.read_bytes()).hexdigest()
        decision = {
            "decision_type": "authorize_controlled_prose_test",
            "project_id": PROJECT_ID,
            "authorized_scope": [f"project_volume1_v1:{PROJECT_ID}:chapter-0001"],
            "forbidden_scope": [
                f"{PROJECT_ID}:chapter-0011-or-later",
                f"{PROJECT_ID}:bulk-or-continuous-production",
                f"{PROJECT_ID}:publish",
            ],
            "expires_after_mission": f"{PROJECT_ID}-volume1-window-001-010-v1",
            "bound_baseline_sha256": sha,
            "bound_sol_review_sha256": "a" * 64,
            "bound_antigravity_review_sha256": "b" * 64,
        }
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_production_runtime import has_bounded_prose_authorization;"
            f"d={decision!r};print(json.dumps(has_bounded_prose_authorization([d],'chapter-0001')))"
        )
        self.assertFalse(self.run_runtime_expression(source))
        decision["bound_baseline_sha256"] = "0" * 64
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_production_runtime import has_bounded_prose_authorization;"
            f"d={decision!r};print(json.dumps(has_bounded_prose_authorization([d],'chapter-0001')))"
        )
        self.assertFalse(self.run_runtime_expression(source))

    def test_compact_context_preserves_payload_and_expected_deltas(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_production_runtime import _compact_chapter_context;"
            "c={'chapter_id':'chapter-0001','writer_asset_ids':['char_zhou_li'],"
            "'assets':[{'asset_id':'char_zhou_li','display_name':'周砺','family':'characters','character':{'goals':['查明责任']},'constraints':['接受复核']}],"
            "'expected_state_deltas':[{'asset_id':'char_zhou_li','field_path':'character.current_state'}],'rolling_state':{'latest_fields':[],'recent_chapters':[]}};"
            "print(json.dumps(_compact_chapter_context(c),ensure_ascii=False))"
        )
        compact = self.run_runtime_expression(source)
        self.assertEqual(compact["assets"][0]["character"]["goals"], ["查明责任"])
        self.assertEqual(compact["expected_state_deltas"][0]["field_path"], "character.current_state")

    def test_first_window_review_blocks_chapter_11(self) -> None:
        result = self.run_runtime_expression(
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_volume1_release import prior_window_review_required;"
            "print(json.dumps(prior_window_review_required('chapter-0011')))"
        )
        self.assertTrue(result)

    def test_first_window_requires_independent_review(self) -> None:
        result = self.run_runtime_expression(
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_volume1_release import window_requires_independent_review;"
            "print(json.dumps(window_requires_independent_review(1,10)))"
        )
        self.assertTrue(result)

    def test_release_root_is_project_isolated(self) -> None:
        result = self.run_runtime_expression(
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "from nrl_volume1_release import RELEASE_ROOT,ROOT;"
            "print(json.dumps(str(RELEASE_ROOT.relative_to(ROOT))))"
        )
        self.assertEqual(
            result,
            f"projects/{PROJECT_ID}/releases/fanqie/volume1",
        )

    def test_settlement_rejects_unknown_stale_undeclared_and_illegal_state(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_production_runtime as r;"
            "rec={'chapter_id':'chapter-0001','stage':'final_audited','artifacts':{'intent':'projects/hundred-crafts-night-procession/production_runtime/intents/chapter-0001.json'}};"
            "r._load_registry=lambda:{'chapters':[rec]};"
            "audit={'verdict':'ACCEPT','issues':[]}\n"
            "def check(asset,field,before,after):\n"
            " o={'facts':{'characters':[{'fact_id':'f','asset_id':asset,'field_path':field,'before':before,'after':after}]}}\n"
            " s={'chapter_id':'chapter-0001','accepted_revision_sha256':'a'*64,'resolved_audit_ids':[],'state_deltas':[{'fact_id':'f','asset_id':asset,'field_path':field,'before':before,'after':after}]}\n"
            " return r.validate_settlement_payload(s,'chapter-0001','a'*64,audit,o)['errors']\n"
            "cases=[check('missing_asset','character.current_state','x','y'),check('char_zhou_li','character.unknown','x','y'),check('char_zhou_li','character.current_state','wrong','y'),check('faction_maintenance_team','lifecycle_state','seed','active')];"
            "print(json.dumps(cases,ensure_ascii=False))"
        )
        cases = self.run_runtime_expression(source)
        self.assertTrue(all(cases))
        self.assertIn("unknown settlement asset", " ".join(cases[0]))
        self.assertIn("unregistered settlement field", " ".join(cases[1]))
        self.assertIn("stale settlement before value", " ".join(cases[2]))
        self.assertIn("not declared by chapter intent", " ".join(cases[3]))

    def test_settlement_rejects_missing_frozen_intent_delta(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_production_runtime as r;"
            "rec={'chapter_id':'chapter-0001','stage':'final_audited','artifacts':{'intent':'projects/hundred-crafts-night-procession/production_runtime/intents/chapter-0001.json'}};"
            "r._load_registry=lambda:{'chapters':[rec]};"
            "s={'chapter_id':'chapter-0001','accepted_revision_sha256':'a'*64,'resolved_audit_ids':[],'state_deltas':[]};"
            "print(json.dumps(r.validate_settlement_payload(s,'chapter-0001','a'*64,{'verdict':'ACCEPT','issues':[]},{'facts':{}}),ensure_ascii=False))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["valid"])
        self.assertTrue(any("missing frozen intent state delta" in item for item in result["errors"]))

    def test_final_reviewer_execution_must_bind_exact_audit_and_revision(self) -> None:
        runtime_root = WORKSPACE / "production_runtime"
        with tempfile.TemporaryDirectory(dir=runtime_root) as directory:
            folder = Path(directory)
            revision = folder / "revision.md"
            audit = folder / "final_audit.json"
            execution = folder / "reviewer.execution.json"
            revision.write_text("正文", encoding="utf-8")
            audit.write_text(
                json.dumps({"artifact_sha256": hashlib.sha256(revision.read_bytes()).hexdigest()}),
                encoding="utf-8",
            )
            execution.write_text(
                json.dumps({
                    "chapter_id": "chapter-0001",
                    "role": "reviewer",
                    "artifact": str(audit.relative_to(ROOT)),
                    "artifact_sha256": "0" * 64,
                    "audit_artifact_sha256": "0" * 64,
                    "revision_sha256": "0" * 64,
                    "provider": "codex",
                    "model": "gpt-5.6-sol",
                }),
                encoding="utf-8",
            )
            record = {
                "chapter_id": "chapter-0001",
                "artifacts": {
                    "revision": str(revision.relative_to(ROOT)),
                    "reviewer_execution": str(execution.relative_to(ROOT)),
                },
            }
            source = (
                "import json,sys;sys.path.insert(0,'system/runtime');"
                "from pathlib import Path;from nrl_production_runtime import validate_role_execution;"
                f"record={record!r};"
                f"print(json.dumps(validate_role_execution(record,'reviewer',Path({str(audit)!r})),ensure_ascii=False))"
            )
            result = self.run_runtime_expression(source)
        self.assertFalse(result["valid"])
        self.assertIn("reviewer execution audit hash mismatch", result["errors"])
        self.assertIn("reviewer execution revision hash mismatch", result["errors"])

    def test_formal_primary_window_review_rejects_antigravity_fallback_identity(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64,'source_kind':'accepted_revision'}]}};"
            "p={'window':'1-10','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'verdict':'ACCEPT','findings':[],'review_provider':'antigravity','review_model':'Claude Opus 4.6 (Thinking)','fallback_used':True};"
            "\ntry:\n r.record_window_review(p);print(json.dumps({'accepted':True}))\nexcept RuntimeError as e:\n print(json.dumps({'accepted':False,'error':str(e)}))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["accepted"])
        self.assertIn("Codex gpt-5.6-sol", result["error"])

    def test_formal_window_review_rejects_self_reported_sol_without_execution(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64,'source_kind':'accepted_revision'}]}};"
            "p={'window':'1-10','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'verdict':'ACCEPT','findings':[],'review_provider':'codex','review_model':'gpt-5.6-sol','fallback_used':False};"
            "\ntry:\n r.record_window_review(p);print(json.dumps({'accepted':True}))\nexcept RuntimeError as e:\n print(json.dumps({'accepted':False,'error':str(e)}))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["accepted"])
        self.assertIn("execution evidence", result["error"])

    def test_independent_window_review_rejects_model_mismatch_before_write(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64,'source_kind':'accepted_revision'}]}};"
            "r._independent_window_path=lambda s,e:(_ for _ in ()).throw(AssertionError('write path reached'));"
            "r._window_execution_path=lambda s,e,independent=False:(_ for _ in ()).throw(AssertionError('execution write path reached'));"
            "p={'window':'1-10','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'verdict':'ACCEPT','findings':[],'review_provider':'antigravity','review_model':'Gemini 3.5 Flash (High)'};"
            "e={'role':'independent_window_reviewer','window':'001-010','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'provider':'antigravity','model':'Claude Opus 4.6 (Thinking)'};"
            "\ntry:\n r.record_independent_window_review(p,e);print(json.dumps({'accepted':True}))\nexcept RuntimeError as error:\n print(json.dumps({'accepted':False,'error':str(error)}))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["accepted"])
        self.assertIn("does not match execution evidence", result["error"])

    def test_chapter_11_rechecks_persisted_window_execution_identity(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "existing=r.ROOT/'projects/hundred-crafts-night-procession/production_runtime/production_readiness/audit-contract.v0.1.json';"
            "r._window_path=lambda s,e:existing;"
            "r._window_requires_independent_review=lambda s,e:False;"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64}]}};"
            "r._read_json=lambda p:{'verdict':'ACCEPT','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'review_provider':'antigravity','review_model':'fallback','fallback_used':True};"
            "print(json.dumps({'blocked':r.prior_window_review_required('chapter-0011')}))"
        )
        result = self.run_runtime_expression(source)
        self.assertTrue(result["blocked"])

    def test_formal_pipeline_never_uses_bundled_writer_observation(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_production_runtime as r;"
            "rec={'chapter_id':'chapter-0001','stage':'revision_generated','artifacts':{}};calls=[];"
            "r._load_registry=lambda:{'chapters':[rec]};r._chapter_record=lambda registry,cid:rec;"
            "r.ingest_bundled_observation=lambda cid:(_ for _ in ()).throw(RuntimeError('bundled used'));"
            "r.dispatch_chapter_observation=lambda cid:(calls.append('observer') or rec.update(stage='final_observed') or {'valid':True});"
            "r.dispatch_chapter_audit=lambda cid,model=None:{'valid':False,'errors':['stop after observation']};"
            "r._read_json=lambda path:{'chapter_id':'chapter-0001'};"
            "result=r.run_controlled_chapter_pipeline('ignored.json');"
            "print(json.dumps({'calls':calls,'errors':result.get('errors',[])}))"
        )
        result = self.run_runtime_expression(source)
        self.assertEqual(result["calls"], ["observer"])

    def test_formal_audit_packet_forbids_empty_dimension_evidence(self) -> None:
        source = (
            "import inspect,json,sys;sys.path.insert(0,'system/runtime');"
            "import nrl_production_runtime as r;"
            "text=inspect.getsource(r.build_chapter_audit_packet);"
            "print(json.dumps({'guard':"
            "'Every array under dimensions must contain at least one specific evidence sentence' in text}))"
        )
        result = self.run_runtime_expression(source)
        self.assertTrue(result["guard"])

    def test_formal_audit_evidence_rejects_generic_and_duplicate_claims(self) -> None:
        keys = project_production.AUDIT_EVIDENCE_DIMENSIONS if hasattr(
            project_production, "AUDIT_EVIDENCE_DIMENSIONS"
        ) else (
            "canon", "character", "state", "causality", "pacing",
            "life_force", "anti_ai_taste", "originality",
            "semantic_realization", "progression_permissions",
            "history_coherence",
        )
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');"
            "import nrl_production_runtime as r;"
            f"keys={keys!r};"
            "ground='周砺查看旧梁，在签认页发现父亲名字，并要求住户见证复核。';"
            "good={'dimensions':{k:[f'周砺在旧梁现场留下第{i}项可核对判断'] for i,k in enumerate(keys)}};"
            "generic={'dimensions':{k:['checked'] for k in keys}};"
            "duplicate={'dimensions':{k:['周砺查看旧梁并要求现场复核'] for k in keys}};"
            "print(json.dumps({"
            "'good':r.validate_grounded_literary_audit_evidence(good,ground)['valid'],"
            "'generic':r.validate_grounded_literary_audit_evidence(generic,ground)['valid'],"
            "'duplicate':r.validate_grounded_literary_audit_evidence(duplicate,ground)['valid']}))"
        )
        result = self.run_runtime_expression(source)
        self.assertTrue(result["good"])
        self.assertFalse(result["generic"])
        self.assertFalse(result["duplicate"])

    def test_chapter_33_carries_the_only_team_activation_contract(self) -> None:
        manifest = json.loads(
            (WORKSPACE / "production_runtime/plans/volume1_production_manifest.v1.json").read_text(encoding="utf-8")
        )
        activations = [
            (item["chapter_id"], delta)
            for item in manifest["chapters"]
            for delta in item["expected_state_deltas"]
            if delta["asset_id"] == "faction_maintenance_team"
            and delta["field_path"] == "lifecycle_state"
            and delta["after"] == "active"
        ]
        self.assertEqual(len(activations), 1)
        self.assertEqual(activations[0][0], "chapter-0033")
        self.assertEqual(activations[0][1]["before"], "seed")

    def test_baseline_locks_policy_titles_intents_and_quality_contract(self) -> None:
        baseline = json.loads((WORKSPACE / "creation_assets/canonical_baseline.json").read_text(encoding="utf-8"))
        paths = {item["path"] for item in baseline["canonical_inputs"]}
        self.assertIn(
            "projects/hundred-crafts-night-procession/production_runtime/production_readiness/audit-contract.v0.1.json",
            paths,
        )
        self.assertIn(
            "projects/hundred-crafts-night-procession/production_runtime/chapter_titles.volume1.json",
            paths,
        )
        self.assertIn(
            "projects/hundred-crafts-night-procession/production_runtime/intents/chapter-0066.json",
            paths,
        )
        self.assertIn(
            "projects/hundred-crafts-night-procession/production_runtime/quality/first_window_quality_contract.v1.json",
            paths,
        )
        self.assertIn("system/runtime/nrl_production_runtime.py", paths)
        self.assertIn("system/runtime/nrl_antigravity_bridge.py", paths)
        self.assertIn("system/runtime/nrl_owner_gate.py", paths)
        self.assertIn(
            "system/production_runtime/schemas/continuity_audit.schema.json",
            paths,
        )
        runtime_sources = {
            f"system/runtime/{path.name}"
            for path in (ROOT / "system/runtime").glob("*.py")
        }
        self.assertTrue(runtime_sources.issubset(paths))

    def test_authorization_validates_registry_before_any_write(self) -> None:
        authorization = {
            "project_id": PROJECT_ID,
            "decisions": [
                {"decision_id": "owner_window_intent"},
                {"decision_id": "owner_window_prose"},
            ],
        }
        project = json.loads(
            (ROOT / "system/projects" / PROJECT_ID / "project.json").read_text(
                encoding="utf-8"
            )
        )
        with mock.patch.object(
            project_production,
            "build_project_window_authorization",
            return_value=authorization,
        ), mock.patch.object(
            project_production, "load_decisions", return_value=[]
        ), mock.patch.object(
            project_production, "load_project", return_value=project
        ), mock.patch.object(
            project_production,
            "load_project_registry",
            return_value={"projects": []},
        ), mock.patch.object(
            project_production, "_write_json"
        ) as write_json, mock.patch.object(
            project_production, "save_decisions"
        ) as save_decisions:
            with self.assertRaisesRegex(RuntimeError, "registry entry is missing"):
                project_production.authorize_project_production_window(
                    1, 10, "owner_window", "approved"
                )
        write_json.assert_not_called()
        save_decisions.assert_not_called()

    def test_review_document_must_bind_verdict_and_baseline_text(self) -> None:
        baseline = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            review = Path(directory) / "review.md"
            review.write_text(
                f"# Review\n\nBASELINE: {baseline}\n\nVERDICT: ACCEPT\n",
                encoding="utf-8",
            )
            self.assertTrue(
                project_production._review_document_accepts(
                    review, baseline, {"ACCEPT"}
                )
            )
            self.assertFalse(
                project_production._review_document_accepts(
                    review, "b" * 64, {"ACCEPT"}
                )
            )
            review.write_text(
                f"# Review\n\nBASELINE: {baseline}f\n\nVERDICT: ACCEPT\n",
                encoding="utf-8",
            )
            self.assertFalse(
                project_production._review_document_accepts(
                    review, baseline, {"ACCEPT"}
                )
            )
            review.write_text(
                f"# Review\n\nBASELINE: {baseline}\n\n"
                "VERDICT: ACCEPT\nVERDICT: ACCEPT\n",
                encoding="utf-8",
            )
            self.assertFalse(
                project_production._review_document_accepts(
                    review, baseline, {"ACCEPT"}
                )
            )

    def test_provider_aware_independent_review_requires_execution_and_degradation_evidence(self) -> None:
        baseline = "a" * 64
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review = root / "review.md"
            request = root / "request.md"
            provider_log = root / "provider-attempt.json"
            unavailable = root / "unavailable.json"
            execution = root / "execution.json"
            review.write_text(
                f"BASELINE: {baseline}\n\nVERDICT: ACCEPT\n", encoding="utf-8"
            )
            request.write_text("independent review request", encoding="utf-8")
            provider_log.write_text(
                '{"returncode":1,"error":"provider unavailable"}\n',
                encoding="utf-8",
            )
            unavailable.write_text(
                json.dumps(
                    {
                        "preferred_provider": "antigravity",
                        "status": "unavailable",
                        "bound_baseline_sha256": baseline,
                        "attempts": [
                            {
                                "provider": "antigravity",
                                "returncode": 1,
                                "result": "quota_exhausted",
                                "started_at": "2026-07-25T00:00:00+08:00",
                                "finished_at": "2026-07-25T00:00:05+08:00",
                                "request_artifact": str(request),
                                "request_artifact_sha256": hashlib.sha256(
                                    request.read_bytes()
                                ).hexdigest(),
                                "log_artifact": "provider-attempt.json",
                                "log_artifact_sha256": hashlib.sha256(
                                    provider_log.read_bytes()
                                ).hexdigest(),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            execution.write_text(
                json.dumps(
                    {
                        "provider": "opencode-go",
                        "model": "qwen3.7-max",
                        "returncode": 0,
                        "started_at": "2026-07-25T00:00:00+08:00",
                        "finished_at": "2026-07-25T00:01:00+08:00",
                        "bound_baseline_sha256": baseline,
                        "request_artifact": "request.md",
                        "request_artifact_sha256": hashlib.sha256(
                            request.read_bytes()
                        ).hexdigest(),
                        "review_artifact": "review.md",
                        "review_artifact_sha256": hashlib.sha256(
                            review.read_bytes()
                        ).hexdigest(),
                    }
                ),
                encoding="utf-8",
            )
            index = {
                "independent_review_provider": "opencode-go",
                "independent_review_model": "qwen3.7-max",
                "independent_review_verdict": "ACCEPT",
                "independent_review_path": "review.md",
                "independent_review_sha256": hashlib.sha256(
                    review.read_bytes()
                ).hexdigest(),
                "independent_review_execution_path": "execution.json",
                "independent_review_execution_sha256": hashlib.sha256(
                    execution.read_bytes()
                ).hexdigest(),
                "degradation_reason": "Antigravity quota exhausted",
                "preferred_provider_unavailable_evidence_path": "unavailable.json",
                "preferred_provider_unavailable_evidence_sha256": hashlib.sha256(
                    unavailable.read_bytes()
                ).hexdigest(),
            }
            with mock.patch.object(project_production, "ROOT", root):
                binding = project_production.resolve_independent_review_binding(
                    index, baseline
                )
                self.assertEqual(binding["provider"], "opencode-go")
                impersonated = dict(index, independent_review_provider="antigravity")
                self.assertIsNone(
                    project_production.resolve_independent_review_binding(
                        impersonated, baseline
                    )
                )
                stale = dict(index, independent_review_execution_sha256="0" * 64)
                self.assertIsNone(
                    project_production.resolve_independent_review_binding(
                        stale, baseline
                    )
                )
                invalid_unavailable = json.loads(
                    unavailable.read_text(encoding="utf-8")
                )
                invalid_unavailable["attempts"][0]["returncode"] = 0
                invalid_unavailable["attempts"][0]["result"] = "success"
                self.assertFalse(
                    project_production.validate_provider_unavailable_evidence(
                        invalid_unavailable, baseline
                    )
                )

    def test_independent_window_review_rejects_unknown_provider(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64,'source_kind':'accepted_revision'}]}};"
            "p={'window':'1-10','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'verdict':'ACCEPT','findings':[],'review_provider':'codex','review_model':'gpt-5.6-sol'};"
            "e={'role':'independent_window_reviewer','window':'001-010','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'provider':'codex','model':'gpt-5.6-sol'};"
            "\ntry:\n r.record_independent_window_review(p,e);print(json.dumps({'accepted':True}))\nexcept RuntimeError as error:\n print(json.dumps({'accepted':False,'error':str(error)}))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["accepted"])
        self.assertIn("approved external provider", result["error"])

    def test_opencode_window_review_requires_unavailable_evidence(self) -> None:
        source = (
            "import json,sys;sys.path.insert(0,'system/runtime');import nrl_volume1_release as r;"
            "request=r.ROOT/'projects/hundred-crafts-night-procession/production_runtime/quality/first_window_quality_contract.v1.json';"
            "r.build_window_review_packet=lambda s,e:{'valid':True,'packet':{'chapter_ids':['chapter-0001'],'chapters':[{'chapter_id':'chapter-0001','revision_sha256':'a'*64,'source_kind':'accepted_revision'}]}};"
            "r._independent_window_path=lambda s,e:(_ for _ in ()).throw(AssertionError('write path reached'));"
            "p={'window':'1-10','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'verdict':'ACCEPT','findings':[],'review_provider':'opencode-go','review_model':'qwen3.7-max'};"
            "e={'role':'independent_window_reviewer','window':'001-010','chapter_ids':['chapter-0001'],'revision_hashes':{'chapter-0001':'a'*64},'provider':'opencode-go','model':'qwen3.7-max','returncode':0,'started_at':'2026-07-25T00:00:00+08:00','finished_at':'2026-07-25T00:01:00+08:00','bound_baseline_sha256':r._current_baseline_sha256(),'request_artifact':str(request.relative_to(r.ROOT)),'request_artifact_sha256':r._sha256(request)};"
            "\ntry:\n r.record_independent_window_review(p,e);print(json.dumps({'accepted':True}))\nexcept RuntimeError as error:\n print(json.dumps({'accepted':False,'error':str(error)}))"
        )
        result = self.run_runtime_expression(source)
        self.assertFalse(result["accepted"])
        self.assertIn("unavailable evidence", result["error"])

    def test_opencode_window_review_accepts_complete_execution_chain(self) -> None:
        baseline = "b" * 64
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review_root = root / "reviews"
            review_root.mkdir()
            request = root / "request.md"
            provider_log = root / "provider-log.json"
            unavailable = root / "unavailable.json"
            request.write_text("window review request", encoding="utf-8")
            provider_log.write_text('{"returncode":1}\n', encoding="utf-8")
            unavailable.write_text(
                json.dumps(
                    {
                        "preferred_provider": "antigravity",
                        "status": "unavailable",
                        "bound_baseline_sha256": baseline,
                        "attempts": [
                            {
                                "provider": "antigravity",
                                "returncode": 1,
                                "result": "provider_error",
                                "started_at": "2026-07-25T00:00:00+08:00",
                                "finished_at": "2026-07-25T00:00:05+08:00",
                                "request_artifact": str(request),
                                "request_artifact_sha256": hashlib.sha256(
                                    request.read_bytes()
                                ).hexdigest(),
                                "log_artifact": str(provider_log),
                                "log_artifact_sha256": hashlib.sha256(
                                    provider_log.read_bytes()
                                ).hexdigest(),
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            payload = {
                "window": "1-10",
                "chapter_ids": ["chapter-0001"],
                "revision_hashes": {"chapter-0001": "a" * 64},
                "verdict": "ACCEPT",
                "findings": [],
                "review_provider": "opencode-go",
                "review_model": "qwen3.7-max",
            }
            execution = {
                "role": "independent_window_reviewer",
                "window": "001-010",
                "chapter_ids": ["chapter-0001"],
                "revision_hashes": {"chapter-0001": "a" * 64},
                "provider": "opencode-go",
                "model": "qwen3.7-max",
                "returncode": 0,
                "started_at": "2026-07-25T00:01:00+08:00",
                "finished_at": "2026-07-25T00:02:00+08:00",
                "bound_baseline_sha256": baseline,
                "request_artifact": str(request),
                "request_artifact_sha256": hashlib.sha256(
                    request.read_bytes()
                ).hexdigest(),
                "preferred_provider_unavailable_evidence": str(unavailable),
                "preferred_provider_unavailable_evidence_sha256": hashlib.sha256(
                    unavailable.read_bytes()
                ).hexdigest(),
            }
            packet = {
                "valid": True,
                "packet": {
                    "chapter_ids": ["chapter-0001"],
                    "chapters": [
                        {
                            "chapter_id": "chapter-0001",
                            "revision_sha256": "a" * 64,
                            "source_kind": "accepted_revision",
                        }
                    ],
                },
            }
            with mock.patch.object(
                volume_release, "ROOT", root
            ), mock.patch.object(
                volume_release, "REVIEW_ROOT", review_root
            ), mock.patch.object(
                volume_release, "runtime_path", side_effect=lambda value: root / value
            ), mock.patch.object(
                volume_release, "_current_baseline_sha256", return_value=baseline
            ), mock.patch.object(
                volume_release, "build_window_review_packet", return_value=packet
            ):
                result = volume_release.record_independent_window_review(
                    payload, execution
                )
            self.assertTrue(result["valid"])
            self.assertTrue((review_root / "window-001-010.independent.json").is_file())
            self.assertTrue(
                (review_root / "window-001-010.independent.execution.json").is_file()
            )

    def test_authorization_failure_before_activation_stays_fail_closed(self) -> None:
        authorization = {
            "project_id": PROJECT_ID,
            "decisions": [
                {"decision_id": "owner_window_intent"},
                {"decision_id": "owner_window_prose"},
            ],
        }
        project = json.loads(
            (ROOT / "system/projects" / PROJECT_ID / "project.json").read_text(
                encoding="utf-8"
            )
        )
        original_authorized = project["content_authorized"]
        events: list[str] = []

        def staged_write(path: Path, payload: object) -> None:
            if path == project_production.project_config_path(PROJECT_ID):
                raise OSError("injected activation write failure")
            events.append(f"write:{path.name}")

        with mock.patch.object(
            project_production,
            "build_project_window_authorization",
            return_value=authorization,
        ), mock.patch.object(
            project_production, "load_decisions", return_value=[]
        ), mock.patch.object(
            project_production, "load_project", return_value=dict(project)
        ), mock.patch.object(
            project_production,
            "load_project_registry",
            return_value={"projects": [{"project_id": PROJECT_ID, "status": "owner_gate"}]},
        ), mock.patch.object(
            project_production, "_write_json", side_effect=staged_write
        ), mock.patch.object(
            project_production,
            "save_decisions",
            side_effect=lambda decisions: events.append("write:decisions"),
        ):
            with self.assertRaisesRegex(OSError, "activation write failure"):
                project_production.authorize_project_production_window(
                    1, 10, "owner_window", "approved"
                )
        self.assertEqual(events, ["write:registry.v1.json", "write:decisions"])
        persisted = json.loads(
            (ROOT / "system/projects" / PROJECT_ID / "project.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(persisted["content_authorized"], original_authorized)

    def test_samples_are_not_formal_registry_entries(self) -> None:
        registry = json.loads(
            (WORKSPACE / "production_runtime/chapter_registry.v0.20.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            [entry["chapter_id"] for entry in registry["chapters"]],
            [f"chapter-{number:04d}" for number in range(1, 8)],
        )
        self.assertTrue(
            all(entry["stage"] == "chapter_accepted" for entry in registry["chapters"])
        )
        self.assertTrue(
            all(
                "controlled_samples" not in artifact_path
                for entry in registry["chapters"]
                for artifact_path in entry["artifacts"].values()
            )
        )
        manifest = json.loads(
            (WORKSPACE / "production_runtime/plans/volume1_production_manifest.v1.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["canonicalization"]["controlled_samples"], "calibration_evidence_only")
        self.assertFalse(manifest["canonicalization"]["sample_import_allowed"])


if __name__ == "__main__":
    unittest.main()
