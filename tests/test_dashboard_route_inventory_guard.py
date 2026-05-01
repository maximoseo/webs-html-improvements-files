import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")

CRITICAL_ACTIVE_POST_ROUTES = {
    # Keep these narrow: routes recently fixed or known to be high-impact UI actions.
    "/api/studio/improve",
    "/api/prompt/improve",
    "/api/prompt/palette",
    "/api/prompt/brainstorm",
    "/api/prompt/tweak",
    "/api/prompt/commit",
    "/api/dashboard/clear-cache",
    "/api/projects/duplicate",
    "/api/projects/rename",
    "/api/projects/delete",
    "/api/projects/star",
    "/api/settings/theme",
}

EXPANDED_ROUTE_FAMILY_POST_ROUTES = {
    # DASHBOARD_ROUTE_INVENTORY_EXPANSION_2026_05_01
    # Curated expansion: state-changing route families already used by the UI.
    "/api/comments",
    "/api/kwr/start",
    "/api/kwr/swarm",
    "/api/template-connectors/test",
    "/api/tasks",
    "/api/tasks/sync-github",
}

ALL_GUARDED_POST_ROUTES = CRITICAL_ACTIVE_POST_ROUTES | EXPANDED_ROUTE_FAMILY_POST_ROUTES


def _method_block(name: str) -> str:
    start = SERVER.find(f"    def {name}(self):")
    assert start != -1, f"{name} not found"
    next_method = re.search(r"\n    def [a-zA-Z_]+\(self", SERVER[start + 1:])
    end = start + 1 + next_method.start() if next_method else len(SERVER)
    return SERVER[start:end]


def test_dashboard_has_single_active_handler_per_core_http_method():
    assert SERVER.count("    def do_POST(self):") == 1
    assert SERVER.count("    def do_GET(self):") == 1
    assert SERVER.count("    def do_DELETE(self):") == 1


def test_critical_mutating_routes_are_guarded_in_active_post_inventory():
    active_post = _method_block("do_POST")
    assert "DASHBOARD_ROUTE_INVENTORY_GUARD_2026_05_01" in active_post
    assert "DASHBOARD_ROUTE_INVENTORY_EXPANSION_2026_05_01" in active_post
    missing = sorted(route for route in ALL_GUARDED_POST_ROUTES if route not in active_post)
    assert not missing, "guarded mutating routes missing from active do_POST: " + ", ".join(missing)


def test_critical_project_and_prompt_frontend_routes_use_explicit_post_helpers():
    # This inventory intentionally focuses on high-impact UI actions already moved
    # to explicit CSRF helpers. It should fail if a later edit reintroduces raw
    # direct fetch calls that bypass the action-specific helper contract.
    assert "promptStudioJsonPost('/api/studio/improve'" in INDEX
    assert "projectQuickActionPostJson('/api/projects/star'" in INDEX
    assert "projectQuickActionPostJson('/api/projects/duplicate'" in INDEX
    assert "projectQuickActionPostJson('/api/projects/delete'" in INDEX
    forbidden_raw_calls = [
        "fetch('/api/studio/improve",
        "fetch('/api/prompt/",
        "fetch('/api/projects/star'",
        "fetch('/api/projects/duplicate'",
        "fetch('/api/projects/delete'",
    ]
    for raw in forbidden_raw_calls:
        assert raw not in INDEX, f"raw mutating fetch bypasses explicit helper: {raw}"


def test_do_get_does_not_write_for_critical_mutating_routes():
    do_get = _method_block("do_GET")
    for route in ALL_GUARDED_POST_ROUTES:
        pos = do_get.find(route)
        if pos == -1:
            continue
        window = do_get[max(0, pos - 500):pos + 1500]
        assert "read_request_json(self)" not in window, f"GET route reads request body near {route}"
        assert "json.dump(" not in window, f"GET route writes JSON directly near {route}"
        assert "_atomic_write_json_file" not in window, f"GET route writes JSON atomically near {route}"
