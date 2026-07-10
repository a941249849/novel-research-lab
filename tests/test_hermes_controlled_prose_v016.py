import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = REPO_ROOT / "system/runtime"
sys.path.insert(0, str(RUNTIME_DIR))

from nrl_hermes_bridge import ask_hermes, build_hermes_execution_status
from nrl_hermes_controlled_prose import (
    build_controlled_prose_readiness,
    build_controlled_prose_prompt,
    dispatch_controlled_prose_test,
    validate_controlled_prose_text,
)


class HermesControlledProseV016Tests(unittest.TestCase):
    def setUp(self):
        self.decision = {
            "decision_id": "owner_gate_controlled_prose_001",
            "decision_type": "authorize_controlled_prose_test",
            "authorized_scope": ["generate_controlled_prose_test"],
            "forbidden_scope": ["generate_full_chapter"],
            "expires_after_mission": "phase2g_controlled_prose_test",
        }
        self.audit = "# Antigravity Final Assets Audit v0.16\n\n## Verdict\n\nACCEPT_WITH_WARNINGS\n"

    def test_cli_bridge_is_ready_when_fake_hermes_is_available(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            binary = Path(temp_dir) / "hermes"
            binary.write_text("#!/bin/sh\nprintf 'Hermes Agent v0.test\\n'\n", encoding="utf-8")
            binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
            old_value = os.environ.get("NRL_HERMES_BIN")
            os.environ["NRL_HERMES_BIN"] = str(binary)
            try:
                status = build_hermes_execution_status({"mode": "cli_bridge"})
            finally:
                if old_value is None:
                    os.environ.pop("NRL_HERMES_BIN", None)
                else:
                    os.environ["NRL_HERMES_BIN"] = old_value
        self.assertTrue(status["available"])
        self.assertTrue(status["can_execute_controlled_prose_test"])

    def test_bridge_pins_codex_provider_when_overriding_model(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            args_path = temp_path / "args.txt"
            binary = temp_path / "hermes"
            binary.write_text(
                "#!/bin/sh\nprintf '%s\\n' \"$@\" > \"$NRL_FAKE_HERMES_ARGS\"\nprintf 'scene'\n",
                encoding="utf-8",
            )
            binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
            old_binary = os.environ.get("NRL_HERMES_BIN")
            old_args = os.environ.get("NRL_FAKE_HERMES_ARGS")
            os.environ["NRL_HERMES_BIN"] = str(binary)
            os.environ["NRL_FAKE_HERMES_ARGS"] = str(args_path)
            try:
                self.assertEqual(ask_hermes("test"), "scene")
            finally:
                if old_binary is None:
                    os.environ.pop("NRL_HERMES_BIN", None)
                else:
                    os.environ["NRL_HERMES_BIN"] = old_binary
                if old_args is None:
                    os.environ.pop("NRL_FAKE_HERMES_ARGS", None)
                else:
                    os.environ["NRL_FAKE_HERMES_ARGS"] = old_args
            self.assertIn("--provider", args_path.read_text(encoding="utf-8"))
            self.assertIn("openai-codex", args_path.read_text(encoding="utf-8"))

    def test_readiness_requires_audited_matching_owner_decision(self):
        blocked = build_controlled_prose_readiness([], self.audit)
        ready = build_controlled_prose_readiness([self.decision], self.audit)
        self.assertFalse(blocked["allowed"])
        self.assertTrue(ready["allowed"])
        self.assertFalse(ready["content_production_allowed"])

    def test_validator_accepts_bounded_sensory_scene_and_rejects_schema_jargon(self):
        good = (
            "泥灯巷的灰雨贴上陆沉渊手背，暗红的寿痕沿着骨节亮起。"
            "他想起母亲的寿债，仍把回灯盏按在阵砖上。街坊没有退开，"
            "有人扶住裂墙，有人替他遮住冷灰。命火回卷时，他鬓角白了一寸，"
            "胸骨像被烧裂，却只看见巷口那盏灯重新有了暖色。"
        ) * 9
        valid = validate_controlled_prose_text(good)
        invalid = validate_controlled_prose_text(good + " ledger schema metric")
        self.assertTrue(valid["valid"], valid["errors"])
        self.assertFalse(invalid["valid"])
        self.assertIn("reader_facing_jargon", {item["code"] for item in invalid["errors"]})

    def test_dispatch_captures_validated_stdout_only_after_gate(self):
        prose = (
            "泥灯巷的灰雨贴上陆沉渊手背，暗红的寿痕沿着骨节亮起。"
            "他想起母亲的寿债，仍把回灯盏按在阵砖上。街坊没有退开，"
            "有人扶住裂墙，有人替他遮住冷灰。命火回卷时，他鬓角白了一寸，"
            "胸骨像被烧裂，却只看见巷口那盏灯重新有了暖色。"
        ) * 9
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "controlled-prose.md"
            result = dispatch_controlled_prose_test(
                "bounded prompt",
                [self.decision],
                self.audit,
                output_path,
                invoke=lambda _: prose,
            )
            self.assertTrue(result["valid"])
            self.assertEqual(output_path.read_text(encoding="utf-8"), prose)

    def test_dispatch_does_not_call_hermes_when_owner_gate_is_missing(self):
        called = False

        def invoke(_: str) -> str:
            nonlocal called
            called = True
            return "unexpected"

        with tempfile.TemporaryDirectory() as temp_dir:
            result = dispatch_controlled_prose_test(
                "bounded prompt", [], self.audit, Path(temp_dir) / "output.md", invoke=invoke
            )
        self.assertFalse(result["valid"])
        self.assertFalse(called)

    def test_prompt_uses_only_approved_context_without_raw_corpus_path(self):
        prompt = build_controlled_prose_prompt()
        self.assertIn("陆沉渊", prompt)
        self.assertIn("ACCEPT_WITH_WARNINGS", prompt)
        self.assertNotIn("novel_training_set/", prompt)


if __name__ == "__main__":
    unittest.main()
