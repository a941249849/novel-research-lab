#!/usr/bin/env python3
"""Build a schema-valid placeholder NarrativeDNA JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "phase1" / "02_narrative_dna"


def safe_name(name: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\s]+', "_", name.strip())
    return cleaned.strip("._") or "untitled"


def build_stub(book_name: str) -> dict[str, object]:
    return {
        "plot_checkpoints": [],
        "pacing_metrics": {
            "target_suppression_to_release_ratio": "1:3",
            "description": f"Placeholder narrative pacing metrics for {book_name}.",
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a NarrativeDNA placeholder JSON file.")
    parser.add_argument("book_name", help="Book name used in JSON content and default output file name.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--output", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.book_name.strip():
        print("ERROR: book_name cannot be empty.", file=sys.stderr)
        return 2

    output = args.output.resolve() if args.output else args.output_dir.resolve() / f"{safe_name(args.book_name)}_narrative.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_stub(args.book_name), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
