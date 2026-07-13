import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "system/runtime"))

from nrl_codex_writer import ask_antigravity_writer, ask_codex_writer, extract_json_object
from nrl_model_router import build_model_routing_status, route_model


class CodexDirectWriterTests(unittest.TestCase):
    def test_routes_assign_models_by_production_risk(self):
        self.assertEqual(route_model("showrunner")["model"], "gpt-5.6-sol")
        self.assertEqual(route_model("writer")["model"], "gpt-5.6-sol")
        self.assertEqual(route_model("observer")["model"], "gpt-5.6-luna")
        self.assertEqual(route_model("writer")["fallback_model"], "Claude Opus 4.6 (Thinking)")
        self.assertEqual(len(build_model_routing_status()["routes"]), 4)

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

    def test_extract_json_object_accepts_fenced_payload(self):
        self.assertEqual(extract_json_object('```json\n{"ok": true}\n```'), {"ok": True})


if __name__ == "__main__":
    unittest.main()
