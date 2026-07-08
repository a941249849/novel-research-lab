#!/usr/bin/env python3
"""Scan local training novels and write a reproducible manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NOVEL_DIR = PROJECT_ROOT / "novel_training_set"
DEFAULT_OUTPUT = PROJECT_ROOT / "phase1" / "00_manifest" / "novel_manifest.csv"
DEFAULT_ENCODINGS = ("utf-8", "gbk", "gb18030")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def detect_and_read(path: Path, encodings: tuple[str, ...]) -> tuple[str, str]:
    errors: list[str] = []
    for encoding in encodings:
        try:
            return encoding, path.read_text(encoding=encoding)
        except UnicodeDecodeError as exc:
            errors.append(f"{encoding}: {exc.reason}")
        except OSError as exc:
            raise RuntimeError(f"failed to read {path}: {exc}") from exc
    raise RuntimeError(
        f"failed to decode {path.name}; tried {', '.join(encodings)}"
        + (f" ({'; '.join(errors)})" if errors else "")
    )


def infer_book_name(file_name: str) -> str:
    stem = Path(file_name).stem
    match = re.search(r"《([^》]+)》", stem)
    if match:
        return match.group(1).strip()
    return stem.strip()


def count_chars(text: str) -> int:
    return sum(1 for char in text if not char.isspace())


def scan_file(path: Path, novel_dir: Path, encodings: tuple[str, ...]) -> dict[str, str | int]:
    file_size_bytes = path.stat().st_size
    sha256 = sha256_file(path)
    relative_path = path.relative_to(PROJECT_ROOT) if path.is_relative_to(PROJECT_ROOT) else path

    try:
        encoding, text = detect_and_read(path, encodings)
        return {
            "file_name": path.name,
            "book_name": infer_book_name(path.name),
            "relative_path": str(relative_path),
            "source_path": str(path.relative_to(novel_dir)),
            "encoding": encoding,
            "char_count": count_chars(text),
            "line_count": len(text.splitlines()),
            "file_size_bytes": file_size_bytes,
            "sha256": sha256,
            "status": "ok",
            "error": "",
        }
    except RuntimeError as exc:
        return {
            "file_name": path.name,
            "book_name": infer_book_name(path.name),
            "relative_path": str(relative_path),
            "source_path": str(path.relative_to(novel_dir)),
            "encoding": "",
            "char_count": 0,
            "line_count": 0,
            "file_size_bytes": file_size_bytes,
            "sha256": sha256,
            "status": "error",
            "error": str(exc),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan novel_training_set txt files and write phase1 novel_manifest.csv."
    )
    parser.add_argument("--novel-dir", type=Path, default=DEFAULT_NOVEL_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--encodings",
        default=",".join(DEFAULT_ENCODINGS),
        help="Comma-separated encodings to try in order. Default: utf-8,gbk,gb18030",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    novel_dir = args.novel_dir.resolve()
    output = args.output.resolve()
    encodings = tuple(item.strip() for item in args.encodings.split(",") if item.strip())

    if not novel_dir.exists():
        print(f"ERROR: novel directory does not exist: {novel_dir}", file=sys.stderr)
        return 2
    if not novel_dir.is_dir():
        print(f"ERROR: novel path is not a directory: {novel_dir}", file=sys.stderr)
        return 2
    if not encodings:
        print("ERROR: at least one encoding must be provided.", file=sys.stderr)
        return 2

    txt_files = sorted(path for path in novel_dir.rglob("*.txt") if path.is_file())
    output.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "file_name",
        "book_name",
        "relative_path",
        "source_path",
        "encoding",
        "char_count",
        "line_count",
        "file_size_bytes",
        "sha256",
        "status",
        "error",
    ]

    rows = [scan_file(path, novel_dir, encodings) for path in txt_files]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    ok_count = sum(1 for row in rows if row["status"] == "ok")
    error_count = len(rows) - ok_count
    print(f"manifest: {output}")
    print(f"scanned_txt_files: {len(rows)}")
    print(f"readable: {ok_count}")
    print(f"errors: {error_count}")
    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
