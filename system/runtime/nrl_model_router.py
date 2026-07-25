from __future__ import annotations

"""Explicit, testable model routing for NRL production roles."""

from typing import Any


VERSION = "0.27"
ROUTES: dict[str, dict[str, Any]] = {
    "showrunner": {"model": "gpt-5.6-sol", "effort": "max", "reason": "high-risk long-range planning and adjudication"},
    "reviewer": {
        "model": "gpt-5.6-sol", "effort": "high",
        "fallback_provider": "antigravity", "fallback_model": "Claude Opus 4.6 (Thinking)",
        "secondary_fallback_model": "Gemini 3.5 Flash (High)",
        "reason": "independent causal, continuity, vitality, and anti-AI-taste adjudication",
    },
    "writer": {
        "model": "gpt-5.6-terra", "effort": "high",
        "fallback_provider": "antigravity", "fallback_model": "Gemini 3.1 Pro (High)",
        "secondary_fallback_model": "Gemini 3.5 Flash (High)",
        "tertiary_fallback_model": "Claude Opus 4.6 (Thinking)",
        "reason": "Terra handles sustained drafting; Gemini Pro is the quota-isolated fallback; Sol is reserved for window adjudication",
    },
    "observer": {
        "model": "gpt-5.6-luna", "effort": "medium",
        "fallback_provider": "antigravity", "fallback_model": "Gemini 3.5 Flash (High)",
        "reason": "schema-bound fact extraction from final text with an independently validated fallback",
    },
    "editor": {
        "model": "gpt-5.6-terra", "effort": "medium",
        "fallback_provider": "antigravity", "fallback_model": "Gemini 3.5 Flash (High)",
        "reason": "bounded compression and bridge editing require instruction fidelity, not another literary rewrite",
    },
    "mechanical": {"model": "gpt-5.6-luna", "effort": "low", "reason": "low-risk structured candidates only"},
}


def route_model(role: str) -> dict[str, Any]:
    if role not in ROUTES:
        raise ValueError(f"unknown production model role: {role}")
    return {"role": role, **ROUTES[role]}


def build_model_routing_status() -> dict[str, Any]:
    contract = validate_model_team_contract()
    return {
        "version": VERSION,
        "strategy": "codex_three_model_team_with_antigravity_fallback",
        "routes": [route_model(role) for role in ROUTES],
        "contract": contract,
    }


def validate_model_team_contract() -> dict[str, Any]:
    expected = {
        "showrunner": "gpt-5.6-sol",
        "reviewer": "gpt-5.6-sol",
        "writer": "gpt-5.6-terra",
        "editor": "gpt-5.6-terra",
        "observer": "gpt-5.6-luna",
        "mechanical": "gpt-5.6-luna",
    }
    errors = [
        f"{role} must route to {model}"
        for role, model in expected.items()
        if ROUTES.get(role, {}).get("model") != model
    ]
    for role in ("reviewer", "writer", "editor", "observer"):
        route = ROUTES.get(role, {})
        if route.get("fallback_provider") != "antigravity" or not route.get("fallback_model"):
            errors.append(f"{role} must declare an Antigravity fallback")
    return {
        "valid": not errors,
        "errors": errors,
        "models": sorted({route["model"] for route in ROUTES.values()}),
        "role_count": len(ROUTES),
    }
