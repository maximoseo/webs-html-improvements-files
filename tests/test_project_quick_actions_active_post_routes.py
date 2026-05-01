from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")


def _active_do_post_block() -> str:
    start = SERVER.rfind("    def do_POST(self):")
    assert start != -1, "active do_POST block not found"
    # The active do_POST is the last method-level POST handler; keep the block bounded enough
    # for static route-shadowing checks without depending on exact class end line.
    end_candidates = [pos for token in ("    def do_PUT", "    def do_DELETE", "    def do_OPTIONS", "    def log_message")
                      if (pos := SERVER.find(token, start + 1)) != -1]
    end = min(end_candidates) if end_candidates else len(SERVER)
    return SERVER[start:end]


def _do_get_block() -> str:
    start = SERVER.find("    def do_GET(self):")
    end = SERVER.find("    def do_POST(self):", start + 1)
    assert start != -1 and end != -1
    return SERVER[start:end]


def test_project_quick_action_post_routes_are_in_active_do_post():
    block = _active_do_post_block()
    assert "PROJECT_QUICK_ACTIONS_ACTIVE_POST_ROUTES_2026_05_01" in block
    for route in ("/api/projects/duplicate", "/api/projects/delete", "/api/projects/rename", "/api/projects/star"):
        assert route in block, f"{route} must be wired in active do_POST, not a shadowed handler"
    assert "read_request_json(self)" in block
    assert "_JSON_FILE_WRITE_LOCK" in block
    assert "_atomic_write_json_file" in block


def test_project_quick_actions_are_not_mutating_inside_do_get():
    block = _do_get_block()
    project_region_start = block.find("/api/projects/duplicate")
    if project_region_start != -1:
        project_region = block[project_region_start:project_region_start + 2200]
        assert "json.dump(data" not in project_region
        assert "_atomic_write_json_file" not in project_region
        assert "return json_response(self, 405" in project_region


def test_project_quick_action_frontend_uses_explicit_csrf_helper():
    assert "PROJECT_QUICK_ACTIONS_EXPLICIT_CSRF_POST_2026_05_01" in INDEX
    assert "async function projectQuickActionPostJson(" in INDEX
    helper_start = INDEX.index("async function projectQuickActionPostJson(")
    helper = INDEX[helper_start:INDEX.index("async function duplicateProject", helper_start)]
    assert "dashboardEnsureCsrf" in helper
    assert "X-CSRF-Token" in helper
    assert "credentials:'same-origin'" in helper or 'credentials:"same-origin"' in helper
    for route in ("/api/projects/duplicate", "/api/projects/delete", "/api/projects/star"):
        assert f"projectQuickActionPostJson('{route}'" in INDEX
        assert f"fetch('{route}'" not in INDEX
    assert "toggleStar('${p.name}',this,event)" in INDEX
    assert "function toggleStar(domain, btn, ev)" in INDEX
    assert "aria-pressed" in INDEX
