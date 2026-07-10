import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"


class VerifiableDeepReadingV018Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        corpus = self.root / "novel_training_set"
        corpus.mkdir()
        self.book = corpus / "《测试长篇》作者：测试.txt"
        self.book.write_bytes(
            "第一章 起点\n".encode() + b"A" * 140
            + "第二章 转折\n".encode() + b"B" * 140
            + "第三章 收束\n".encode() + b"C" * 140
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, *args):
        env = os.environ.copy()
        env["NRL_ROOT"] = str(self.root)
        return subprocess.run(
            [sys.executable, str(NRL), *args],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

    def plan(self):
        result = self.run_cli("deep-read-plan", "--target-bytes", "180")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def write_response(self, chunk, *, bad_hash=False):
        response = self.root / chunk["response_path"]
        response.parent.mkdir(parents=True, exist_ok=True)
        manifest = {
            "job_id": "job-v018-verifiable-deep-reading",
            "contract_version": "0.18",
            "chunk_id": chunk["chunk_id"],
            "source_file": chunk["source_file"],
            "source_file_sha256": chunk["source_file_sha256"],
            "start_byte": chunk["start_byte"],
            "end_byte": chunk["end_byte"],
            "chunk_sha256": "bad" if bad_hash else chunk["chunk_sha256"],
            "analysis": {
                "chapter_span": chunk["chapter_headings"],
                "major_events": ["事件推进"],
                "character_state_transitions": ["人物状态发生变化"],
                "long_form_mechanisms": ["压力与兑现形成连续循环"],
                "continuity_observations": ["承接上一范围并留下后续问题"],
                "style_observations": ["叙述节奏随冲突变化"],
                "creation_family_evidence": {
                    "characters": ["人物目标与代价绑定"],
                    "state_ledger": ["关键状态发生可追踪变化"],
                },
                "originality_risks": ["只迁移抽象机制"],
            },
        }
        response.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")

    def test_plan_covers_every_byte_without_gap_or_overlap(self):
        plan = self.plan()
        chunks = plan["books"][0]["chunks"]
        self.assertGreater(len(chunks), 1)
        self.assertEqual(chunks[0]["start_byte"], 0)
        self.assertEqual(chunks[-1]["end_byte"], self.book.stat().st_size)
        for left, right in zip(chunks, chunks[1:]):
            self.assertEqual(left["end_byte"], right["start_byte"])
        self.assertEqual(plan["coverage_bytes"], plan["total_size_bytes"])
        self.assertEqual(plan["coverage_ratio"], 1.0)

    def test_status_never_treats_legacy_sample_proof_as_deep_read(self):
        validation = self.root / "system/agent_ops/validation/full_corpus_proof_v0.8.json"
        validation.parent.mkdir(parents=True, exist_ok=True)
        validation.write_text(
            json.dumps({"status": "proof_verified", "verified_receipts": 1}),
            encoding="utf-8",
        )
        result = self.run_cli("deep-read-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        status = json.loads(result.stdout)
        self.assertEqual(status["status"], "missing")
        self.assertEqual(status["legacy_v08_effective_status"], "access_sample_verified")
        self.assertFalse(status["deep_read_verified"])

    def test_all_chunk_responses_are_required_for_coverage_verification(self):
        plan = self.plan()
        chunks = plan["books"][0]["chunks"]
        self.write_response(chunks[0])
        result = self.run_cli("deep-read-validate-all")
        self.assertEqual(result.returncode, 1)
        validation = json.loads(result.stdout)
        self.assertEqual(validation["status"], "in_progress")
        self.assertEqual(validation["validated_chunk_count"], 1)
        self.assertEqual(validation["required_chunk_count"], len(chunks))

    def test_chunk_response_must_bind_to_planned_hash(self):
        plan = self.plan()
        chunk = plan["books"][0]["chunks"][0]
        self.write_response(chunk, bad_hash=True)
        result = self.run_cli(
            "deep-read-validate-chunk", "--chunk-id", chunk["chunk_id"]
        )
        self.assertEqual(result.returncode, 1)
        validation = json.loads(result.stdout)
        self.assertFalse(validation["valid"])
        self.assertIn("chunk_sha256 mismatch", validation["errors"])

    def test_full_chunk_set_reaches_chunk_coverage_verified_only(self):
        plan = self.plan()
        chunks = plan["books"][0]["chunks"]
        for chunk in chunks:
            self.write_response(chunk)
        result = self.run_cli("deep-read-validate-all")
        self.assertEqual(result.returncode, 0, result.stderr)
        validation = json.loads(result.stdout)
        self.assertEqual(validation["status"], "chunk_coverage_verified")
        self.assertFalse(validation["deep_read_verified"])
        self.assertEqual(validation["validated_byte_ratio"], 1.0)


if __name__ == "__main__":
    unittest.main()
