import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
NRL = REPO_ROOT / "system/runtime/nrl.py"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class FullCorpusProofGateV08Tests(unittest.TestCase):
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

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        shutil.copytree(
            REPO_ROOT / "system/mission_controller",
            self.root / "system/mission_controller",
        )
        (self.root / "system/runtime").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            REPO_ROOT / "system/runtime/agent_adapters.json",
            self.root / "system/runtime/agent_adapters.json",
        )
        self.corpus_dir = self.root / "novel_training_set"
        self.corpus_dir.mkdir()
        self.book_a = self.corpus_dir / "《测试甲》作者：甲.txt"
        self.book_b = self.corpus_dir / "《测试乙》作者：乙.txt"
        self.book_a.write_bytes((b"A" * 64) + (b"B" * 64) + (b"C" * 64) + (b"D" * 64))
        self.book_b.write_bytes((b"E" * 64) + (b"F" * 64) + (b"G" * 64) + (b"H" * 64))
        self.review_path = self.root / "system/agent_ops/inbox/proof-review.md"
        self.review_path.parent.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write_review(self, manifest):
        self.review_path.write_text(
            "\n".join(
                [
                    "# Proof Review",
                    "## JSON Manifest",
                    "```json",
                    json.dumps(manifest, ensure_ascii=False, indent=2),
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def valid_receipt(self, path: Path, title: str):
        data = path.read_bytes()
        rel = str(path.relative_to(self.root))
        segments = []
        phases = ["early", "middle", "late", "ending"]
        for index, phase in enumerate(phases):
            start = index * 64
            end = start + 64
            segments.append(
                {
                    "chunk_id": f"{title}-{phase}",
                    "phase": phase,
                    "start_byte": start,
                    "end_byte": end,
                    "chunk_sha256": sha256_bytes(data[start:end]),
                }
            )
        return {
            "book_title": title,
            "source_file": rel,
            "source_file_size_bytes": len(data),
            "source_file_sha256": sha256_bytes(data),
            "read_scope": "full_text_reviewed",
            "segments": segments,
        }

    def test_status_reports_corpus_inventory_without_reading_prose(self):
        result = self.run_cli("full-corpus-proof-status")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.8")
        self.assertEqual(data["corpus_inventory"]["file_count"], 2)
        self.assertEqual(data["corpus_inventory"]["total_size_bytes"], 512)
        self.assertEqual(data["required_receipts"], 2)
        self.assertEqual(data["promotion_allowed"], False)

    def test_validate_rejects_schema_valid_review_without_reading_receipts(self):
        self.write_review(
            {
                "job_id": "job-v07-full-corpus-antigravity-review",
                "contract_version": "0.7",
                "book_reviews": [
                    {"book_title": "测试甲", "read_scope": "full_text_reviewed"},
                    {"book_title": "测试乙", "read_scope": "full_text_reviewed"},
                ],
            }
        )
        result = self.run_cli(
            "full-corpus-proof-validate",
            "--file",
            str(self.review_path.relative_to(self.root)),
        )
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "schema_valid_but_depth_unverified")
        self.assertIn("reading_receipts must be a list", data["errors"])
        self.assertEqual(data["promotion_allowed"], False)

    def test_validate_accepts_receipts_with_verified_file_and_chunk_hashes(self):
        self.write_review(
            {
                "job_id": "job-v08-full-corpus-proof-review",
                "contract_version": "0.8",
                "reading_receipts": [
                    self.valid_receipt(self.book_a, "测试甲"),
                    self.valid_receipt(self.book_b, "测试乙"),
                ],
            }
        )
        result = self.run_cli(
            "full-corpus-proof-validate",
            "--file",
            str(self.review_path.relative_to(self.root)),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "proof_verified")
        self.assertEqual(data["verified_receipts"], 2)
        self.assertEqual(data["promotion_allowed"], False)

    def test_validate_rejects_missing_phase_chunk_coverage(self):
        receipt = self.valid_receipt(self.book_a, "测试甲")
        receipt["segments"] = receipt["segments"][:3]
        self.write_review(
            {
                "job_id": "job-v08-full-corpus-proof-review",
                "contract_version": "0.8",
                "reading_receipts": [receipt, self.valid_receipt(self.book_b, "测试乙")],
            }
        )
        result = self.run_cli(
            "full-corpus-proof-validate",
            "--file",
            str(self.review_path.relative_to(self.root)),
        )
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertIn("missing required phase coverage", "\n".join(data["errors"]))

    def test_validate_partial_receipts_reports_verified_count_without_promotion(self):
        self.write_review(
            {
                "job_id": "job-v08-full-corpus-proof-review",
                "contract_version": "0.8",
                "reading_receipts": [self.valid_receipt(self.book_a, "测试甲")],
            }
        )
        result = self.run_cli(
            "full-corpus-proof-validate",
            "--file",
            str(self.review_path.relative_to(self.root)),
        )
        self.assertNotEqual(result.returncode, 0)
        data = json.loads(result.stdout)
        self.assertEqual(data["status"], "schema_valid_but_depth_unverified")
        self.assertEqual(data["verified_receipts"], 1)
        self.assertEqual(data["required_receipts"], 2)
        self.assertEqual(data["promotion_allowed"], False)

    def test_pack_writes_one_antigravity_request_per_corpus_file(self):
        result = self.run_cli("full-corpus-proof-pack", "--all")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["version"], "0.8")
        self.assertEqual(data["request_count"], 2)
        request_paths = [item["request_path"] for item in data["requests"]]
        self.assertEqual(len(set(request_paths)), 2)
        for item in data["requests"]:
            request_path = self.root / item["request_path"]
            self.assertTrue(request_path.exists())
            text = request_path.read_text(encoding="utf-8")
            self.assertIn("Do not quote raw prose", text)
            self.assertIn("reading_receipt", text)

    def test_merge_combines_per_book_receipts_into_master_manifest(self):
        input_dir = self.root / "system/agent_ops/inbox/full_corpus_proof_v0.8"
        input_dir.mkdir(parents=True, exist_ok=True)
        receipts = [
            self.valid_receipt(self.book_a, "测试甲"),
            self.valid_receipt(self.book_b, "测试乙"),
        ]
        receipts[0]["segments"][0]["chunk_id"] = "chapter_1_header"
        for index, receipt in enumerate(
            [
                receipts[0],
                receipts[1],
            ],
            start=1,
        ):
            (input_dir / f"{index:02d}_response.md").write_text(
                "\n".join(
                    [
                        "# Per Book Proof",
                        "## JSON Manifest",
                        "```json",
                        json.dumps(
                            {
                                "job_id": "job-v08-full-corpus-proof-review",
                                "contract_version": "0.8",
                                "reading_receipts": [receipt],
                            },
                            ensure_ascii=False,
                            indent=2,
                        ),
                        "```",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        output_file = self.root / "system/agent_ops/inbox/full_corpus_proof_v0.8/master.md"
        merge = self.run_cli(
            "full-corpus-proof-merge",
            "--input-dir",
            str(input_dir.relative_to(self.root)),
            "--output-file",
            str(output_file.relative_to(self.root)),
        )
        self.assertEqual(merge.returncode, 0, merge.stderr)
        data = json.loads(merge.stdout)
        self.assertEqual(data["receipt_count"], 2)
        self.assertTrue(output_file.exists())
        self.assertNotIn("chapter_1_header", output_file.read_text(encoding="utf-8"))
        validate = self.run_cli(
            "full-corpus-proof-validate",
            "--file",
            str(output_file.relative_to(self.root)),
        )
        self.assertEqual(validate.returncode, 0, validate.stderr)


if __name__ == "__main__":
    unittest.main()
