import os
import json
import stat
import sys
import tempfile
import unittest
import subprocess
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "system/runtime"))

from nrl_codex_writer import (
    _codex_response_schema,
    ask_antigravity_writer,
    ask_codex_structured,
    ask_codex_writer,
    ask_opencode_writer,
    extract_json_object,
)
from nrl_model_router import build_model_routing_status, route_model


class CodexDirectWriterTests(unittest.TestCase):
    def test_routes_assign_models_by_production_risk(self):
        self.assertEqual(route_model("showrunner")["model"], "gpt-5.6-sol")
        self.assertEqual(route_model("reviewer")["model"], "gpt-5.6-sol")
        self.assertEqual(route_model("writer")["model"], "gpt-5.6-terra")
        self.assertEqual(route_model("observer")["model"], "gpt-5.6-luna")
        self.assertEqual(route_model("editor")["fallback_model"], "Gemini 3.5 Flash (High)")
        self.assertEqual(route_model("writer")["fallback_model"], "Gemini 3.1 Pro (High)")
        self.assertEqual(len(build_model_routing_status()["routes"]), 6)

    def test_direct_writer_reads_only_explicit_output_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            binary = root / "codex"
            args_path = root / "args.txt"
            binary.write_text(
                "#!/bin/sh\n"
                "printf '%s\\n' \"$@\" > \"$NRL_FAKE_CODEX_ARGS\"\n"
                "while [ \"$1\" != \"-o\" ]; do shift; done\n"
                "shift\n"
                "printf '正文候选' > \"$1\"\n",
                encoding="utf-8",
            )
            binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
            previous_path = os.environ.get("PATH", "")
            previous_args = os.environ.get("NRL_FAKE_CODEX_ARGS")
            os.environ["PATH"] = f"{root}:{previous_path}"
            os.environ["NRL_FAKE_CODEX_ARGS"] = str(args_path)
            try:
                self.assertEqual(ask_codex_writer("prompt", model="gpt-5.6-terra"), "正文候选")
            finally:
                os.environ["PATH"] = previous_path
                if previous_args is None:
                    os.environ.pop("NRL_FAKE_CODEX_ARGS", None)
                else:
                    os.environ["NRL_FAKE_CODEX_ARGS"] = previous_args
            self.assertIn("--skip-git-repo-check", args_path.read_text(encoding="utf-8"))

    def test_antigravity_writer_is_isolated_and_returns_stdout(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            binary = root / "agy"
            cwd_path = root / "cwd.txt"
            binary.write_text(
                "#!/bin/sh\n"
                "pwd > \"$NRL_FAKE_AGY_CWD\"\n"
                "printf '备用正文'\n",
                encoding="utf-8",
            )
            binary.chmod(binary.stat().st_mode | stat.S_IXUSR)
            previous_path = os.environ.get("PATH", "")
            os.environ["PATH"] = f"{root}:{previous_path}"
            os.environ["NRL_FAKE_AGY_CWD"] = str(cwd_path)
            try:
                result = ask_antigravity_writer("prompt", model="Claude Opus 4.6 (Thinking)")
            finally:
                os.environ["PATH"] = previous_path
                os.environ.pop("NRL_FAKE_AGY_CWD", None)
            self.assertEqual(result, "备用正文")
            self.assertNotEqual(cwd_path.read_text(encoding="utf-8").strip(), str(REPO_ROOT))

    def test_opencode_writer_uses_isolated_direct_adapter(self):
        completed = subprocess.CompletedProcess(
            args=["node"], returncode=0, stdout="独立审查结果\n", stderr=""
        )
        with patch("nrl_codex_writer.shutil.which", return_value="/usr/bin/node"), patch(
            "nrl_codex_writer.subprocess.run", return_value=completed
        ) as run:
            result = ask_opencode_writer("review prompt", model="qwen3.7-max")
        self.assertEqual(result, "独立审查结果")
        args, kwargs = run.call_args
        self.assertEqual(args[0][-1], "qwen3.7-max")
        self.assertNotEqual(Path(kwargs["cwd"]), REPO_ROOT)

    def test_extract_json_object_accepts_fenced_payload(self):
        self.assertEqual(extract_json_object('```json\n{"ok": true}\n```'), {"ok": True})

    def test_structured_timeout_is_a_recoverable_runtime_error(self):
        with patch("nrl_codex_writer.find_codex_binary", return_value="codex"), patch(
            "nrl_codex_writer.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="codex", timeout=1),
        ):
            with self.assertRaisesRegex(RuntimeError, "timed out"):
                ask_codex_structured(
                    "prompt", model="gpt-5.6-sol", schema_path=REPO_ROOT / "missing.json", timeout_seconds=1
                )

    def test_codex_response_schema_removes_provider_unsupported_keywords(self):
        original = {
            "type": "object",
            "required": [],
            "properties": {
                "ids": {
                    "type": "array",
                    "uniqueItems": True,
                    "items": {"type": "string"},
                }
            },
        }

        compatible = _codex_response_schema(original)

        self.assertNotIn("uniqueItems", compatible["properties"]["ids"])
        self.assertEqual(compatible["required"], ["ids"])
        self.assertTrue(original["properties"]["ids"]["uniqueItems"])
        self.assertEqual(original["required"], [])
        self.assertEqual(
            json.dumps(compatible, sort_keys=True),
            json.dumps(_codex_response_schema(compatible), sort_keys=True),
        )

    def test_provider_failure_does_not_persist_prompt_or_warning_flood(self):
        stderr = "\n".join([
            "WARN noisy warning",
            "{\"secret_prompt\": \"must not leak\"}",
            "ERROR: You've hit your usage limit. Try again tomorrow.",
        ])
        with patch("nrl_codex_writer._CODEX_USAGE_LIMITED", False), patch(
            "nrl_codex_writer.find_codex_binary", return_value="codex"
        ), patch(
            "nrl_codex_writer.subprocess.run",
            return_value=subprocess.CompletedProcess("codex", 1, stdout="", stderr=stderr),
        ):
            with self.assertRaises(RuntimeError) as raised:
                ask_codex_writer("prompt", model="gpt-5.6-terra")
        message = str(raised.exception)
        self.assertIn("usage limit", message)
        self.assertNotIn("secret_prompt", message)
        self.assertNotIn("noisy warning", message)


if __name__ == "__main__":
    unittest.main()
