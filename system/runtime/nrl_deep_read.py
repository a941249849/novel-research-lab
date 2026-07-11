from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from nrl_paths import ROOT, runtime_path


VERSION = "0.18"
JOB_ID = "job-v018-verifiable-deep-reading"
DEFAULT_TARGET_BYTES = 1_500_000
PLAN_PATH = runtime_path("system/research_assets/deep_read/v0.18/plan.json")
VALIDATION_PATH = runtime_path("system/research_assets/deep_read/v0.18/validation.json")
REQUEST_DIR = runtime_path("system/agent_ops/packets/deep_read_v0.18")
RESPONSE_DIR = runtime_path("system/agent_ops/inbox/deep_read_v0.18/chunks")
WORK_CHUNK_DIR = runtime_path(".nrl-work/deep_read_v0.18/chunks")
SYNTHESIS_REQUEST_DIR = runtime_path("system/agent_ops/packets/deep_read_v0.18/synthesis")
SYNTHESIS_RESPONSE_DIR = runtime_path("system/agent_ops/inbox/deep_read_v0.18/synthesis")
SYNTHESIS_VALIDATION_PATH = runtime_path("system/research_assets/deep_read/v0.18/synthesis_validation.json")
CROSS_REQUEST_PATH = runtime_path("system/agent_ops/packets/deep_read_v0.18/cross_book_distillation.md")
CROSS_RESPONSE_PATH = runtime_path("system/agent_ops/inbox/deep_read_v0.18/cross_book_distillation.json")
CROSS_VALIDATION_PATH = runtime_path("system/research_assets/deep_read/v0.18/cross_validation.json")
LEGACY_VALIDATION_PATH = runtime_path(
    "system/agent_ops/validation/full_corpus_proof_v0.8.json"
)
CHAPTER_PATTERN = re.compile(r"(?m)^\s*(第[^\r\n]{1,24}[章节回卷部集][^\r\n]{0,40})\s*$")
REQUIRED_ANALYSIS_LISTS = (
    "major_events",
    "character_state_transitions",
    "long_form_mechanisms",
    "continuity_observations",
    "style_observations",
    "originality_risks",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _corpus_files() -> list[Path]:
    corpus = runtime_path("novel_training_set")
    return sorted(path for path in corpus.glob("*.txt") if path.is_file()) if corpus.exists() else []


def _safe_boundary(data: bytes, proposed: int) -> int:
    if proposed >= len(data):
        return len(data)
    newline = data.find(b"\n", proposed, min(len(data), proposed + 65536))
    return newline + 1 if newline >= 0 else proposed


def _detect_encoding(data: bytes) -> str:
    try:
        data.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError:
        data.decode("gb18030")
        return "gb18030"


def _headings(data: bytes, encoding: str) -> list[str]:
    text = data.decode(encoding)
    headings = [match.group(1).strip() for match in CHAPTER_PATTERN.finditer(text)]
    if len(headings) <= 24:
        return headings
    indexes = sorted({round(index * (len(headings) - 1) / 23) for index in range(24)})
    return [headings[index] for index in indexes]


def _request_text(chunk: dict[str, Any]) -> str:
    binding_template = {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "chunk_id": chunk["chunk_id"],
        "source_file": chunk["source_file"],
        "source_file_sha256": chunk["source_file_sha256"],
        "start_byte": chunk["start_byte"],
        "end_byte": chunk["end_byte"],
        "chunk_sha256": chunk["chunk_sha256"],
        "source_encoding": chunk["source_encoding"],
        "bounded_chunk_utf8_sha256": chunk["bounded_chunk_utf8_sha256"],
        "analysis": {
            "chapter_span": [],
            "major_events": [],
            "character_state_transitions": [],
            "long_form_mechanisms": [],
            "continuity_observations": [],
            "style_observations": [],
            "creation_family_evidence": {},
            "originality_risks": [],
        },
    }
    return f"""# NRL Antigravity Deep-Read Chunk v0.18

Read the exact byte range below from the shared local source file. Analyze the
range itself; do not rely on existing summaries. Do not quote source prose.

- chunk_id: `{chunk['chunk_id']}`
- source_file: `{chunk['source_file']}`
- source_file_sha256: `{chunk['source_file_sha256']}`
- start_byte: {chunk['start_byte']}
- end_byte: {chunk['end_byte']}
- chunk_sha256: `{chunk['chunk_sha256']}`
- source_encoding: `{chunk['source_encoding']}`
- bounded_chunk_utf8_sha256: `{chunk['bounded_chunk_utf8_sha256']}`
- bounded_chunk_file: `{chunk['bounded_chunk_file']}`

The bounded chunk file contains exactly the bytes identified above. Read that
entire bounded file before responding. Do not inspect or summarize a different
range and do not use pre-existing book reports as a substitute.

Return one JSON object only with these binding fields and an `analysis` object.
The analysis must contain non-empty arrays named `major_events`,
`character_state_transitions`, `long_form_mechanisms`,
`continuity_observations`, `style_observations`, and `originality_risks`;
`chapter_span` as an array; and `creation_family_evidence` as a non-empty object.
Use chapter titles or abstract event labels as evidence anchors, never raw prose.
For million-byte chunks, provide at least 16 major events, 10 character-state
transitions, 8 long-form mechanisms, 8 continuity observations, 6 style
observations, and 4 originality risks. Cite at least 8 exact chapter headings
from the bounded UTF-8 file when that many headings exist.
The job_id is `{JOB_ID}` and contract_version is `{VERSION}`. Copy every
binding field exactly from this template and replace only the analysis values:

```json
{json.dumps(binding_template, ensure_ascii=False, indent=2)}
```
"""


def build_deep_read_plan(target_bytes: int = DEFAULT_TARGET_BYTES) -> dict[str, Any]:
    if target_bytes < 128:
        raise RuntimeError("target_bytes must be at least 128")
    books: list[dict[str, Any]] = []
    total_size = 0
    total_chunks = 0
    REQUEST_DIR.mkdir(parents=True, exist_ok=True)
    WORK_CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for book_index, path in enumerate(_corpus_files(), start=1):
        data = path.read_bytes()
        source_encoding = _detect_encoding(data)
        source_hash = _sha256(data)
        source_file = _relative(path)
        chunks: list[dict[str, Any]] = []
        start = 0
        ordinal = 1
        while start < len(data):
            end = _safe_boundary(data, min(len(data), start + target_bytes))
            if end <= start:
                end = len(data)
            chunk_data = data[start:end]
            chunk_text = chunk_data.decode(source_encoding)
            utf8_data = chunk_text.encode("utf-8")
            chunk_id = f"book-{book_index:02d}-{source_hash[:12]}-chunk-{ordinal:03d}"
            response_path = RESPONSE_DIR / f"{chunk_id}.json"
            request_path = REQUEST_DIR / f"{chunk_id}.md"
            bounded_chunk_path = WORK_CHUNK_DIR / f"{chunk_id}.txt"
            bounded_chunk_path.write_bytes(utf8_data)
            chunk = {
                "chunk_id": chunk_id,
                "book_index": book_index,
                "ordinal": ordinal,
                "source_file": source_file,
                "source_file_sha256": source_hash,
                "start_byte": start,
                "end_byte": end,
                "size_bytes": end - start,
                "chunk_sha256": _sha256(chunk_data),
                "source_encoding": source_encoding,
                "bounded_chunk_utf8_sha256": _sha256(utf8_data),
                "chapter_headings": _headings(chunk_data, source_encoding),
                "bounded_chunk_file": _relative(bounded_chunk_path),
                "request_path": _relative(request_path),
                "response_path": _relative(response_path),
            }
            request_path.write_text(_request_text(chunk), encoding="utf-8")
            chunks.append(chunk)
            start = end
            ordinal += 1
        total_size += len(data)
        total_chunks += len(chunks)
        books.append(
            {
                "book_index": book_index,
                "book_title": path.stem,
                "source_file": source_file,
                "source_file_sha256": source_hash,
                "source_encoding": source_encoding,
                "size_bytes": len(data),
                "chunk_count": len(chunks),
                "chunks": chunks,
            }
        )
    plan = {
        "version": VERSION,
        "job_id": JOB_ID,
        "status": "planned",
        "target_bytes": target_bytes,
        "book_count": len(books),
        "chunk_count": total_chunks,
        "total_size_bytes": total_size,
        "coverage_bytes": sum(chunk["size_bytes"] for book in books for chunk in book["chunks"]),
        "coverage_ratio": 1.0 if books else 0.0,
        "books": books,
        "created_at": _now_iso(),
    }
    _write_json(PLAN_PATH, plan)
    return plan


def _legacy_status() -> str:
    if not LEGACY_VALIDATION_PATH.exists():
        return "missing"
    try:
        legacy = _read_json(LEGACY_VALIDATION_PATH)
    except (json.JSONDecodeError, OSError):
        return "invalid"
    if legacy.get("status") == "proof_verified":
        return "access_sample_verified"
    return str(legacy.get("status", "unknown"))


def validate_plan_integrity(plan: dict[str, Any]) -> dict[str, Any]:
    errors = []
    current_sources = {_relative(path): path for path in _corpus_files()}
    planned_sources = {str(book["source_file"]) for book in plan.get("books", [])}
    if set(current_sources) != planned_sources:
        errors.append("corpus inventory mismatch")
    for book in plan.get("books", []):
        source = current_sources.get(str(book["source_file"]))
        if not source:
            errors.append(f"source is missing: {book.get('source_file')}")
            continue
        source_data = source.read_bytes()
        if _sha256(source_data) != book.get("source_file_sha256"):
            errors.append(f"source hash mismatch: {book.get('source_file')}")
            continue
        if source.stat().st_size != book.get("size_bytes"):
            errors.append(f"source size mismatch: {book.get('source_file')}")
        expected_start = 0
        for chunk in book.get("chunks", []):
            if chunk.get("start_byte") != expected_start:
                errors.append(f"chunk range gap or overlap: {chunk.get('chunk_id')}")
            expected_start = int(chunk.get("end_byte", 0))
            raw_slice = source_data[int(chunk["start_byte"]):int(chunk["end_byte"])]
            if _sha256(raw_slice) != chunk.get("chunk_sha256"):
                errors.append(f"raw chunk hash mismatch: {chunk.get('chunk_id')}")
            bounded = runtime_path(str(chunk.get("bounded_chunk_file", "")))
            if not bounded.is_file() or _sha256(bounded.read_bytes()) != chunk.get("bounded_chunk_utf8_sha256"):
                errors.append(f"bounded chunk hash mismatch: {chunk.get('chunk_id')}")
        if expected_start != book.get("size_bytes"):
            errors.append(f"chunk coverage mismatch: {book.get('source_file')}")
    return {"valid": not errors, "errors": errors}


def build_deep_read_status() -> dict[str, Any]:
    plan = _read_json(PLAN_PATH) if PLAN_PATH.exists() else None
    validation = _read_json(VALIDATION_PATH) if VALIDATION_PATH.exists() else None
    synthesis = _read_json(SYNTHESIS_VALIDATION_PATH) if SYNTHESIS_VALIDATION_PATH.exists() else None
    cross = _read_json(CROSS_VALIDATION_PATH) if CROSS_VALIDATION_PATH.exists() else None
    plan_integrity = validate_plan_integrity(plan) if plan else {"valid": False, "errors": ["plan missing"]}
    if cross and cross.get("valid") and plan_integrity["valid"]:
        status = "deep_read_verified"
    elif synthesis and synthesis.get("valid") and plan_integrity["valid"]:
        status = "book_synthesis_verified"
    else:
        status = str(validation.get("status")) if validation else ("planned" if plan else "missing")
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "status": status,
        "deep_read_verified": status == "deep_read_verified",
        "legacy_v08_effective_status": _legacy_status(),
        "plan_path": _relative(PLAN_PATH),
        "validation_path": _relative(VALIDATION_PATH),
        "book_count": int(plan.get("book_count", 0)) if plan else 0,
        "required_chunk_count": int(plan.get("chunk_count", 0)) if plan else 0,
        "validation": validation,
        "synthesis_validation": synthesis,
        "cross_validation": cross,
        "plan_integrity": plan_integrity,
        "next_action": (
            "Create a contiguous deep-read plan."
            if not plan
            else "Complete and validate all planned chunk analyses."
            if status in {"planned", "in_progress", "blocked"}
            else "Build and validate all per-book syntheses."
            if status == "chunk_coverage_verified"
            else "Build and validate cross-book distillation."
            if status == "book_synthesis_verified"
            else "Run project impact review before production promotion."
        ),
    }


def _find_chunk(plan: dict[str, Any], chunk_id: str) -> dict[str, Any] | None:
    for book in plan.get("books", []):
        for chunk in book.get("chunks", []):
            if chunk.get("chunk_id") == chunk_id:
                return chunk
    return None


def _load_response(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").strip()
    match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
    return json.loads(match.group(1) if match else text)


def validate_chunk_response(chunk_id: str) -> dict[str, Any]:
    if not PLAN_PATH.exists():
        return {"chunk_id": chunk_id, "valid": False, "errors": ["deep-read plan is missing"]}
    plan = _read_json(PLAN_PATH)
    chunk = _find_chunk(plan, chunk_id)
    if not chunk:
        return {"chunk_id": chunk_id, "valid": False, "errors": ["unknown chunk_id"]}
    path = runtime_path(str(chunk["response_path"]))
    if not path.exists():
        return {"chunk_id": chunk_id, "valid": False, "errors": ["response file is missing"]}
    try:
        response = _load_response(path)
    except (json.JSONDecodeError, OSError) as error:
        return {"chunk_id": chunk_id, "valid": False, "errors": [f"invalid response JSON: {error}"]}
    errors: list[str] = []
    expected_fields = (
        "chunk_id",
        "source_file",
        "source_file_sha256",
        "start_byte",
        "end_byte",
        "chunk_sha256",
        "source_encoding",
        "bounded_chunk_utf8_sha256",
    )
    for field in expected_fields:
        if response.get(field) != chunk.get(field):
            errors.append(f"{field} mismatch")
    if response.get("job_id") != JOB_ID:
        errors.append("job_id mismatch")
    if response.get("contract_version") != VERSION:
        errors.append("contract_version mismatch")
    analysis = response.get("analysis")
    if not isinstance(analysis, dict):
        errors.append("analysis must be an object")
    else:
        if not isinstance(analysis.get("chapter_span"), list):
            errors.append("analysis.chapter_span must be an array")
        for field in REQUIRED_ANALYSIS_LISTS:
            value = analysis.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"analysis.{field} must be a non-empty array")
        if int(chunk.get("size_bytes", 0)) >= 1_000_000:
            minimums = {
                "major_events": 16,
                "character_state_transitions": 10,
                "long_form_mechanisms": 8,
                "continuity_observations": 8,
                "style_observations": 6,
                "originality_risks": 4,
            }
            for field, minimum in minimums.items():
                if isinstance(analysis.get(field), list) and len(analysis[field]) < minimum:
                    errors.append(f"analysis.{field} requires at least {minimum} items")
        family_evidence = analysis.get("creation_family_evidence")
        if not isinstance(family_evidence, dict) or not family_evidence:
            errors.append("analysis.creation_family_evidence must be a non-empty object")
        known_headings = [str(item) for item in chunk.get("chapter_headings", [])]
        if known_headings:
            encoded_analysis = json.dumps(analysis, ensure_ascii=False)
            heading_matches = sum(1 for heading in known_headings if heading in encoded_analysis)
            required_matches = min(8, len(known_headings))
            if heading_matches < required_matches:
                errors.append(
                    f"analysis must cite at least {required_matches} detected chapter headings"
                )
        else:
            heading_matches = 0
    return {
        "chunk_id": chunk_id,
        "valid": not errors,
        "errors": errors,
        "response_path": chunk["response_path"],
        "size_bytes": chunk["size_bytes"],
        "evidence_heading_matches": heading_matches if isinstance(analysis, dict) else 0,
    }


def validate_all_chunks() -> dict[str, Any]:
    if not PLAN_PATH.exists():
        result = {
            "version": VERSION,
            "job_id": JOB_ID,
            "status": "missing",
            "deep_read_verified": False,
            "errors": ["deep-read plan is missing"],
            "validated_chunk_count": 0,
            "required_chunk_count": 0,
            "validated_byte_ratio": 0.0,
        }
        _write_json(VALIDATION_PATH, result)
        return result
    plan = _read_json(PLAN_PATH)
    plan_integrity = validate_plan_integrity(plan)
    chunks = [chunk for book in plan["books"] for chunk in book["chunks"]]
    validations = [validate_chunk_response(str(chunk["chunk_id"])) for chunk in chunks]
    valid_ids = {item["chunk_id"] for item in validations if item["valid"]}
    validated_bytes = sum(chunk["size_bytes"] for chunk in chunks if chunk["chunk_id"] in valid_ids)
    required_bytes = int(plan["total_size_bytes"])
    valid_count = len(valid_ids)
    all_valid = bool(chunks) and valid_count == len(chunks) and plan_integrity["valid"]
    result = {
        "version": VERSION,
        "job_id": JOB_ID,
        "status": "chunk_coverage_verified" if all_valid else "in_progress",
        "deep_read_verified": False,
        "book_count": int(plan["book_count"]),
        "validated_chunk_count": valid_count,
        "required_chunk_count": len(chunks),
        "validated_bytes": validated_bytes,
        "required_bytes": required_bytes,
        "validated_byte_ratio": round(validated_bytes / required_bytes, 6) if required_bytes else 0.0,
        "invalid_chunks": [item for item in validations if not item["valid"]],
        "plan_integrity": plan_integrity,
        "validated_at": _now_iso(),
    }
    _write_json(VALIDATION_PATH, result)
    return result


def _dispatch_one(chunk: dict[str, Any], model: str, print_timeout: str) -> dict[str, Any]:
    binary = shutil.which("agy") or str(Path.home() / ".local/bin/agy")
    if not Path(binary).exists():
        return {"chunk_id": chunk["chunk_id"], "valid": False, "errors": ["agy binary is missing"]}
    request_path = runtime_path(str(chunk["request_path"]))
    response_path = runtime_path(str(chunk["response_path"]))
    response_path.parent.mkdir(parents=True, exist_ok=True)
    prompt = request_path.read_text(encoding="utf-8")
    result = subprocess.run(
        [
            binary,
            "--model",
            model,
            "--mode",
            "plan",
            "--sandbox",
            "--print-timeout",
            print_timeout,
            "-p",
            prompt,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout.strip():
        response_path.write_text(result.stdout, encoding="utf-8")
    else:
        response_path.unlink(missing_ok=True)
    validation = validate_chunk_response(str(chunk["chunk_id"]))
    validation["returncode"] = result.returncode
    if result.returncode != 0:
        validation["errors"] = list(validation["errors"]) + [
            (result.stderr.strip() or f"agy exited with {result.returncode}")
        ]
        validation["valid"] = False
    return validation


def dispatch_pending_chunks(
    *,
    limit: int = 0,
    workers: int = 2,
    model: str = "Gemini 3.5 Flash (High)",
    print_timeout: str = "10m0s",
) -> dict[str, Any]:
    if not PLAN_PATH.exists():
        raise RuntimeError("deep-read plan is missing")
    if workers < 1 or workers > 8:
        raise RuntimeError("workers must be between 1 and 8")
    plan = _read_json(PLAN_PATH)
    chunks = [chunk for book in plan["books"] for chunk in book["chunks"]]
    pending = [chunk for chunk in chunks if not validate_chunk_response(chunk["chunk_id"])["valid"]]
    if limit > 0:
        pending = pending[:limit]
    results: list[dict[str, Any]] = []
    quota_blocked = False
    if workers == 1:
        for chunk in pending:
            try:
                item = _dispatch_one(chunk, model, print_timeout)
            except Exception as error:  # keep the batch resumable
                item = {"chunk_id": chunk["chunk_id"], "valid": False, "errors": [str(error)]}
            results.append(item)
            error_text = " ".join(str(error) for error in item.get("errors", []))
            if "quota reached" in error_text.casefold():
                quota_blocked = True
                break
    else:
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(_dispatch_one, chunk, model, print_timeout): chunk
                for chunk in pending
            }
            for future in as_completed(futures):
                chunk = futures[future]
                try:
                    results.append(future.result())
                except Exception as error:  # keep the batch resumable
                    results.append(
                        {"chunk_id": chunk["chunk_id"], "valid": False, "errors": [str(error)]}
                    )
        quota_blocked = any(
            "quota reached" in " ".join(str(error) for error in item.get("errors", [])).casefold()
            for item in results
        )
    coverage = validate_all_chunks()
    return {
        "version": VERSION,
        "job_id": JOB_ID,
        "model": model,
        "requested": len(pending),
        "dispatched": len(results),
        "succeeded": sum(1 for item in results if item["valid"]),
        "failed": [item for item in results if not item["valid"]],
        "quota_blocked": quota_blocked,
        "coverage": coverage,
    }


def _book_id(book: dict[str, Any]) -> str:
    return f"book-{int(book['book_index']):02d}-{str(book['source_file_sha256'])[:12]}"


def build_book_synthesis_packets() -> dict[str, Any]:
    coverage = validate_all_chunks()
    if coverage["status"] != "chunk_coverage_verified":
        raise RuntimeError("all chunk analyses must validate before book synthesis")
    plan = _read_json(PLAN_PATH)
    SYNTHESIS_REQUEST_DIR.mkdir(parents=True, exist_ok=True)
    requests = []
    for book in plan["books"]:
        book_id = _book_id(book)
        chunk_ids = [chunk["chunk_id"] for chunk in book["chunks"]]
        response_paths = [chunk["response_path"] for chunk in book["chunks"]]
        chunk_hashes = [
            {
                "chunk_id": chunk["chunk_id"],
                "response_sha256": _sha256(runtime_path(chunk["response_path"]).read_bytes()),
            }
            for chunk in book["chunks"]
        ]
        output_path = SYNTHESIS_RESPONSE_DIR / f"{book_id}.json"
        template = {
            "job_id": JOB_ID,
            "contract_version": VERSION,
            "book_id": book_id,
            "book_title": book["book_title"],
            "covered_chunk_ids": chunk_ids,
            "covered_chunk_hashes": chunk_hashes,
            "synthesis": {
                "narrative_spine": [],
                "character_arcs": [],
                "mechanism_evolution": [],
                "world_expansion": [],
                "long_term_reader_hooks": [],
                "style_and_life_force": [],
                "continuity_failures": [],
                "creation_family_evidence": {},
                "originality_red_lines": [],
            },
        }
        request_path = SYNTHESIS_REQUEST_DIR / f"{book_id}.md"
        request_path.write_text(
            "\n".join(
                [
                    "# NRL Antigravity Per-Book Synthesis v0.18",
                    "",
                    "Read every validated chunk-analysis file listed below and synthesize the complete book trajectory.",
                    "Do not use pre-existing short reports and do not quote source prose.",
                    "",
                    *[f"- `{path}`" for path in response_paths],
                    "",
                    "Return one JSON object only. Copy binding fields and covered_chunk_ids exactly.",
                    "All synthesis arrays and all nine creation-family keys must be non-empty.",
                    "",
                    "```json",
                    json.dumps(template, ensure_ascii=False, indent=2),
                    "```",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        requests.append(
            {
                "book_id": book_id,
                "request_path": _relative(request_path),
                "response_path": _relative(output_path),
                "covered_chunk_ids": chunk_ids,
                "covered_chunk_hashes": chunk_hashes,
            }
        )
    return {"version": VERSION, "job_id": JOB_ID, "request_count": len(requests), "requests": requests}


def _validate_book_synthesis(request: dict[str, Any]) -> dict[str, Any]:
    path = runtime_path(request["response_path"])
    if not path.exists():
        return {"book_id": request["book_id"], "valid": False, "errors": ["response file is missing"]}
    try:
        data = _load_response(path)
    except (json.JSONDecodeError, OSError) as error:
        return {"book_id": request["book_id"], "valid": False, "errors": [f"invalid response JSON: {error}"]}
    errors = []
    if data.get("job_id") != JOB_ID:
        errors.append("job_id mismatch")
    if data.get("contract_version") != VERSION:
        errors.append("contract_version mismatch")
    if data.get("book_id") != request["book_id"]:
        errors.append("book_id mismatch")
    if data.get("covered_chunk_ids") != request["covered_chunk_ids"]:
        errors.append("covered_chunk_ids mismatch")
    if data.get("covered_chunk_hashes") != request["covered_chunk_hashes"]:
        errors.append("covered_chunk_hashes mismatch")
    synthesis = data.get("synthesis")
    required = (
        "narrative_spine", "character_arcs", "mechanism_evolution", "world_expansion",
        "long_term_reader_hooks", "style_and_life_force", "continuity_failures",
        "originality_red_lines",
    )
    if not isinstance(synthesis, dict):
        errors.append("synthesis must be an object")
    else:
        for field in required:
            if not isinstance(synthesis.get(field), list) or not synthesis[field]:
                errors.append(f"synthesis.{field} must be a non-empty array")
        families = synthesis.get("creation_family_evidence")
        expected_families = {
            "characters", "npcs", "factions", "artifacts", "techniques", "naming",
            "emotional_bonds", "foreshadowing", "state_ledger",
        }
        if not isinstance(families, dict) or set(families) != expected_families:
            errors.append("synthesis.creation_family_evidence must contain all nine families")
        elif any(not value for value in families.values()):
            errors.append("all creation-family evidence must be non-empty")
    return {"book_id": request["book_id"], "valid": not errors, "errors": errors, "response_path": request["response_path"]}


def validate_book_syntheses() -> dict[str, Any]:
    packet = build_book_synthesis_packets()
    results = [_validate_book_synthesis(request) for request in packet["requests"]]
    result = {
        "version": VERSION,
        "job_id": JOB_ID,
        "valid": bool(results) and all(item["valid"] for item in results),
        "validated_book_count": sum(1 for item in results if item["valid"]),
        "required_book_count": len(results),
        "invalid_books": [item for item in results if not item["valid"]],
        "validated_at": _now_iso(),
    }
    _write_json(SYNTHESIS_VALIDATION_PATH, result)
    return result


def dispatch_book_syntheses(
    *, workers: int = 2, model: str = "Gemini 3.5 Flash (High)", print_timeout: str = "10m0s"
) -> dict[str, Any]:
    packet = build_book_synthesis_packets()
    pending = [item for item in packet["requests"] if not _validate_book_synthesis(item)["valid"]]
    chunks = [
        {
            "chunk_id": item["book_id"],
            "request_path": item["request_path"],
            "response_path": item["response_path"],
        }
        for item in pending
    ]
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_dispatch_generic, item, model, print_timeout): item for item in chunks}
        for future in as_completed(futures):
            results.append(future.result())
    validation = validate_book_syntheses()
    return {"dispatched": len(pending), "results": results, "validation": validation}


def _dispatch_generic(item: dict[str, Any], model: str, print_timeout: str) -> dict[str, Any]:
    binary = shutil.which("agy") or str(Path.home() / ".local/bin/agy")
    request_path = runtime_path(item["request_path"])
    response_path = runtime_path(item["response_path"])
    response_path.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [binary, "--model", model, "--mode", "plan", "--sandbox", "--print-timeout", print_timeout, "-p", request_path.read_text(encoding="utf-8")],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.stdout.strip():
        response_path.write_text(result.stdout, encoding="utf-8")
    else:
        response_path.unlink(missing_ok=True)
    return {"id": item["chunk_id"], "returncode": result.returncode, "stderr": result.stderr.strip()}


def build_cross_book_packet() -> dict[str, Any]:
    synthesis = validate_book_syntheses()
    if not synthesis["valid"]:
        raise RuntimeError("all book syntheses must validate before cross-book distillation")
    packet = build_book_synthesis_packets()
    book_ids = [item["book_id"] for item in packet["requests"]]
    book_synthesis_hashes = [
        {
            "book_id": item["book_id"],
            "response_sha256": _sha256(runtime_path(item["response_path"]).read_bytes()),
        }
        for item in packet["requests"]
    ]
    all_chunk_ids = [chunk_id for item in packet["requests"] for chunk_id in item["covered_chunk_ids"]]
    template = {
        "job_id": JOB_ID,
        "contract_version": VERSION,
        "covered_book_ids": book_ids,
        "book_synthesis_hashes": book_synthesis_hashes,
        "cross_book_mechanisms": [
            {
                "mechanism_id": "CB18-M01",
                "name": "",
                "source_book_ids": [],
                "source_chunk_ids": [],
                "abstract_rule": "",
                "variation_pattern": "",
                "failure_modes": [],
                "originality_boundary": "",
                "nrl_relevance": [],
            }
        ],
        "corpus_level_findings": {
            "long_form_vitality": [],
            "anti_ai_prose_lessons": [],
            "continuity_system_lessons": [],
            "creation_family_findings": {},
        },
    }
    CROSS_REQUEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    CROSS_REQUEST_PATH.write_text(
        "\n".join(
            [
                "# NRL Antigravity Cross-Book Distillation v0.18", "",
                "Read all 18 validated per-book synthesis files below.",
                "Derive at least 12 abstract mechanisms, each supported by at least two books and valid chunk IDs.",
                "Do not copy names, prose, scenes, proprietary systems, or author-specific style.", "",
                *[f"- `{item['response_path']}`" for item in packet["requests"]], "",
                f"Valid chunk IDs are: {json.dumps(all_chunk_ids, ensure_ascii=False)}", "",
                "Return one JSON object only using this binding template:", "```json",
                json.dumps(template, ensure_ascii=False, indent=2), "```", "",
            ]
        ), encoding="utf-8",
    )
    return {
        "request_path": _relative(CROSS_REQUEST_PATH),
        "response_path": _relative(CROSS_RESPONSE_PATH),
        "book_ids": book_ids,
        "book_synthesis_hashes": book_synthesis_hashes,
        "chunk_ids": all_chunk_ids,
    }


def validate_cross_book_distillation() -> dict[str, Any]:
    packet = build_cross_book_packet()
    errors = []
    if not CROSS_RESPONSE_PATH.exists():
        errors.append("cross-book response is missing")
        data = {}
    else:
        try:
            data = _load_response(CROSS_RESPONSE_PATH)
        except (json.JSONDecodeError, OSError) as error:
            data = {}
            errors.append(f"invalid response JSON: {error}")
    if data.get("job_id") != JOB_ID:
        errors.append("job_id mismatch")
    if data.get("contract_version") != VERSION:
        errors.append("contract_version mismatch")
    if data.get("covered_book_ids") != packet["book_ids"]:
        errors.append("covered_book_ids mismatch")
    if data.get("book_synthesis_hashes") != packet["book_synthesis_hashes"]:
        errors.append("book_synthesis_hashes mismatch")
    mechanisms = data.get("cross_book_mechanisms")
    if not isinstance(mechanisms, list) or len(mechanisms) < 12:
        errors.append("at least 12 cross-book mechanisms are required")
    else:
        valid_books = set(packet["book_ids"])
        valid_chunks = set(packet["chunk_ids"])
        for index, mechanism in enumerate(mechanisms):
            if len(set(mechanism.get("source_book_ids", []))) < 2 or not set(mechanism.get("source_book_ids", [])) <= valid_books:
                errors.append(f"mechanism[{index}] has invalid source_book_ids")
            if not mechanism.get("source_chunk_ids") or not set(mechanism["source_chunk_ids"]) <= valid_chunks:
                errors.append(f"mechanism[{index}] has invalid source_chunk_ids")
            for field in ("name", "abstract_rule", "variation_pattern", "originality_boundary"):
                if not mechanism.get(field):
                    errors.append(f"mechanism[{index}].{field} is required")
    findings = data.get("corpus_level_findings")
    if not isinstance(findings, dict) or any(not findings.get(key) for key in ("long_form_vitality", "anti_ai_prose_lessons", "continuity_system_lessons", "creation_family_findings")):
        errors.append("corpus_level_findings is incomplete")
    result = {"version": VERSION, "job_id": JOB_ID, "valid": not errors, "errors": errors, "mechanism_count": len(mechanisms) if isinstance(mechanisms, list) else 0, "validated_at": _now_iso()}
    _write_json(CROSS_VALIDATION_PATH, result)
    return result


def dispatch_cross_book_distillation(model: str = "Gemini 3.5 Flash (High)", print_timeout: str = "15m0s") -> dict[str, Any]:
    packet = build_cross_book_packet()
    execution = _dispatch_generic({"chunk_id": "cross-book", "request_path": packet["request_path"], "response_path": packet["response_path"]}, model, print_timeout)
    return {"execution": execution, "validation": validate_cross_book_distillation()}
