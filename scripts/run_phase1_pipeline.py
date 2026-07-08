#!/usr/bin/env python3
"""Run the minimal Phase 1A local pipeline end to end."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
DEFAULT_DIRS = (
    PROJECT_ROOT / "phase1" / "00_manifest",
    PROJECT_ROOT / "phase1" / "01_skeletons",
    PROJECT_ROOT / "phase1" / "02_book_dna",
    PROJECT_ROOT / "phase1" / "02_narrative_dna",
    PROJECT_ROOT / "phase1" / "02_state_ledgers",
    PROJECT_ROOT / "phase1" / "03_features",
    PROJECT_ROOT / "phase1" / "04_mechanism_library",
    PROJECT_ROOT / "phase1" / "05_review",
)
DEFAULT_MANIFEST = PROJECT_ROOT / "phase1" / "00_manifest" / "novel_manifest.csv"
DEFAULT_REPORT = PROJECT_ROOT / "phase1" / "00_pipeline_run_report.md"


def run_command(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return {
        "command": " ".join(command),
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def read_books(manifest: Path) -> list[str]:
    if not manifest.exists():
        return []
    with manifest.open("r", encoding="utf-8", newline="") as handle:
        return [
            row["book_name"]
            for row in csv.DictReader(handle)
            if row.get("status") == "ok" and row.get("book_name")
        ]


def fenced(text: str) -> str:
    return text if text else "(empty)"


def write_report(path: Path, results: list[dict[str, object]], books: list[str]) -> None:
    failed = [result for result in results if result["returncode"] != 0]
    lines = [
        "# Phase 1A Pipeline Run Report",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- project_root: {PROJECT_ROOT}",
        f"- books_processed_for_stubs: {len(books)}",
        f"- command_count: {len(results)}",
        f"- status: {'fail' if failed else 'pass'}",
        "",
        "## Commands",
        "",
    ]
    for index, result in enumerate(results, 1):
        lines.extend(
            [
                f"### {index}. `{result['command']}`",
                "",
                f"- returncode: {result['returncode']}",
                "",
                "stdout:",
                "```text",
                fenced(str(result["stdout"])),
                "```",
                "",
                "stderr:",
                "```text",
                fenced(str(result["stderr"])),
                "```",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run scan, skeleton extraction, stub generation, and validation.")
    parser.add_argument("--python", default=sys.executable, help="Python executable to use for child scripts.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--novel-dir", type=Path, default=PROJECT_ROOT / "novel_training_set")
    parser.add_argument("--schema-dir", type=Path, default=PROJECT_ROOT / "phase0B" / "03_json_schema_v1")
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of books for skeletons and stubs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    for directory in DEFAULT_DIRS:
        directory.mkdir(parents=True, exist_ok=True)

    py = args.python
    manifest = args.manifest.resolve()
    report = args.report.resolve()
    results: list[dict[str, object]] = []

    scan_cmd = [
        py,
        str(SCRIPTS_DIR / "scan_novels.py"),
        "--novel-dir",
        str(args.novel_dir.resolve()),
        "--output",
        str(manifest),
    ]
    results.append(run_command(scan_cmd))

    extract_cmd = [
        py,
        str(SCRIPTS_DIR / "extract_skeletons.py"),
        "--manifest",
        str(manifest),
        "--output-dir",
        str(PROJECT_ROOT / "phase1" / "01_skeletons"),
    ]
    if args.limit > 0:
        extract_cmd.extend(["--limit", str(args.limit)])
    results.append(run_command(extract_cmd))

    books = read_books(manifest)
    if args.limit > 0:
        books = books[: args.limit]

    builders = (
        ("build_book_dna_stub.py", PROJECT_ROOT / "phase1" / "02_book_dna"),
        ("build_narrative_dna_stub.py", PROJECT_ROOT / "phase1" / "02_narrative_dna"),
        ("build_state_ledger_stub.py", PROJECT_ROOT / "phase1" / "02_state_ledgers"),
    )
    for book in books:
        for script_name, output_dir in builders:
            results.append(
                run_command(
                    [
                        py,
                        str(SCRIPTS_DIR / script_name),
                        book,
                        "--output-dir",
                        str(output_dir),
                    ]
                )
            )

    validate_cmd = [
        py,
        str(SCRIPTS_DIR / "validate_schemas_draft7.py"),
        "--schema-dir",
        str(args.schema_dir.resolve()),
        "--report",
        str(PROJECT_ROOT / "phase1" / "05_review" / "schema_validation_report.md"),
        "--validate-phase1-stubs",
    ]
    results.append(run_command(validate_cmd))

    write_report(report, results, books)
    failed = [result for result in results if result["returncode"] != 0]
    print(f"report: {report}")
    print(f"status: {'fail' if failed else 'pass'}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
