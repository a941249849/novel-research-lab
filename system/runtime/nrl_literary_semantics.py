from __future__ import annotations

"""Loss-resistant literary distillation and project semantic-contract validation."""

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from nrl_paths import ROOT
from nrl_projects import load_project


VERSION = "0.29"
V018_SYNTHESIS_ROOT = ROOT / "system/agent_ops/inbox/deep_read_v0.18/synthesis"
V018_CROSS_PATH = ROOT / "system/agent_ops/inbox/deep_read_v0.18/cross_book_distillation.json"
SEMANTIC_ROOT = ROOT / "system/research_assets/deep_read/v0.29"
CONTRACT_PATH = SEMANTIC_ROOT / "literary_semantic_contract.v1.json"
PROFILE_PATH = SEMANTIC_ROOT / "signature_profiles.v1.json"
LIBRARY_PATH = SEMANTIC_ROOT / "loss_resistant_mechanism_library.v1.json"
VALIDATION_PATH = SEMANTIC_ROOT / "validation.v1.json"

DIMENSIONS = (
    "narrative_spine",
    "character_highlight_architecture",
    "progression_and_thresholds",
    "world_map_and_scale",
    "embedded_history_and_lore",
    "faction_and_resource_game",
    "relationship_and_emotional_cost",
    "foreshadowing_and_payoff",
    "climax_convergence",
    "reader_feedback_rhythm",
    "style_and_life_force",
    "failure_modes_and_negative_lessons",
)

DIMENSION_SOURCES: dict[str, tuple[str, ...]] = {
    "narrative_spine": ("narrative_spine",),
    "character_highlight_architecture": ("character_arcs",),
    "progression_and_thresholds": ("mechanism_evolution",),
    "world_map_and_scale": ("world_expansion",),
    "embedded_history_and_lore": (
        "style_and_life_force",
        "world_expansion",
        "long_term_reader_hooks",
    ),
    "faction_and_resource_game": ("factions", "artifacts", "state_ledger"),
    "relationship_and_emotional_cost": ("emotional_bonds", "character_arcs"),
    "foreshadowing_and_payoff": ("foreshadowing", "long_term_reader_hooks"),
    "climax_convergence": ("narrative_spine", "world_expansion"),
    "reader_feedback_rhythm": ("long_term_reader_hooks", "style_and_life_force"),
    "style_and_life_force": ("style_and_life_force",),
    "failure_modes_and_negative_lessons": ("continuity_failures", "originality_red_lines"),
}

HISTORY_MARKERS = (
    "历史",
    "神话",
    "寓言",
    "传说",
    "史诗",
    "纪元",
    "古代",
    "前代",
    "尊者",
    "人祖传",
    "遗产",
    "遗迹",
    "真传",
)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def _normalize_book_title(value: str) -> str:
    match = re.search(r"《([^》]+)》", value)
    if match:
        return match.group(1).strip()
    return value.split("（", 1)[0].strip()


def _section_values(synthesis: dict[str, Any], section: str) -> list[str]:
    if section in synthesis:
        value = synthesis.get(section)
    else:
        value = synthesis.get("creation_family_evidence", {}).get(section)
    return [str(item).strip() for item in value or [] if str(item).strip()]


def _dimension_findings(synthesis: dict[str, Any], dimension: str) -> tuple[str, list[str]]:
    sections = DIMENSION_SOURCES[dimension]
    values: list[str] = []
    for section in sections:
        values.extend(_section_values(synthesis, section))
    if dimension == "embedded_history_and_lore":
        explicit = [item for item in values if any(marker in item for marker in HISTORY_MARKERS)]
        if explicit:
            return "explicit", explicit[:4]
        fallback = (
            _section_values(synthesis, "world_expansion")
            + _section_values(synthesis, "long_term_reader_hooks")
        )
        return (
            "not_dominant",
            [
                "本书没有被单书综合识别出独立的历史/神话叙事载体；必须保留这一缺口，不能由通用世界观条目冒充。",
                *(fallback[:1] or ["现有综合未提供可替代的历史载体证据。"]),
            ],
        )
    if dimension == "climax_convergence":
        narrative = _section_values(synthesis, "narrative_spine")
        world = _section_values(synthesis, "world_expansion")
        values = (narrative[-2:] if narrative else []) + (world[-1:] if world else [])
    if not values:
        return "not_dominant", [f"现有单书综合未显式覆盖 {dimension}，保留为语义缺口。"]
    return "explicit", values[:4]


def _evidence_claims(synthesis: dict[str, Any], dimension: str) -> list[str]:
    tokens = {
        "narrative_spine": ("narrative_spine",),
        "character_highlight_architecture": ("character_arcs", "characters", "npcs"),
        "progression_and_thresholds": ("mechanism_evolution", "techniques"),
        "world_map_and_scale": ("world_expansion",),
        "embedded_history_and_lore": ("style_and_life_force", "foreshadowing"),
        "faction_and_resource_game": ("factions", "artifacts", "state_ledger"),
        "relationship_and_emotional_cost": ("emotional_bonds", "character_arcs"),
        "foreshadowing_and_payoff": ("foreshadowing", "long_term_reader_hooks"),
        "climax_convergence": ("narrative_spine", "style_and_life_force"),
        "reader_feedback_rhythm": ("style_and_life_force", "long_term_reader_hooks"),
        "style_and_life_force": ("style_and_life_force",),
        "failure_modes_and_negative_lessons": ("continuity_failures", "originality_red_lines"),
    }[dimension]
    claims = []
    for evidence in synthesis.get("evidence_map", []):
        claim = str(evidence.get("claim", ""))
        if any(token in claim for token in tokens):
            claims.append(claim)
    return claims[:4]


def _build_profile(path: Path) -> dict[str, Any]:
    payload = _read_json(path)
    synthesis = payload["synthesis"]
    dimensions = {}
    for dimension in DIMENSIONS:
        status, findings = _dimension_findings(synthesis, dimension)
        dimensions[dimension] = {
            "status": status,
            "source_sections": list(DIMENSION_SOURCES[dimension]),
            "findings": findings,
            "evidence_claims": _evidence_claims(synthesis, dimension),
            "retention": "protected_signature_lane",
        }
    return {
        "profile_id": f"signature-{payload['book_id']}",
        "book_id": payload["book_id"],
        "book_title": _normalize_book_title(str(payload["book_title"])),
        "synthesis_path": _relative(path),
        "synthesis_sha256": _sha256(path),
        "dimensions": dimensions,
        "originality_red_lines": synthesis["originality_red_lines"],
        "semantic_gaps": [
            dimension
            for dimension, item in dimensions.items()
            if item["status"] != "explicit"
        ],
    }


def build_literary_semantic_assets() -> dict[str, Any]:
    synthesis_paths = sorted(V018_SYNTHESIS_ROOT.glob("book-*.json"))
    if len(synthesis_paths) != 18:
        raise RuntimeError(f"expected 18 verified book syntheses, found {len(synthesis_paths)}")
    profiles = [_build_profile(path) for path in synthesis_paths]
    contract = {
        "version": VERSION,
        "contract_id": "literary-semantic-integrity-v1",
        "dimensions": list(DIMENSIONS),
        "allowed_dimension_status": ["explicit", "implicit", "not_dominant"],
        "retention_lanes": {
            "cross_book_common": "Mechanisms supported by multiple books may be abstracted.",
            "protected_signature_lane": "Single-book signatures remain queryable even when no peer mechanism exists.",
        },
        "hard_gates": {
            "all_verified_books_profiled": True,
            "all_dimensions_declared": True,
            "synthesis_hashes_current": True,
            "not_dominant_requires_explicit_gap": True,
            "project_application_required": True,
        },
    }
    profile_payload = {
        "version": VERSION,
        "source_contract": _relative(CONTRACT_PATH),
        "profile_count": len(profiles),
        "profiles": profiles,
    }
    _write_json(CONTRACT_PATH, contract)
    _write_json(PROFILE_PATH, profile_payload)
    cross = _read_json(V018_CROSS_PATH)
    library = {
        "version": VERSION,
        "source_cross_book_path": _relative(V018_CROSS_PATH),
        "source_cross_book_sha256": _sha256(V018_CROSS_PATH),
        "source_signature_profiles_path": _relative(PROFILE_PATH),
        "source_signature_profiles_sha256": _sha256(PROFILE_PATH),
        "cross_book_mechanism_count": len(cross.get("cross_book_mechanisms", [])),
        "cross_book_mechanism_ids": [
            item.get("mechanism_id") for item in cross.get("cross_book_mechanisms", [])
        ],
        "protected_signature_profiles": [
            {
                "profile_id": item["profile_id"],
                "book_id": item["book_id"],
                "book_title": item["book_title"],
                "dimensions": {
                    key: value["status"] for key, value in item["dimensions"].items()
                },
            }
            for item in profiles
        ],
        "loss_prevention_rules": [
            "A mechanism does not need a second source book to remain queryable.",
            "Cross-book abstraction cannot replace a protected signature profile.",
            "Project reconciliation must record adopt, transform, defer, or reject decisions.",
            "Originality boundaries remain attached to every source profile.",
            "Semantic gaps are preserved as gaps instead of being filled by generic language.",
        ],
    }
    _write_json(LIBRARY_PATH, library)
    result = validate_literary_semantic_assets()
    _write_json(VALIDATION_PATH, result)
    return result


def validate_literary_semantic_assets(
    *, profile_payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    if not CONTRACT_PATH.is_file() or not PROFILE_PATH.is_file() or not LIBRARY_PATH.is_file():
        return {
            "version": VERSION,
            "valid": False,
            "errors": ["literary semantic assets are missing"],
            "profile_count": 0,
        }
    contract = _read_json(CONTRACT_PATH)
    profiles_payload = profile_payload or _read_json(PROFILE_PATH)
    library = _read_json(LIBRARY_PATH)
    if contract.get("dimensions") != list(DIMENSIONS):
        errors.append("semantic dimension contract drift")
    profiles = profiles_payload.get("profiles")
    synthesis_paths = sorted(V018_SYNTHESIS_ROOT.glob("book-*.json"))
    expected = {
        _read_json(path)["book_id"]: (
            path,
            _normalize_book_title(str(_read_json(path)["book_title"])),
        )
        for path in synthesis_paths
    }
    if not isinstance(profiles, list) or len(profiles) != len(expected):
        errors.append("signature profiles must cover all verified books")
        profiles = profiles if isinstance(profiles, list) else []
    seen: set[str] = set()
    for profile in profiles:
        book_id = str(profile.get("book_id", ""))
        if book_id in seen:
            errors.append(f"duplicate signature profile: {book_id}")
        seen.add(book_id)
        if book_id not in expected:
            errors.append(f"unknown signature profile: {book_id}")
            continue
        path, title = expected[book_id]
        if profile != _build_profile(path):
            errors.append(f"signature profile content drift: {book_id}")
        if profile.get("book_title") != title:
            errors.append(f"book title mismatch: {book_id}")
        if profile.get("synthesis_path") != _relative(path):
            errors.append(f"synthesis path mismatch: {book_id}")
        if profile.get("synthesis_sha256") != _sha256(path):
            errors.append(f"stale synthesis hash: {book_id}")
        dimensions = profile.get("dimensions")
        if not isinstance(dimensions, dict) or set(dimensions) != set(DIMENSIONS):
            errors.append(f"dimension coverage mismatch: {book_id}")
            continue
        for dimension, item in dimensions.items():
            if item.get("status") not in {"explicit", "implicit", "not_dominant"}:
                errors.append(f"invalid dimension status: {book_id}:{dimension}")
            if not item.get("findings"):
                errors.append(f"empty dimension findings: {book_id}:{dimension}")
            if item.get("retention") != "protected_signature_lane":
                errors.append(f"signature retention missing: {book_id}:{dimension}")
        if not profile.get("originality_red_lines"):
            errors.append(f"originality red lines missing: {book_id}")
    if set(expected) != seen:
        errors.append("verified book/profile identity set mismatch")
    for dimension in DIMENSIONS:
        fingerprints = [
            hashlib.sha256(
                json.dumps(
                    profile["dimensions"][dimension]["findings"],
                    ensure_ascii=False,
                    sort_keys=True,
                ).encode("utf-8")
            ).hexdigest()
            for profile in profiles
            if dimension in profile.get("dimensions", {})
        ]
        if len(fingerprints) != len(set(fingerprints)):
            errors.append(f"collapsed signature findings across books: {dimension}")
    if library.get("source_cross_book_sha256") != _sha256(V018_CROSS_PATH):
        errors.append("cross-book source hash drift")
    if profile_payload is None and library.get("source_signature_profiles_sha256") != _sha256(PROFILE_PATH):
        errors.append("signature profile library hash drift")
    protected_ids = {
        item.get("book_id") for item in library.get("protected_signature_profiles", [])
    }
    if protected_ids != set(expected):
        errors.append("protected signature lane does not cover every book")
    result = {
        "version": VERSION,
        "valid": not errors,
        "errors": errors,
        "profile_count": len(profiles),
        "dimension_count": len(DIMENSIONS),
        "cross_book_mechanism_count": library.get("cross_book_mechanism_count", 0),
        "protected_signature_count": len(protected_ids),
    }
    return result


def _project_semantic_paths(project_id: str) -> dict[str, Path]:
    project = load_project(project_id)
    workspace = ROOT / str(project["workspace"])
    return {
        "highlight": workspace / "design/character_highlight_matrix.v1.json",
        "atlas": workspace / "design/world_progression_atlas.v1.json",
        "history": workspace / "design/embedded_history_engine.v1.json",
        "volume1_beats": workspace / "production_runtime/plans/volume1_semantic_beat_contract.v1.json",
        "application": workspace / "validation/literary_semantic_application.v1.json",
    }


def validate_project_semantic_contracts(
    project_id: str, *, application_payload: dict[str, Any] | None = None
) -> dict[str, Any]:
    errors: list[str] = []
    research_validation = validate_literary_semantic_assets()
    if not research_validation.get("valid"):
        errors.extend(
            f"research semantic integrity: {item}"
            for item in research_validation.get("errors", [])
        )
    paths = _project_semantic_paths(project_id)
    for label, path in paths.items():
        if not path.is_file():
            errors.append(f"missing project semantic contract: {label}")
    if errors:
        return {"version": VERSION, "project_id": project_id, "valid": False, "errors": errors}
    highlight = _read_json(paths["highlight"])
    atlas = _read_json(paths["atlas"])
    history = _read_json(paths["history"])
    volume1_beats = _read_json(paths["volume1_beats"])
    application = application_payload or _read_json(paths["application"])
    character_ids = {str(item.get("character_id")) for item in highlight.get("characters", [])}
    volumes = highlight.get("volumes", [])
    volume_numbers = [item.get("volume") for item in volumes]
    if volume_numbers != list(range(1, 16)):
        errors.append("character highlight matrix must cover volumes 1-15 in order")
    every_agency = all(
        set(item.get("agency", {})) == character_ids
        and all(
            all(
                value.get(field)
                for field in (
                    "independent_action",
                    "on_page_obligation",
                    "failure_consequence",
                )
            )
            for value in item.get("agency", {}).values()
        )
        for item in volumes
    )
    agency_actions_by_character = {
        character_id: [
            volume.get("agency", {})
            .get(character_id, {})
            .get("independent_action")
            for volume in volumes
        ]
        for character_id in character_ids
    }
    agency_actions_are_volume_specific = all(
        len(actions) == len(set(actions))
        for actions in agency_actions_by_character.values()
    )
    if not every_agency:
        errors.append("every volume must preserve independent agency for all core characters")
    if not agency_actions_are_volume_specific:
        errors.append("character agency actions must be specific to each volume")
    highlight_counts = {character_id: 0 for character_id in character_ids}
    spotlight_highlights_match = True
    for volume in volumes:
        spotlight = set(volume.get("primary_spotlight", []))
        highlighted = {
            item.get("character_id")
            for item in volume.get("signature_highlights", [])
        }
        if not spotlight or spotlight != highlighted:
            spotlight_highlights_match = False
        for item in volume.get("signature_highlights", []):
            character_id = item.get("character_id")
            if character_id in highlight_counts and all(
                item.get(field)
                for field in ("irreversible_choice", "competence_display", "cost", "reader_payoff")
            ):
                highlight_counts[character_id] += 1
    three_highlights = bool(highlight_counts) and all(count >= 3 for count in highlight_counts.values())
    if not three_highlights:
        errors.append("every core character needs at least three signature highlights")
    if not spotlight_highlights_match:
        errors.append(
            "each volume must distinguish spotlight highlights from supporting agency"
        )
    competencies = atlas.get("competencies", [])
    ranks = atlas.get("authority_ranks", [])
    atlas_volumes = atlas.get("volumes", [])
    fixed_permissions = (
        len(competencies) == 6
        and len(ranks) == 4
        and all(
            all(item.get(field) for field in ("entry_proof", "permissions", "prohibitions", "liability"))
            for item in ranks
        )
        and [item.get("volume") for item in atlas_volumes] == list(range(1, 16))
        and all(
            all(
                item.get(field)
                for field in (
                    "scope",
                    "entry_conditions",
                    "new_rule",
                    "irreversible_cost",
                    "evidence_routes",
                )
            )
            for item in atlas_volumes
        )
    )
    if not fixed_permissions:
        errors.append("world/progression atlas permissions or volume map is incomplete")
    dossiers = history.get("dossiers", [])
    history_changes_plot = (
        [item.get("volume") for item in dossiers] == list(range(1, 16))
        and all(
            all(
                item.get(field)
                for field in (
                    "carrier",
                    "public_account",
                    "suppressed_burden",
                    "present_trigger",
                    "initial_misreading",
                    "reveal",
                    "plot_consequence",
                    "originality_guard",
                )
            )
            for item in dossiers
        )
    )
    if not history_changes_plot:
        errors.append("embedded history must change the present plot in every volume")
    semantic_beats = volume1_beats.get("chapters", [])
    beat_ids = [item.get("chapter_id") for item in semantic_beats]
    expected_beat_ids = [f"chapter-{number:04d}" for number in range(1, 67)]
    if beat_ids != expected_beat_ids:
        errors.append("Volume 1 semantic beat contract must cover chapters 1-66 in order")
    if any(
        not item.get("character_pressure")
        or not item.get("progression_function")
        or not item.get("history_function")
        or not item.get("reader_payoff")
        or not item.get("originality_guard")
        for item in semantic_beats
    ):
        errors.append("Volume 1 semantic beats are incomplete")
    future_dossier_names = {
        str(item.get("dossier_name"))
        for item in dossiers
        if int(item.get("volume", 0)) > 1
    }
    leaked_future_dossiers = sorted(
        {
            name
            for item in semantic_beats
            for name in future_dossier_names
            if name and name in str(item.get("history_function", ""))
        }
    )
    if leaked_future_dossiers:
        errors.append(
            "Volume 1 semantic beats leak future dossiers: "
            + ", ".join(leaked_future_dossiers)
        )
    profile_hash = _sha256(PROFILE_PATH) if PROFILE_PATH.is_file() else ""
    library_hash = _sha256(LIBRARY_PATH) if LIBRARY_PATH.is_file() else ""
    if application.get("source_signature_profiles_sha256") != profile_hash:
        errors.append("project semantic application has stale signature profile hash")
    if application.get("source_mechanism_library_sha256") != library_hash:
        errors.append("project semantic application has stale mechanism library hash")
    decisions = application.get("dimension_decisions", [])
    decision_dimensions = [item.get("dimension") for item in decisions]
    if len(decision_dimensions) != len(set(decision_dimensions)):
        errors.append("duplicate project semantic dimension decision")
    if (
        len(decision_dimensions) != len(DIMENSIONS)
        or set(decision_dimensions) != set(DIMENSIONS)
    ):
        errors.append("project application must decide every semantic dimension")
    allowed = {"adopt", "transform", "defer", "reject"}
    if any(
        item.get("decision") not in allowed
        or not item.get("rationale")
        or not item.get("canonical_artifacts")
        or not item.get("originality_transformation")
        for item in decisions
    ):
        errors.append("dimension decisions are incomplete")
    signature_decisions = application.get("signature_decisions", [])
    signature_decision_cells = [
        (item.get("source_book"), item.get("source_dimension"))
        for item in signature_decisions
    ]
    if len(signature_decision_cells) != len(set(signature_decision_cells)):
        errors.append("duplicate selected source-book signature decision")
    for item in signature_decisions:
        if (
            item.get("decision") not in {"adopt", "transform", "reject"}
            or not item.get("source_book")
            or item.get("source_dimension") not in DIMENSIONS
            or not item.get("rationale")
            or not item.get("originality_transformation")
            or not item.get("canonical_artifacts")
        ):
            errors.append("signature decision is incomplete")
    expected_source_books = {
        item.get("book_title")
        for item in _read_json(PROFILE_PATH).get("profiles", [])
    }
    profiles = _read_json(PROFILE_PATH).get("profiles", [])
    expected_cells = {
        (profile.get("profile_id"), profile.get("book_title"), dimension)
        for profile in profiles
        for dimension in DIMENSIONS
    }
    dispositions = application.get("signature_dimension_dispositions", [])
    selected_by_cell = {
        (item.get("source_book"), item.get("source_dimension")): item
        for item in signature_decisions
    }
    disposition_cells = [
        (
            item.get("source_profile_id"),
            item.get("source_book"),
            item.get("source_dimension"),
        )
        for item in dispositions
    ]
    if len(disposition_cells) != len(set(disposition_cells)):
        errors.append("duplicate source-book signature dimension disposition")
    if set(disposition_cells) != expected_cells:
        errors.append("project application must disposition all 216 protected signature cells")
    disposition_source_books = {item.get("source_book") for item in dispositions}
    if disposition_source_books != expected_source_books:
        errors.append("project application must disposition every protected source book")
    profile_map = {
        (profile.get("profile_id"), profile.get("book_title")): profile
        for profile in profiles
    }
    for item in dispositions:
        profile = profile_map.get(
            (item.get("source_profile_id"), item.get("source_book"))
        )
        dimension = item.get("source_dimension")
        source = (profile or {}).get("dimensions", {}).get(dimension, {})
        expected_digest = hashlib.sha256(
            json.dumps(
                source.get("findings", []), ensure_ascii=False, sort_keys=True
            ).encode("utf-8")
        ).hexdigest()
        if item.get("source_finding_digest") != expected_digest:
            errors.append(
                f"stale signature finding disposition: {item.get('source_book')}:{dimension}"
            )
        if (
            item.get("decision") not in allowed
            or item.get("review_status") not in {
                "project_activated",
                "project_rejected",
                "protected_deferred",
            }
            or not item.get("rationale")
            or not item.get("canonical_artifacts")
            or not item.get("originality_transformation")
            or not item.get("activation_requirements")
        ):
            errors.append("signature dimension disposition is incomplete")
        for relative in item.get("canonical_artifacts", []):
            if not (ROOT / str(relative)).is_file():
                errors.append(f"signature disposition artifact is missing: {relative}")
        selected = selected_by_cell.get(
            (item.get("source_book"), item.get("source_dimension"))
        )
        if item.get("decision") == "defer":
            if selected is not None:
                errors.append(
                    "deferred signature disposition must not enter selected decisions: "
                    f"{item.get('source_book')}:{dimension}"
                )
        elif selected is None:
            errors.append(
                "active signature disposition lacks an explicit selected decision: "
                f"{item.get('source_book')}:{dimension}"
            )
        elif any(
            item.get(key) != selected.get(key)
            for key in (
                "decision",
                "rationale",
                "canonical_artifacts",
                "originality_transformation",
            )
        ):
            errors.append(
                "active signature disposition differs from selected decision: "
                f"{item.get('source_book')}:{dimension}"
            )
    active_disposition_cells = {
        (item.get("source_book"), item.get("source_dimension"))
        for item in dispositions
        if item.get("decision") != "defer"
    }
    if set(signature_decision_cells) != active_disposition_cells:
        errors.append(
            "selected signature decisions must exactly equal active dispositions"
        )
    checks = {
        "every_character_has_three_signature_highlights": three_highlights,
        "every_volume_preserves_all_character_agency": every_agency,
        "character_agency_is_volume_specific": agency_actions_are_volume_specific,
        "spotlight_highlights_match_primary_cast": spotlight_highlights_match,
        "fixed_progression_permissions": fixed_permissions,
        "history_changes_present_plot": history_changes_plot,
        "volume1_has_no_future_dossier_leak": not leaked_future_dossiers,
        "volume1_semantic_beats_complete": beat_ids == expected_beat_ids,
        "all_semantic_dimensions_decided": {
            item.get("dimension") for item in decisions
        } == set(DIMENSIONS),
        "all_source_books_decided": disposition_source_books == expected_source_books,
        "all_signature_cells_dispositioned": set(disposition_cells) == expected_cells,
        "source_hashes_current": not any("stale" in error for error in errors),
    }
    return {
        "version": VERSION,
        "project_id": project_id,
        "valid": not errors and all(checks.values()),
        "errors": errors,
        "checks": checks,
        "character_count": len(character_ids),
        "volume_count": len(volumes),
        "history_dossier_count": len(dossiers),
        "volume1_semantic_beat_count": len(semantic_beats),
        "highlight_counts": highlight_counts,
    }


def build_literary_semantic_status(project_id: str | None = None) -> dict[str, Any]:
    research = validate_literary_semantic_assets()
    project = (
        validate_project_semantic_contracts(project_id)
        if project_id
        else {"valid": False, "status": "project_not_selected"}
    )
    valid = bool(research.get("valid") and project.get("valid"))
    return {
        "version": VERSION,
        "valid": valid,
        "research_semantics": research,
        "project_semantics": project,
        "status": "semantic_integrity_verified" if valid else "blocked_on_semantic_integrity",
        "next_action": (
            "Run independent semantic and project-impact review."
            if valid
            else "Repair literary semantic profiles or project application contracts."
        ),
    }
