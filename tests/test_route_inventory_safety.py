from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'server.py'
DASHBOARD_FEATURES_API = ROOT / 'dashboard_features_api.py'

SERVER_ROUTE_LITERAL_RE = re.compile(
    r"parsed\.path\s*(?:==|!=)\s*['\"]([^'\"]+)['\"]|"
    r"parsed\.path\.startswith\(['\"]([^'\"]+)['\"]\)"
)
PATH_ROUTE_LITERAL_RE = re.compile(
    r"\bpath\s*(?:==|!=)\s*['\"]([^'\"]+)['\"]|"
    r"\bpath\.startswith\(['\"]([^'\"]+)['\"]\)"
)
MUTATING_GET_TOKENS = (
    '/run', '/start', '/save', '/update', '/delete', '/remove', '/sync',
    '/commit', '/deploy', 'backup', '/logout', '/test-email', '/action',
    '/config', '/topics', '/notes', '/cancel', '/append', '/notify',
)
MUTATING_CALL_RE = re.compile(
    r"\b(?:sh\.)?(?:supa_insert|supa_update|supa_delete|create_budget_notification)\s*\("
    r"|\b(?:log_existing_operation|notify_operation)\s*\("
)

# Existing legacy GET side effects. These are not endorsed; they are pinned so
# future work can remove them deliberately and no new mutating GET routes slip in.
KNOWN_LEGACY_MUTATING_GET_ROUTES = {
    '/api/auth/logout',
    '/api/cloud-backup',
}

# There is a large old code block after do_GET's static fallback. It is currently
# unreachable, but it contains many mutating-looking routes. This guard makes the
# boundary explicit before any later refactor touches that area.
DO_GET_STATIC_FALLBACK = '        return self.serve_static(parsed.path)'


def _source(path: Path = SERVER) -> str:
    return path.read_text(encoding='utf-8')


def _method_body(source: str, method_name: str) -> str:
    marker = f'    def {method_name}(self):'
    start = source.index(marker)
    next_method = re.search(r'^    def \w+\(self\):', source[start + len(marker):], flags=re.M)
    end = start + len(marker) + next_method.start() if next_method else len(source)
    return source[start:end]


def _function_body(source: str, function_name: str) -> str:
    marker = f'def {function_name}('
    start = source.index(marker)
    next_function = re.search(r'^def \w+\(', source[start + len(marker):], flags=re.M)
    end = start + len(marker) + next_function.start() if next_function else len(source)
    return source[start:end]


def _route_literals(block: str, pattern: re.Pattern[str] = SERVER_ROUTE_LITERAL_RE) -> set[str]:
    routes = set()
    for match in pattern.finditer(block):
        routes.add(next(group for group in match.groups() if group))
    # Handle tuple membership like parsed.path in ('/api/a', '/api/b') conservatively.
    for tuple_match in re.finditer(r"(?:parsed\.)?path\s+in\s+\((.*?)\)", block, flags=re.S):
        routes.update(re.findall(r"['\"](/[^'\"]+)['\"]", tuple_match.group(1)))
    return routes


def _looks_mutating_get(route: str) -> bool:
    return any(token in route for token in MUTATING_GET_TOKENS)


def _df_new_paths_from_server_do_post() -> set[str]:
    body = _method_body(_source(), 'do_POST')
    match = re.search(r"_df_new_paths\s*=\s*\((.*?)\)\s*\n\s*if any", body, flags=re.S)
    assert match, 'server.py do_POST should expose the dashboard feature API route allowlist'
    return set(re.findall(r"['\"](/[^'\"]+)['\"]", match.group(1)))


def test_do_get_has_explicit_static_fallback_before_legacy_unreachable_block():
    body = _method_body(_source(), 'do_GET')
    assert DO_GET_STATIC_FALLBACK in body
    fallback_pos = body.index(DO_GET_STATIC_FALLBACK)
    legacy_pos = body.index("if parsed.path == '/api/stuck-projects':")
    assert fallback_pos < legacy_pos


def test_reachable_get_mutating_routes_are_only_documented_legacy_exceptions():
    body = _method_body(_source(), 'do_GET')
    reachable = body[:body.index(DO_GET_STATIC_FALLBACK)]
    mutating = {route for route in _route_literals(reachable) if route.startswith('/api/') and _looks_mutating_get(route)}
    assert mutating == KNOWN_LEGACY_MUTATING_GET_ROUTES


def test_delegated_dashboard_feature_get_routes_do_not_write_state():
    body = _function_body(_source(DASHBOARD_FEATURES_API), 'handle_get')
    mutating_calls = [
        line.strip()
        for line in body.splitlines()
        if MUTATING_CALL_RE.search(line)
    ]
    assert mutating_calls == []


def test_delegated_budget_check_get_is_read_only_and_post_can_create_notifications():
    source = _source(DASHBOARD_FEATURES_API)
    get_body = _function_body(source, 'handle_get')
    post_body = _function_body(source, 'handle_post')
    assert "if path == '/api/budget/check':" in get_body
    get_budget_block = get_body[get_body.index("if path == '/api/budget/check':"):get_body.index("if path == '/api/budget/status':")]
    assert 'create_budget_notification' not in get_budget_block

    assert "if path == '/api/budget/check':" in post_body
    post_budget_block = post_body[post_body.index("if path == '/api/budget/check':"):post_body.index("if path == '/api/budget-limits':")]
    assert 'create_budget_notification' in post_budget_block
    assert '/api/budget/check' in _df_new_paths_from_server_do_post()


def test_unreachable_legacy_block_is_not_accidentally_promoted_before_static_fallback():
    body = _method_body(_source(), 'do_GET')
    reachable = body[:body.index(DO_GET_STATIC_FALLBACK)]
    legacy_mutating_routes = {
        '/api/stuck-projects/alerts/test-email',
        '/api/improve/start',
        '/api/backup/run',
        '/api/radar/export/excel',
        '/api/bulk',
    }
    reachable_routes = _route_literals(reachable)
    assert legacy_mutating_routes.isdisjoint(reachable_routes)


def test_post_handler_owns_expected_mutating_dashboard_routes():
    body = _method_body(_source(), 'do_POST')
    routes = _route_literals(body)
    df_routes = _df_new_paths_from_server_do_post()
    expected_post_routes = {
        '/api/auth/login',
        '/api/login',
        '/api/kwr/start',
        '/api/kwr/swarm',
        '/api/dashboard/clear-cache',
        '/api/projects/star',
        '/api/settings/theme',
        '/api/improve/start',
        '/api/improve/instructions',
        '/api/productivity/notifications',
        '/api/productivity/audit',
        '/api/template-connectors/test',
        '/api/playground/templates',
        '/api/preferences',
        '/api/stuck-projects/sync',
        '/api/stuck-projects/bulk-update',
        '/api/stuck-projects/alerts/test-email',
    }
    expected_delegated_post_routes = {
        '/api/notifications',
        '/api/notifications/mark-read',
        '/api/notifications/mark-all-read',
        '/api/budget-limits',
        '/api/budget/check',
        '/api/template-versions',
        '/api/reports/generate',
        '/api/reports/export',
        '/api/report-schedules',
        '/api/quick-actions',
    }
    assert not (expected_post_routes - routes)
    assert not (expected_delegated_post_routes - df_routes)
