from __future__ import annotations

"""Explicit, testable model routing for NRL production roles."""

from typing import Any


VERSION = "0.22"
ROUTES: dict[str, dict[str, Any]] = {
    "showrunner": {"model": "gpt-5.6-sol", "effort": "max", "reason": "high-risk long-range planning and adjudication"},
    "writer": {
        "model": "gpt-5.6-sol", "effort": "max",
        "fallback_provider": "antigravity", "fallback_model": "Claude Opus 4.6 (Thinking)",
        "secondary_fallback_model": "Claude Sonnet 4.6 (Thinking)",
        "reason": "Sol is primary; isolated literary fallback prevents quota from stopping a registered batch",
    },
    "observer": {
        "model": "gpt-5.6-luna", "effort": "medium",
        "fallback_provider": "antigravity", "fallback_model": "Gemini 3.5 Flash (High)",
        "reason": "schema-bound fact extraction from final text with an independently validated fallback",
    },
    "mechanical": {"model": "gpt-5.6-luna", "effort": "low", "reason": "low-risk structured candidates only"},
}


def route_model(role: str) -> dict[str, Any]:
    if role not in ROUTES:
        raise ValueError(f"unknown production model role: {role}")
    return {"role": role, **ROUTES[role]}


def build_model_routing_status() -> dict[str, Any]:
    return {"version": VERSION, "routes": [route_model(role) for role in ROUTES]}
