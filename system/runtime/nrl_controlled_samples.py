from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from nrl_paths import ROOT
from nrl_production_runtime import analyze_prose_metrics
from nrl_projects import build_project_status, load_project


BLOCKING_METRIC_FLAGS = {
    "prompt_context_leak",
    "generation_meta_leak",
    "latin_token_leak",
    "termination_token_loop",
    "oversized_paragraph_loop",
    "duplicate_text_span",
    "tail_fragmentation_loop",
}


def split_sample_chapters(text: str) -> list[dict[str, Any]]:
    matches = list(re.finditer(r"(?m)^## 第(\d+)章\s+(.+?)\s*$", text))
    rows: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        rows.append(
            {
                "chapter": int(match.group(1)),
                "title": match.group(2).strip(),
                "prose": text[start:end].strip(),
            }
        )
    return rows


def validate_controlled_samples(project_id: str | None = None) -> dict[str, Any]:
    project = load_project(project_id)
    status = build_project_status(str(project["project_id"]))
    workspace = ROOT / str(project["workspace"])
    run_path = workspace / "production_runtime/plans/controlled_sample_run.v0.1.json"
    outline_path = workspace / "production_runtime/plans/volume1_outline.v1.json"
    run = json.loads(run_path.read_text(encoding="utf-8"))
    outline = json.loads(outline_path.read_text(encoding="utf-8"))
    outline_by_chapter = {row["chapter"]: row for row in outline["chapters"]}
    limits = run["quality_contract"]["chapter_character_range"]
    windows = []
    all_errors: list[str] = []

    if not status.get("sample_test_authorized"):
        all_errors.append("controlled sample owner authorization is not active")
    if run.get("continuous_prose_authorized") is not False:
        all_errors.append("continuous prose must remain unauthorized")
    if run.get("publish_authorized") is not False:
        all_errors.append("publishing must remain unauthorized")

    for window in run["windows"]:
        output_path = workspace / window["output_path"]
        errors: list[str] = []
        chapters: list[dict[str, Any]] = []
        if not output_path.is_file():
            errors.append("sample output missing")
        else:
            text = output_path.read_text(encoding="utf-8")
            if "novel_training_set/" in text:
                errors.append("raw corpus path leaked into sample")
            parsed = split_sample_chapters(text)
            if [row["chapter"] for row in parsed] != window["chapters"]:
                errors.append("chapter headings do not match authorized window")
            for row in parsed:
                expected = outline_by_chapter.get(row["chapter"], {})
                if row["title"] != expected.get("title"):
                    errors.append(f"chapter {row['chapter']} title mismatch")
                metrics = analyze_prose_metrics(row["prose"])
                count = int(metrics["chinese_character_count"])
                if count < int(limits[0]) or count > int(limits[1]):
                    errors.append(f"chapter {row['chapter']} length out of range: {count}")
                blocking_flags = sorted(set(metrics.get("flags", [])) & BLOCKING_METRIC_FLAGS)
                if blocking_flags:
                    errors.append(f"chapter {row['chapter']} blocking metrics: {blocking_flags}")
                chapters.append(
                    {
                        "chapter": row["chapter"],
                        "title": row["title"],
                        "metrics": metrics,
                        "sha256": hashlib.sha256(row["prose"].encode("utf-8")).hexdigest(),
                    }
                )
        windows.append(
            {
                "window_id": window["window_id"],
                "path": str(output_path.relative_to(ROOT)),
                "valid": not errors,
                "errors": errors,
                "chapters": chapters,
            }
        )
        all_errors.extend(f"{window['window_id']}: {error}" for error in errors)

    return {
        "version": "0.1",
        "project_id": project["project_id"],
        "mission_id": run["mission_id"],
        "valid": not all_errors,
        "continuous_prose_authorized": False,
        "publish_authorized": False,
        "windows": windows,
        "errors": all_errors,
    }
