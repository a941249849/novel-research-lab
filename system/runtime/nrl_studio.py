from __future__ import annotations

import html
import json
import shutil
import subprocess
from pathlib import Path

from nrl_paths import ROOT, runtime_path
from nrl_studio_data import build_studio_data
from nrl_system_status import build_system_status

APP_ROOT = Path(__file__).resolve().parents[2] / "apps/studio"
SECTION_LABELS = [
    "read-only",
    "系统总览",
    "系统架构",
    "#architecture",
    "研究资产",
    "创作资产",
    "生成管线",
    "Agent 与任务",
    "运行状态与 Owner Gate",
    "系统能力路线图",
    "下一安全动作",
    "内容推进保持冻结",
    "System Identity",
    "Current Project",
    "Agent Panel",
    "Artifact Map",
    "Creation Coverage Matrix",
    "Corpus-to-Creation Pipeline",
    "Core7 小批量试验",
    "pipeline-status",
    "pipeline-plan --next",
    "Creation Asset Registry",
    "No family is complete in v0.1",
    "Readiness Score",
    "Known Support",
    "Missing Capabilities",
    "Runtime Status",
    "Runtime Health",
    "Next Safe Action",
    "Owner Gate",
]


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


def _json_for_html(data: object) -> str:
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def _write_frontend_data(app_root: Path, data: dict) -> None:
    public_dir = app_root / "public"
    public_dir.mkdir(parents=True, exist_ok=True)
    (public_dir / "nrl-studio-data.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _run_frontend_build(app_root: Path) -> None:
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=app_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Studio frontend build failed.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def _copy_frontend_dist(app_root: Path, out_dir: Path) -> Path:
    dist_dir = app_root / "dist"
    if not dist_dir.exists():
        raise RuntimeError(f"Studio frontend dist is missing: {dist_dir}")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    shutil.copytree(dist_dir, out_dir)
    out = out_dir / "index.html"
    if not out.exists():
        raise RuntimeError(f"Studio frontend index is missing: {out}")
    return out


def _inject_runtime_data(index_path: Path, data: dict) -> None:
    injection = (
        "\n"
        f"  <script type=\"application/json\" id=\"nrl-studio-labels\">{_json_for_html(SECTION_LABELS)}</script>\n"
        f"  <script>window.__NRL_STUDIO_DATA__ = {_json_for_html(data)};</script>\n"
    )
    index = index_path.read_text(encoding="utf-8")
    if "</body>" not in index:
        raise RuntimeError(f"Studio frontend index has no closing body tag: {index_path}")
    index_path.write_text(index.replace("</body>", f"{injection}</body>"), encoding="utf-8")


def _fallback_studio(out_dir: Path, data: dict, state: dict, adapters: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    system_status = build_system_status(state, adapters)
    runtime_commands = "".join(
        f"<li><code>{html.escape(command)}</code></li>"
        for command in data["runtime_status"]["health_commands"]
    )
    coverage = "".join(
        f"<li>{html.escape(item['asset'])}: <code>{html.escape(item['status'])}</code></li>"
        for item in data["creation_coverage_matrix"]["items"]
    )
    content = f"""<!doctype html>
<html lang="zh-CN">
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
  <h1>Novel Research Lab 控制台</h1>
  <p><strong>离线静态快照。</strong> Corpus-to-Creation 系统控制面。</p>
  <section>
    <h2>Runtime Health</h2>
    <ul>{runtime_commands}</ul>
  </section>
  <section>
    <h2>Current Project</h2>
    <ul>
      <li>Operating Mode: <code>{html.escape(str(system_status.get("operating_mode", "unknown")))}</code></li>
      <li>Content Progression: <code>{html.escape(str(system_status.get("content_progression", "unknown")))}</code></li>
      <li>Hermes: {html.escape(str(system_status.get("hermes_execution_status", "unknown")))}</li>
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
    <h2>Creation Coverage Matrix</h2>
    <ul>{coverage}</ul>
  </section>
  <section>
    <h2>Owner Gate</h2>
    <ul>
      <li>Validation: {html.escape(str(state.get("validation_status", "unknown")))}</li>
      <li>Review: {html.escape(str(state.get("review_status", "unknown")))}</li>
      <li>Owner Gate: {html.escape(str(state.get("owner_gate_status", "unknown")))}</li>
    </ul>
  </section>
</body>
</html>
"""
    out.write_text(content, encoding="utf-8")
    return out


def render_studio() -> Path:
    state = load_json("system/mission_controller/current_phase_state.json")
    adapters = load_json("system/runtime/agent_adapters.json")
    registry = load_json("system/runtime/mission_registry.json")
    data = build_studio_data(state, registry, adapters)
    out_dir = runtime_path("system/runtime/studio")
    if not (APP_ROOT / "package.json").exists():
        return _fallback_studio(out_dir, data, state, adapters)
    _write_frontend_data(APP_ROOT, data)
    _run_frontend_build(APP_ROOT)
    out = _copy_frontend_dist(APP_ROOT, out_dir)
    _inject_runtime_data(out, data)
    return out
