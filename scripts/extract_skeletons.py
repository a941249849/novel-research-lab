#!/usr/bin/env python3
"""Extract deterministic skeleton slices from manifest-listed novels."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "phase1" / "00_manifest" / "novel_manifest.csv"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "phase1" / "01_skeletons"
DEFAULT_OPENING_CHARS = 15000
DEFAULT_MID_WINDOW_CHARS = 2000
DEFAULT_ENDING_CHARS = 10000
DEFAULT_MARKS = (20, 40, 60, 80)


def safe_name(name: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\s]+', "_", name.strip())
    return cleaned.strip("._") or "untitled"


def read_manifest(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"manifest not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    required = {"book_name", "relative_path", "encoding", "status"}
    missing = required.difference(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"manifest missing required columns: {', '.join(sorted(missing))}")
    return rows


def slice_window(text: str, center: int, width: int) -> str:
    start = max(0, center - width // 2)
    end = min(len(text), start + width)
    start = max(0, end - width)
    return text[start:end]


def build_skeleton(book_name: str, file_name: str, text: str, marks: tuple[int, ...], opening_chars: int, mid_window_chars: int, ending_chars: int) -> str:
    parts = [
        f"SKELETON: {book_name}",
        f"Source file: {file_name}",
        f"Total characters including whitespace: {len(text)}",
        "",
        "## opening_15000",
        text[:opening_chars],
        "",
    ]

    for mark in marks:
        center = int(len(text) * (mark / 100))
        parts.extend(
            [
                f"## window_{mark}_percent_{mid_window_chars}",
                slice_window(text, center, mid_window_chars),
                "",
            ]
        )

    parts.extend(["## ending_10000", text[-ending_chars:] if ending_chars else "", ""])
    return "\n".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract opening, mid-point windows, and ending skeleton slices from novels."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--opening-chars", type=int, default=DEFAULT_OPENING_CHARS)
    parser.add_argument("--mid-window-chars", type=int, default=DEFAULT_MID_WINDOW_CHARS)
    parser.add_argument("--ending-chars", type=int, default=DEFAULT_ENDING_CHARS)
    parser.add_argument("--marks", default=",".join(str(item) for item in DEFAULT_MARKS))
    parser.add_argument("--limit", type=int, default=0, help="Optional max number of readable manifest rows to process.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rows = [row for row in read_manifest(args.manifest.resolve()) if row.get("status") == "ok"]
        marks = tuple(int(item.strip()) for item in args.marks.split(",") if item.strip())
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if any(mark <= 0 or mark >= 100 for mark in marks):
        print("ERROR: --marks values must be between 1 and 99.", file=sys.stderr)
        return 2
    if args.opening_chars < 0 or args.mid_window_chars < 0 or args.ending_chars < 0:
        print("ERROR: slice sizes must be non-negative integers.", file=sys.stderr)
        return 2
    if args.limit > 0:
        rows = rows[: args.limit]

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    errors = 0
    for row in rows:
        book_name = row["book_name"]
        source_path = (PROJECT_ROOT / row["relative_path"]).resolve()
        encoding = row["encoding"]
        try:
            text = source_path.read_text(encoding=encoding)
            skeleton = build_skeleton(
                book_name=book_name,
                file_name=row["file_name"],
                text=text,
                marks=marks,
                opening_chars=args.opening_chars,
                mid_window_chars=args.mid_window_chars,
                ending_chars=args.ending_chars,
            )
            output_path = output_dir / f"{safe_name(book_name)}_skeleton.txt"
            output_path.write_text(skeleton, encoding="utf-8")
            written += 1
            print(f"wrote: {output_path}")
        except OSError as exc:
            errors += 1
            print(f"ERROR: failed for {book_name}: {exc}", file=sys.stderr)
        except UnicodeDecodeError as exc:
            errors += 1
            print(f"ERROR: failed decoding {source_path} with {encoding}: {exc}", file=sys.stderr)

    print(f"skeletons_written: {written}")
    print(f"errors: {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
