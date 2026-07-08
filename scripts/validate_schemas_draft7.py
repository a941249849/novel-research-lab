#!/usr/bin/env python3
"""Validate Phase0B schemas and optional Phase1 JSON outputs with Draft-07."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA_DIR = PROJECT_ROOT / "phase0B" / "03_json_schema_v1"
DEFAULT_REPORT = PROJECT_ROOT / "phase1" / "05_review" / "schema_validation_report.md"
PHASE1_STUB_TARGETS = (
    ("book_dna.schema.json", PROJECT_ROOT / "phase1" / "02_book_dna"),
    ("narrative_dna.schema.json", PROJECT_ROOT / "phase1" / "02_narrative_dna"),
    ("state_ledger.schema.json", PROJECT_ROOT / "phase1" / "02_state_ledgers"),
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def format_error(error: Exception) -> str:
    return str(error).replace("\n", " ")


def parse_target(value: str) -> tuple[Path, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("target must use JSON_PATH=SCHEMA_FILE format")
    json_path, schema_name = value.split("=", 1)
    if not json_path or not schema_name:
        raise argparse.ArgumentTypeError("target must include both JSON_PATH and SCHEMA_FILE")
    return Path(json_path), schema_name


def collect_phase1_targets() -> list[tuple[Path, str]]:
    targets: list[tuple[Path, str]] = []
    for schema_name, directory in PHASE1_STUB_TARGETS:
        if directory.exists():
            targets.extend((path, schema_name) for path in sorted(directory.glob("*.json")))
    return targets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate JSON schemas and JSON files with jsonschema Draft-07.")
    parser.add_argument("--schema-dir", type=Path, default=DEFAULT_SCHEMA_DIR)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument(
        "--target",
        type=parse_target,
        action="append",
        default=[],
        help="Optional JSON validation target in JSON_PATH=SCHEMA_FILE format. May be repeated.",
    )
    parser.add_argument(
        "--validate-phase1-stubs",
        action="store_true",
        help="Validate JSON files in standard Phase1 stub output directories.",
    )
    return parser.parse_args()


def main() -> int:
    try:
        import jsonschema
        from jsonschema import Draft7Validator
    except ImportError:
        print("ERROR: missing dependency 'jsonschema'. Install it with: python3 -m pip install jsonschema", file=sys.stderr)
        return 2

    args = parse_args()
    schema_dir = args.schema_dir.resolve()
    report_path = args.report.resolve()
    if not schema_dir.exists():
        print(f"ERROR: schema directory does not exist: {schema_dir}", file=sys.stderr)
        return 2

    schema_files = sorted(schema_dir.glob("*.schema.json"))
    if not schema_files:
        print(f"ERROR: no *.schema.json files found in: {schema_dir}", file=sys.stderr)
        return 2

    lines = [
        "# Draft-07 Schema Validation Report",
        "",
        f"- generated_at: {datetime.now().isoformat(timespec='seconds')}",
        f"- schema_dir: {schema_dir}",
        "",
        "## Schema Checks",
        "",
    ]

    schemas: dict[str, object] = {}
    ok = True
    for schema_path in schema_files:
        try:
            schema = load_json(schema_path)
            Draft7Validator.check_schema(schema)
            schemas[schema_path.name] = schema
            lines.append(f"- PASS `{schema_path.name}`")
        except (OSError, json.JSONDecodeError, jsonschema.exceptions.SchemaError) as exc:
            ok = False
            lines.append(f"- FAIL `{schema_path.name}`: {format_error(exc)}")

    targets = list(args.target)
    if args.validate_phase1_stubs:
        targets.extend(collect_phase1_targets())

    lines.extend(["", "## JSON Instance Checks", ""])
    if not targets:
        lines.append("- SKIP no JSON instance targets requested")
    else:
        for json_path, schema_name in targets:
            json_path = json_path.resolve()
            try:
                schema = schemas.get(schema_name)
                if schema is None:
                    raise ValueError(f"schema not loaded: {schema_name}")
                data = load_json(json_path)
                validator = Draft7Validator(schema)
                errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
                if errors:
                    ok = False
                    first = errors[0]
                    location = ".".join(str(part) for part in first.path) or "<root>"
                    lines.append(f"- FAIL `{json_path}` against `{schema_name}`: {location}: {first.message}")
                else:
                    lines.append(f"- PASS `{json_path}` against `{schema_name}`")
            except (OSError, json.JSONDecodeError, ValueError) as exc:
                ok = False
                lines.append(f"- FAIL `{json_path}` against `{schema_name}`: {format_error(exc)}")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"report: {report_path}")
    print("status: pass" if ok else "status: fail")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
