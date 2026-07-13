from __future__ import annotations

"""Explicit, testable model routing for NRL production roles."""

from typing import Any


VERSION = "0.21"
ROUTES: dict[str, dict[str, Any]] = {
    "showrunner": {"model": "gpt-5.6-sol", "effort": "max", "reason": "high-risk long-range planning and adjudication"},
    "writer": {"model": "gpt-5.6-sol", "effort": "max", "reason": "primary prose route after the blind calibration's positive Sol controls"},
    "observer": {"model": "gpt-5.6-luna", "effort": "medium", "reason": "schema-bound fact extraction from final text"},
    "mechanical": {"model": "gpt-5.6-luna", "effort": "low", "reason": "low-risk structured candidates only"},
}


def route_model(role: str) -> dict[str, Any]:
    if role not in ROUTES:
        raise ValueError(f"unknown production model role: {role}")
    return {"role": role, **ROUTES[role]}


def build_model_routing_status() -> dict[str, Any]:
    return {"version": VERSION, "routes": [route_model(role) for role in ROUTES]}
