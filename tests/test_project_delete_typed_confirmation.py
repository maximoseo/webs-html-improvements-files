from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")
SERVER = (ROOT / "server.py").read_text(encoding="utf-8")

MARKER = "PROJECT_DELETE_TYPED_CONFIRMATION_2026_05_01"


def _active_do_post_block() -> str:
    start = SERVER.rfind("    def do_POST(self):")
    assert start != -1, "active do_POST block not found"
    end_candidates = [
        pos for token in ("    def do_PUT", "    def do_DELETE", "    def do_OPTIONS", "    def log_message")
        if (pos := SERVER.find(token, start + 1)) != -1
    ]
    end = min(end_candidates) if end_candidates else len(SERVER)
    return SERVER[start:end]


def _delete_project_function() -> str:
    start = INDEX.index("async function deleteProject(domain)")
    end = INDEX.index("async function toggleStar", start)
    return INDEX[start:end]


def test_project_delete_requires_typed_frontend_confirmation_before_post():
    assert MARKER in INDEX
    assert "function confirmProjectDelete(domain)" in INDEX
    confirm_start = INDEX.index("function confirmProjectDelete(domain)")
    confirm_block = INDEX[confirm_start:INDEX.index("async function deleteProject", confirm_start)]
    assert "window.prompt" in confirm_block
    assert "typed===domain" in confirm_block or "typed === domain" in confirm_block
    assert "Type the exact project/domain name" in confirm_block

    delete_block = _delete_project_function()
    assert "confirmProjectDelete(domain)" in delete_block
    assert "projectQuickActionPostJson('/api/projects/delete',{domain:domain,confirm_domain:domain})" in delete_block
    assert "confirm('Delete '+domain" not in delete_block


def test_project_delete_menu_labels_dangerous_action_as_confirmation_flow():
    card_start = INDEX.index("PROJECT_CARD_SAFE_RENDER_ESCAPE_2026_05_01")
    card_block = INDEX[card_start:INDEX.index("</div>\n      </div>\n      <div class=\"card-header\"", card_start)]
    assert "deleteProject('${_projectNameArg}')" in card_block
    assert "Delete…" in card_block or "Delete..." in card_block


def test_backend_project_delete_requires_matching_confirm_domain_before_write():
    block = _active_do_post_block()
    assert MARKER in block
    delete_route = block[block.index("if parsed.path in ('/api/projects/duplicate', '/api/projects/rename', '/api/projects/delete'):"):
                         block.index("# PROJECT_SETTINGS_POST_2026_04_29", block.index("if parsed.path in ('/api/projects/duplicate'"))]
    assert "confirm_domain" in delete_route
    assert "confirm_domain != domain" in delete_route or "domain != confirm_domain" in delete_route
    confirm_pos = delete_route.index("confirm_domain")
    write_pos = delete_route.rindex("_atomic_write_json_file(data_path, data)")
    assert confirm_pos < write_pos
