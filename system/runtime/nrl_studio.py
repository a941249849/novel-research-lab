from __future__ import annotations

import html
import json
from pathlib import Path

from nrl_paths import runtime_path


def load_json(relative: str):
    path = runtime_path(relative)
    if not path.exists():
        return [] if relative.endswith(".json") else {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_list(items) -> str:
    if not items:
        return "<li>None</li>"
    return "".join(f"<li>{html.escape(str(item))}</li>" for item in items)


def render_studio() -> Path:
    state = load_json("system/mission_controller/current_phase_state.json")
    registry = load_json("system/runtime/mission_registry.json")
    out_dir = runtime_path("system/runtime/studio")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    missions = "".join(
        f"<li>{html.escape(item.get('mission_id', 'unknown'))}: {html.escape(item.get('status', 'unknown'))}</li>"
        for item in registry
    )
    if not missions:
        missions = "<li>No registered missions</li>"
    content = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Novel Research Lab Studio</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 32px; line-height: 1.45; }}
    section {{ border-top: 1px solid #ddd; padding-top: 16px; margin-top: 16px; }}
    code {{ background: #f5f5f5; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>Novel Research Lab Studio</h1>
  <p><strong>Read-only cockpit.</strong> All state mutations must go through runtime commands.</p>
  <section>
    <h2>Runtime Health</h2>
    <ul>
      <li><code>python3 system/runtime/nrl.py doctor</code></li>
      <li><code>python3 system/runtime/nrl.py advance</code></li>
      <li><code>python3 system/runtime/nrl.py check-inputs</code></li>
      <li><code>python3 system/runtime/nrl.py validate-state</code></li>
      <li><code>python3 system/runtime/nrl.py prepare-handoff --agent antigravity</code></li>
    </ul>
  </section>
  <section>
    <h2>Current Phase</h2>
    <p>{html.escape(str(state.get("current_phase", "unknown")))} / {html.escape(str(state.get("current_subphase", "unknown")))}</p>
    <p>Status: <code>{html.escape(str(state.get("phase_status", "unknown")))}</code></p>
  </section>
  <section>
    <h2>Next Mission</h2>
    <p>{html.escape(str(state.get("next_recommended_mission", "unknown")))}</p>
  </section>
  <section>
    <h2>Blocked Actions</h2>
    <ul>{render_list(state.get("blocked_actions", []))}</ul>
  </section>
  <section>
    <h2>Gate Chain</h2>
    <ul>
      <li>Validation: {html.escape(str(state.get("validation_status", "unknown")))}</li>
      <li>Review: {html.escape(str(state.get("review_status", "unknown")))}</li>
      <li>Owner Gate: {html.escape(str(state.get("owner_gate_status", "unknown")))}</li>
    </ul>
  </section>
  <section>
    <h2>Missions</h2>
    <ul>{missions}</ul>
  </section>
</body>
</html>
"""
    out.write_text(content, encoding="utf-8")
    return out
