from __future__ import annotations

import os
from pathlib import Path


def resolve_root() -> Path:
    override = os.environ.get("NRL_ROOT")
    if override:
        return Path(override).resolve()
    return Path(__file__).resolve().parents[2]


ROOT = resolve_root()


def runtime_path(relative: str) -> Path:
    return ROOT / relative
