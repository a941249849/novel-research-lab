from __future__ import annotations

import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlparse

from nrl_creation_schemas import build_creation_schema_registry
from nrl_corpus_pipeline import build_pipeline_plan, build_pipeline_status
from nrl_paths import runtime_path
from nrl_registry import load_registry
from nrl_research_assets import build_research_asset_catalog
from nrl_studio_data import build_studio_data
from nrl_system_check import run_system_check, validate_runtime_state


STATE_PATH = runtime_path("system/mission_controller/current_phase_state.json")
ADAPTERS_PATH = runtime_path("system/runtime/agent_adapters.json")
STUDIO_ROOT = runtime_path("system/runtime/studio")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _studio_data() -> dict[str, Any]:
    return build_studio_data(
        _load_json(STATE_PATH),
        load_registry(),
        _load_json(ADAPTERS_PATH),
    )


def _pipeline_status() -> dict[str, Any]:
    return build_pipeline_status(_load_json(STATE_PATH), _load_json(ADAPTERS_PATH))


def _pipeline_plan(query: str) -> dict[str, Any]:
    params = parse_qs(query)
    next_only = params.get("next", ["false"])[0].lower() == "true"
    family_values = params.get("family", [])
    family = family_values[0] if family_values else None
    if not next_only and not family:
        raise ValueError("pipeline plan requires family=<asset_family> or next=true")
    return build_pipeline_plan(
        _load_json(STATE_PATH),
        _load_json(ADAPTERS_PATH),
        family=family,
        next_only=next_only,
    )


GET_ROUTES: dict[str, Callable[[], dict[str, Any]]] = {
    "/api/studio-data": _studio_data,
    "/api/research-assets": build_research_asset_catalog,
    "/api/creation-schemas": build_creation_schema_registry,
    "/api/pipeline-status": _pipeline_status,
}
ACTION_ROUTES: dict[str, Callable[[], dict[str, Any]]] = {
    "/api/actions/system-check": run_system_check,
    "/api/actions/validate-state": validate_runtime_state,
}


class StudioRequestHandler(SimpleHTTPRequestHandler):
    def _send_json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/pipeline-plan":
            try:
                self._send_json(200, _pipeline_plan(parsed.query))
            except ValueError as error:
                self._send_json(400, {"error": str(error)})
            except RuntimeError as error:
                self._send_json(400, {"error": str(error)})
            except Exception as error:
                self._send_json(500, {"error": str(error)})
            return
        route = GET_ROUTES.get(parsed.path)
        if route is not None:
            try:
                self._send_json(200, route())
            except Exception as error:
                self._send_json(500, {"error": str(error)})
            return
        super().do_GET()

    def do_POST(self) -> None:
        route = ACTION_ROUTES.get(self.path)
        if route is None:
            self._send_json(404, {"error": "unknown or forbidden action"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "request body must be a JSON object"})
            return
        if not isinstance(payload, dict) or payload:
            self._send_json(400, {"error": "action does not accept parameters"})
            return
        try:
            self._send_json(200, route())
        except Exception as error:
            self._send_json(500, {"error": str(error)})

    def log_message(self, format: str, *args: object) -> None:
        return


def create_studio_server(
    host: str = "127.0.0.1",
    port: int = 4173,
) -> ThreadingHTTPServer:
    STUDIO_ROOT.mkdir(parents=True, exist_ok=True)
    handler = partial(StudioRequestHandler, directory=str(STUDIO_ROOT))
    return ThreadingHTTPServer((host, port), handler)
