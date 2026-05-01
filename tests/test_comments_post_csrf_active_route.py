from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SERVER = ROOT / "server.py"


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def _server() -> str:
    return SERVER.read_text(encoding="utf-8")


def _active_do_post_block() -> str:
    s = _server()
    start = s.rfind("    def do_POST(self):")
    assert start != -1, "active do_POST not found"
    end = s.find("\n    def ", start + 1)
    return s[start : end if end != -1 else len(s)]


def _save_comment_block() -> str:
    html = _index()
    start = html.index("async function saveComment(btn)")
    end = html.index("function openCommentsModal", start)
    return html[start:end]


def test_comments_save_uses_explicit_csrf_post_helper():
    html = _index()
    block = _save_comment_block()

    assert "COMMENTS_EXPLICIT_CSRF_POST_2026_05_01" in html
    assert "async function commentsPostJson(payload){" in html
    assert "await window.dashboardEnsureCsrf()" in html
    assert "'X-CSRF-Token':csrf" in html
    assert "credentials:'same-origin'" in html
    assert "fetch('/api/comments'" in html

    assert "const {res,data}=await commentsPostJson({" in block
    assert "const res=await fetch('/api/comments'" not in block
    assert "headers:{'Content-Type':'application/json'}" not in block


def test_comments_post_route_is_wired_in_active_do_post():
    block = _active_do_post_block()

    assert "COMMENTS_ACTIVE_POST_ROUTE_2026_05_01" in block
    assert "if parsed.path == '/api/comments':" in block
    assert "payload = read_request_json(self) or {}" in block
    assert "result = save_supabase_comment(payload)" in block
    assert "return json_response(self, 200, result)" in block


def test_legacy_shadowed_comments_post_block_is_not_the_only_route():
    server = _server()
    active = _active_do_post_block()

    # Historical code had /api/comments in an earlier post-dispatch block; guard
    # that the live handler contains its own copy so Python method ordering cannot
    # silently shadow Review Notes saves.
    assert server.count("if parsed.path == '/api/comments':") >= 1
    assert "if parsed.path == '/api/comments':" in active
