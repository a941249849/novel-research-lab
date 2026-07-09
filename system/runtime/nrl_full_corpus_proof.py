from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_owner_gate import load_decisions
from nrl_paths import ROOT, runtime_path


VERSION = "0.8"
JOB_ID = "job-v08-full-corpus-proof-review"
PROMOTION_SCOPE = "promote_full_corpus_proof_to_research_assets"
REQUIRED_PHASES = ("early", "middle", "late", "ending")
REQUEST_DIR = runtime_path("system/agent_ops/packets/full_corpus_proof_v0.8")
VALIDATION_PATH = runtime_path("system/agent_ops/validation/full_corpus_proof_v0.8.json")
FULL_CORPUS_PROOF_MASTER = runtime_path(
    "system/agent_ops/inbox/full_corpus_proof_v0.8/master.md"
)
PROMOTION_MANIFEST_PATH = runtime_path(
    "system/research_assets/promotions/full_corpus_proof_v0.9.json"
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_to_root(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def corpus_files() -> list[Path]:
    corpus_dir = runtime_path("novel_training_set")
    if not corpus_dir.exists():
        return []
    return sorted(path for path in corpus_dir.glob("*.txt") if path.is_file())


def build_corpus_inventory(include_hashes: bool = False) -> dict[str, Any]:
    files = []
    total_size = 0
    for path in corpus_files():
        size = path.stat().st_size
        total_size += size
        item = {
            "source_file": _relative_to_root(path),
            "file_name": path.name,
            "size_bytes": size,
        }
        if include_hashes:
            item["sha256"] = _sha256_file(path)
        files.append(item)
    return {
        "file_count": len(files),
        "total_size_bytes": total_size,
        "files": files,
    }


def build_proof_status() -> dict[str, Any]:
    inventory = build_corpus_inventory(include_hashes=False)
    latest_validation = load_latest_validation()
    promotion_readiness = build_promotion_readiness(latest_validation)
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "status": "proof_gate_ready",
        "corpus_inventory": inventory,
        "required_receipts": inventory["file_count"],
        "required_phases": list(REQUIRED_PHASES),
        "latest_validation": latest_validation,
        "promotion_readiness": promotion_readiness,
        "promotion_allowed": promotion_readiness["promotion_allowed"],
        "commands": {
            "pack": "python3 system/runtime/nrl.py full-corpus-proof-pack --all",
            "validate": "python3 system/runtime/nrl.py full-corpus-proof-validate --file <path>",
            "promote": "python3 system/runtime/nrl.py full-corpus-proof-promote",
        },
    }


def load_latest_validation() -> dict[str, Any] | None:
    if not VALIDATION_PATH.exists():
        return None
    try:
        return json.loads(VALIDATION_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "status": "invalid_validation_json",
            "valid": False,
            "path": _relative_to_root(VALIDATION_PATH),
        }


def build_promotion_readiness(latest_validation: dict[str, Any] | None) -> dict[str, Any]:
    proof_verified = bool(latest_validation and latest_validation.get("status") == "proof_verified")
    required = int(latest_validation.get("required_receipts", 0)) if latest_validation else 0
    verified = int(latest_validation.get("verified_receipts", 0)) if latest_validation else 0
    decision = _latest_full_corpus_promotion_decision() if proof_verified else None
    if decision:
        return {
            "status": "promotable_research_asset",
            "proof_verified": proof_verified,
            "verified_receipts": verified,
            "required_receipts": required,
            "promotion_allowed": True,
            "owner_decision_id": decision["decision_id"],
            "next_required_action": "Promote the verified proof into research-asset ingestion; prose remains blocked.",
            "forbidden_actions": _promotion_forbidden_actions(decision),
        }
    return {
        "status": "blocked_on_owner_gate" if proof_verified else "blocked_on_proof_verification",
        "proof_verified": proof_verified,
        "verified_receipts": verified,
        "required_receipts": required,
        "promotion_allowed": False,
        "next_required_action": (
            "Owner must explicitly authorize research-asset promotion."
            if proof_verified
            else "Complete full-corpus proof verification before promotion."
        ),
        "forbidden_actions": [
            "auto_promote_research_assets",
            "generate_novel_prose",
            "execute_hermes",
        ],
    }


def _latest_full_corpus_promotion_decision() -> dict[str, Any] | None:
    for decision in reversed(load_decisions()):
        if decision.get("decision_type") != "authorize_research_promotion":
            continue
        scopes = set(decision.get("authorized_scope", []))
        if PROMOTION_SCOPE not in scopes:
            continue
        if decision.get("expires_after_mission") != JOB_ID:
            continue
        return decision
    return None


def _promotion_forbidden_actions(decision: dict[str, Any]) -> list[str]:
    forbidden = list(decision.get("forbidden_scope", []))
    forbidden.extend(["generate_novel_prose", "execute_hermes"])
    return sorted(dict.fromkeys(str(item) for item in forbidden))


def _resolve_repo_path(file_arg: str) -> Path:
    path = Path(file_arg)
    if not path.is_absolute():
        path = ROOT / path
    return path.resolve()


def _extract_manifest(text: str) -> tuple[dict[str, Any] | None, str | None]:
    pattern = r"## JSON Manifest\s*```json\s*(.*?)\s*```"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        return None, "missing JSON Manifest fenced json block"
    try:
        manifest = json.loads(match.group(1))
    except json.JSONDecodeError as error:
        return None, f"invalid JSON Manifest: {error}"
    if not isinstance(manifest, dict):
        return None, "JSON Manifest must be an object"
    return manifest, None


def _read_manifest(file_arg: str) -> tuple[dict[str, Any] | None, list[str]]:
    path = _resolve_repo_path(file_arg)
    if not path.exists():
        return None, [f"review file does not exist: {file_arg}"]
    manifest, error = _extract_manifest(path.read_text(encoding="utf-8"))
    return manifest, [error] if error else []


def _validate_segment(receipt_index: int, receipt: dict[str, Any], data: bytes) -> list[str]:
    errors: list[str] = []
    segments = receipt.get("segments")
    if not isinstance(segments, list) or not segments:
        return [f"receipt[{receipt_index}].segments must be a non-empty list"]
    seen_phases: set[str] = set()
    for segment_index, segment in enumerate(segments):
        if not isinstance(segment, dict):
            errors.append(f"receipt[{receipt_index}].segments[{segment_index}] must be an object")
            continue
        phase = segment.get("phase")
        if phase not in REQUIRED_PHASES:
            errors.append(f"receipt[{receipt_index}].segments[{segment_index}].phase is invalid")
        else:
            seen_phases.add(str(phase))
        start = segment.get("start_byte")
        end = segment.get("end_byte")
        if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end <= start or end > len(data):
            errors.append(f"receipt[{receipt_index}].segments[{segment_index}] has invalid byte range")
            continue
        expected = segment.get("chunk_sha256")
        actual = _sha256_bytes(data[start:end])
        if expected != actual:
            errors.append(f"receipt[{receipt_index}].segments[{segment_index}].chunk_sha256 mismatch")
    missing = sorted(set(REQUIRED_PHASES) - seen_phases)
    if missing:
        errors.append(f"receipt[{receipt_index}] missing required phase coverage: {', '.join(missing)}")
    return errors


def _validate_receipt(receipt_index: int, receipt: Any, expected_files: dict[str, Path]) -> list[str]:
    if not isinstance(receipt, dict):
        return [f"receipt[{receipt_index}] must be an object"]
    errors: list[str] = []
    source_file = receipt.get("source_file")
    if not isinstance(source_file, str):
        return [f"receipt[{receipt_index}].source_file must be a string"]
    if source_file not in expected_files:
        return [f"receipt[{receipt_index}].source_file is not in corpus inventory: {source_file}"]
    path = expected_files[source_file]
    data = path.read_bytes()
    if receipt.get("read_scope") != "full_text_reviewed":
        errors.append(f"receipt[{receipt_index}].read_scope must be full_text_reviewed")
    if receipt.get("source_file_size_bytes") != len(data):
        errors.append(f"receipt[{receipt_index}].source_file_size_bytes mismatch")
    if receipt.get("source_file_sha256") != _sha256_bytes(data):
        errors.append(f"receipt[{receipt_index}].source_file_sha256 mismatch")
    if not receipt.get("book_title"):
        errors.append(f"receipt[{receipt_index}].book_title is required")
    errors.extend(_validate_segment(receipt_index, receipt, data))
    return errors


def validate_proof_file(file_arg: str) -> dict[str, Any]:
    manifest, errors = _read_manifest(file_arg)
    inventory_paths = {_relative_to_root(path): path for path in corpus_files()}
    if manifest is None:
        result = _validation_result(file_arg, "schema_valid_but_depth_unverified", errors, 0, len(inventory_paths))
        _write_json(VALIDATION_PATH, result)
        return result
    receipts = manifest.get("reading_receipts")
    if not isinstance(receipts, list):
        errors.append("reading_receipts must be a list")
        result = _validation_result(file_arg, "schema_valid_but_depth_unverified", errors, 0, len(inventory_paths))
        _write_json(VALIDATION_PATH, result)
        return result
    seen_files: set[str] = set()
    verified_receipts = 0
    for index, receipt in enumerate(receipts):
        if isinstance(receipt, dict) and isinstance(receipt.get("source_file"), str):
            seen_files.add(str(receipt["source_file"]))
        receipt_errors = _validate_receipt(index, receipt, inventory_paths)
        if receipt_errors:
            errors.extend(receipt_errors)
        else:
            verified_receipts += 1
    missing_receipts = sorted(set(inventory_paths) - seen_files)
    extra_receipts = sorted(seen_files - set(inventory_paths))
    if missing_receipts:
        errors.append(f"missing reading receipts for corpus files: {', '.join(missing_receipts)}")
    if extra_receipts:
        errors.append(f"unknown reading receipts: {', '.join(extra_receipts)}")
    status = "proof_verified" if not errors else "schema_valid_but_depth_unverified"
    result = _validation_result(file_arg, status, errors, verified_receipts, len(inventory_paths))
    _write_json(VALIDATION_PATH, result)
    return result


def merge_proof_receipts(input_dir_arg: str, output_file_arg: str) -> dict[str, Any]:
    input_dir = _resolve_repo_path(input_dir_arg)
    if not input_dir.exists() or not input_dir.is_dir():
        raise RuntimeError(f"proof input dir does not exist: {input_dir_arg}")
    manifests = []
    receipts = []
    errors = []
    for path in sorted(input_dir.glob("*_response.md")):
        manifest, manifest_errors = _read_manifest(str(path))
        if manifest_errors:
            errors.extend(f"{_relative_to_root(path)}: {error}" for error in manifest_errors)
            continue
        manifests.append(_relative_to_root(path))
        found = manifest.get("reading_receipts") if manifest else None
        if not isinstance(found, list):
            errors.append(f"{_relative_to_root(path)}: reading_receipts must be a list")
            continue
        receipts.extend(found)
    if errors:
        raise RuntimeError("; ".join(errors))
    output_file = _resolve_repo_path(output_file_arg)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "merged_from": manifests,
        "reading_receipts": _normalize_master_receipts(receipts),
    }
    output_file.write_text(
        "\n".join(
            [
                "# NRL Full-Corpus Proof Master Manifest v0.8",
                "",
                "## JSON Manifest",
                "```json",
                json.dumps(manifest, ensure_ascii=False, indent=2),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "input_dir": _relative_to_root(input_dir),
        "output_file": _relative_to_root(output_file),
        "source_manifest_count": len(manifests),
        "receipt_count": len(receipts),
    }


def promote_verified_proof() -> dict[str, Any]:
    proof_status = build_proof_status()
    readiness = proof_status["promotion_readiness"]
    if not readiness["promotion_allowed"]:
        return {
            "version": "0.9",
            "job_id": JOB_ID,
            "status": readiness["status"],
            "promotion_allowed": False,
            "manifest_written": False,
            "next_required_action": readiness["next_required_action"],
        }
    if not FULL_CORPUS_PROOF_MASTER.exists():
        return {
            "version": "0.9",
            "job_id": JOB_ID,
            "status": "blocked_missing_master_manifest",
            "promotion_allowed": False,
            "manifest_written": False,
            "next_required_action": "Rebuild full-corpus proof master manifest before promotion.",
        }
    manifest = {
        "version": "0.9",
        "asset_id": "full-corpus-proof-v08",
        "promotion_state": "promoted_research_asset",
        "source_proof_state": proof_status["latest_validation"]["status"],
        "proof_master_path": _relative_to_root(FULL_CORPUS_PROOF_MASTER),
        "proof_master_sha256": _sha256_file(FULL_CORPUS_PROOF_MASTER),
        "validation_path": _relative_to_root(VALIDATION_PATH),
        "validation_sha256": _sha256_file(VALIDATION_PATH),
        "owner_decision_id": readiness["owner_decision_id"],
        "verified_receipts": readiness["verified_receipts"],
        "required_receipts": readiness["required_receipts"],
        "content_generation_allowed": False,
        "forbidden_actions": readiness["forbidden_actions"],
        "created_at": now_iso(),
    }
    PROMOTION_MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_json(PROMOTION_MANIFEST_PATH, manifest)
    return {
        "version": "0.9",
        "job_id": JOB_ID,
        "status": "promoted_research_asset",
        "promotion_allowed": True,
        "manifest_written": True,
        "manifest_path": _relative_to_root(PROMOTION_MANIFEST_PATH),
        "owner_decision_id": readiness["owner_decision_id"],
    }


def _normalize_master_receipts(receipts: list[Any]) -> list[Any]:
    normalized_receipts = []
    for receipt_index, receipt in enumerate(receipts, start=1):
        if not isinstance(receipt, dict):
            normalized_receipts.append(receipt)
            continue
        normalized = dict(receipt)
        segments = normalized.get("segments")
        if isinstance(segments, list):
            normalized_segments = []
            for segment_index, segment in enumerate(segments, start=1):
                if not isinstance(segment, dict):
                    normalized_segments.append(segment)
                    continue
                normalized_segment = dict(segment)
                phase = str(normalized_segment.get("phase", "segment"))
                normalized_segment["chunk_id"] = f"receipt_{receipt_index:02d}_{phase}_{segment_index:02d}"
                normalized_segments.append(normalized_segment)
            normalized["segments"] = normalized_segments
        normalized_receipts.append(normalized)
    return normalized_receipts


def _validation_result(
    file_arg: str,
    status: str,
    errors: list[str],
    verified_receipts: int,
    required_receipts: int,
) -> dict[str, Any]:
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "file": file_arg,
        "status": status,
        "valid": status == "proof_verified",
        "errors": errors,
        "verified_receipts": verified_receipts,
        "required_receipts": required_receipts,
        "promotion_allowed": False,
        "validated_at": now_iso(),
    }


def _request_text(path: Path, inventory_item: dict[str, Any]) -> str:
    source_file = str(inventory_item["source_file"])
    return f"""# NRL Antigravity Per-Book Proof Request v0.8

## Role

You are Antigravity acting as long-text literary review agent for one bounded source file.

## Source File

- source_file: `{source_file}`
- size_bytes: {inventory_item["size_bytes"]}
- source_file_sha256: `{inventory_item["sha256"]}`

## Task

Read this one file from the shared local workspace and produce a structured literary mechanism review plus a machine-verifiable `reading_receipt`.

Do not quote raw prose. Do not generate novel prose. Do not create chapter plans, final character sheets, final technique trees, or Hermes instructions.

## Required Receipt

Return a fenced JSON block under `## JSON Manifest` containing:

```json
{{
  "job_id": "{JOB_ID}",
  "contract_version": "{VERSION}",
  "reading_receipts": [
    {{
      "book_title": "",
      "source_file": "{source_file}",
      "source_file_size_bytes": {inventory_item["size_bytes"]},
      "source_file_sha256": "{inventory_item["sha256"]}",
      "read_scope": "full_text_reviewed",
      "segments": [
        {{"chunk_id": "", "phase": "early", "start_byte": 0, "end_byte": 0, "chunk_sha256": ""}},
        {{"chunk_id": "", "phase": "middle", "start_byte": 0, "end_byte": 0, "chunk_sha256": ""}},
        {{"chunk_id": "", "phase": "late", "start_byte": 0, "end_byte": 0, "chunk_sha256": ""}},
        {{"chunk_id": "", "phase": "ending", "start_byte": 0, "end_byte": 0, "chunk_sha256": ""}}
      ]
    }}
  ],
  "mechanism_review": {{
    "single_book_dna": [],
    "long_form_mechanisms": [],
    "creation_asset_evidence": {{}},
    "originality_risks": []
  }}
}}
```

The chunk hashes must be SHA-256 over exact byte ranges from the local source file. Use short ranges that prove access to early, middle, late, and ending regions without copying text.
"""


def write_proof_packets(all_books: bool = False, book_title: str | None = None) -> dict[str, Any]:
    if not all_books and not book_title:
        raise RuntimeError("pass --all or --book-title")
    inventory = build_corpus_inventory(include_hashes=True)
    requests = []
    REQUEST_DIR.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(inventory["files"], start=1):
        name = str(item["file_name"])
        if book_title and book_title not in name:
            continue
        ascii_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(name).stem).strip("_")
        if ascii_stem:
            request_name = f"{index:02d}-{ascii_stem[:40]}"
        else:
            request_name = f"{index:02d}-{str(item['sha256'])[:12]}"
        request_path = REQUEST_DIR / f"{request_name}.md"
        source_path = runtime_path(str(item["source_file"]))
        request_path.write_text(_request_text(source_path, item), encoding="utf-8")
        requests.append(
            {
                "source_file": item["source_file"],
                "request_path": _relative_to_root(request_path),
                "expected_response_path": f"system/agent_ops/inbox/full_corpus_proof_v0.8/{request_path.stem}_response.md",
            }
        )
    if book_title and not requests:
        raise RuntimeError(f"no corpus file matched --book-title: {book_title}")
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "request_count": len(requests),
        "requests": requests,
    }
