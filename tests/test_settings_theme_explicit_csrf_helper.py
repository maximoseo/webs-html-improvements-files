from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / 'index.html').read_text(encoding='utf-8')
SERVER = (ROOT / 'server.py').read_text(encoding='utf-8')
MARKER = 'SETTINGS_THEME_EXPLICIT_CSRF_POST_2026_05_01'


def _theme_block():
    start = INDEX.index('// Theme')
    end = INDEX.index('(function initTheme()', start)
    return INDEX[start:end]


def _active_post_block():
    start = SERVER.index('    def do_POST(self):')
    next_method = SERVER.find('\n    def ', start + 1)
    return SERVER[start: next_method if next_method != -1 else len(SERVER)]


def test_settings_theme_frontend_uses_explicit_csrf_helper():
    block = _theme_block()
    assert MARKER in block
    assert 'async function settingsThemePostJson(color){' in block
    helper = block[block.index('async function settingsThemePostJson'):block.index('function setThemeColor')]
    assert 'dashboardEnsureCsrf' in helper
    assert "headers['X-CSRF-Token']=csrf" in helper
    assert "credentials:'same-origin'" in helper or 'credentials:"same-origin"' in helper
    assert "body:JSON.stringify({theme_color:color})" in helper


def test_set_theme_color_uses_helper_not_raw_fetch():
    block = _theme_block()
    set_theme = block[block.index('function setThemeColor'):]
    assert "settingsThemePostJson(color).catch(function(){});" in set_theme
    assert "fetch('/api/settings/theme'" not in set_theme
    assert 'headers:{\'Content-Type\':\'application/json\'}' not in set_theme


def test_settings_theme_active_post_route_remains_guarded_and_validates_color():
    active = _active_post_block()
    assert "/api/settings/theme" in active
    route = active[active.index("if parsed.path == '/api/settings/theme':"):]
    route = route[:route.index("# TEMPLATE_IMPROVEMENTS_POST_ACTIVE", 1)]
    assert 'read_request_json(self)' in route
    assert "valid_colors = ['purple', 'blue', 'green', 'red', 'orange', 'pink']" in route
    assert "if theme_color not in valid_colors:" in route
    assert 'return json_response(self, 400' in route
