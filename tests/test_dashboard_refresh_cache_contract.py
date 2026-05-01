from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
SERVER = ROOT / "server.py"


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def _server() -> str:
    return SERVER.read_text(encoding="utf-8")


def test_refresh_cache_frontend_clears_project_cache_keys():
    html = _index()

    assert "DASHBOARD_REFRESH_CACHE_BUTTON_2026_04_26" in html
    assert "localStorage.removeItem('dashboard_cache')" in html
    assert "sessionStorage.removeItem('dashboard_cache')" in html
    assert "localStorage.removeItem('dashboard_projects_cache')" in html
    assert "sessionStorage.removeItem('dashboard_projects_cache')" in html
    assert "window.__fetchMemoClear" in html
    assert "loadDashboard({forceRefresh:true})" in html
    assert "'/api/dashboard/clear-cache'" in html


def test_refresh_cache_backend_contract_matches_frontend_cache_keys():
    server = _server()
    active = server[server.rfind("    def do_POST(self):"):]

    assert "DASHBOARD_REFRESH_CACHE_CONTRACT_FIX_2026_05_01" in active
    assert "if parsed.path == '/api/dashboard/clear-cache':" in active
    assert "'server_cache_control': 'no-store'" in active
    assert "'no-store-response'" in active
    assert "'localStorage:dashboard_cache'" in active
    assert "'sessionStorage:dashboard_cache'" in active
    assert "'localStorage:dashboard_projects_cache'" in active
    assert "'sessionStorage:dashboard_projects_cache'" in active
    assert "no project files were modified" in active


def test_refresh_cache_backend_reports_targets_without_deleting_files():
    server = _server()
    active = server[server.rfind("    def do_POST(self):"):]
    route = active[active.index("if parsed.path == '/api/dashboard/clear-cache':"):active.index("# PROJECT_SETTINGS_POST_2026_04_29")]

    assert "add_target('data.json', ROOT / 'data.json')" in route
    assert "add_target('outputs', ROOT / 'outputs')" in route
    assert "add_target('n8n-workflow-map.json', MAP_FILE)" in route
    assert "add_target('index.html', INDEX)" in route
    assert ".unlink(" not in route
    assert "shutil.rmtree" not in route
    assert "os.remove" not in route
