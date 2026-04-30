from pathlib import Path
import re

import server

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'server.py'

UNSAFE_METHODS = ('POST', 'PUT', 'PATCH', 'DELETE')
HIGH_RISK_WRITE_PATHS = {
    '/api/delete-agent',
    '/api/kwr/save-obsidian',
    '/api/kwr/update-rows',
    '/api/studio/improve',
    '/api/playground/templates',
    '/api/playground/templates/example-id/favorite',
    '/api/playground/templates/example-id/export/prompt',
    '/api/preferences',
}
PUBLIC_UNSAFE_ALLOWED = {
    '/api/auth/login',
    '/api/login',
    '/api/auth/request-reset',
    '/api/auth/reset',
    '/api/reset-password',
}
CSRF_EXEMPT_ALLOWED = PUBLIC_UNSAFE_ALLOWED | {
    '/api/n8n/webhook',
    '/login',
    '/api/csrf',
    '/metrics',
}


def _source() -> str:
    return SERVER.read_text(encoding='utf-8')


def _method_body(source: str, method_name: str) -> str:
    marker = f'    def {method_name}(self):'
    start = source.index(marker)
    next_method = re.search(r'^    def \w+\(self\):', source[start + len(marker):], flags=re.M)
    end = start + len(marker) + next_method.start() if next_method else len(source)
    return source[start:end]


def _csrf_exempt_prefixes() -> tuple[str, ...]:
    return tuple(server._R3_CSRF_EXEMPT)


def _is_csrf_exempt(path: str) -> bool:
    return any(path.startswith(prefix) for prefix in _csrf_exempt_prefixes())


def test_public_path_policy_is_method_aware_for_unsafe_methods():
    for path in HIGH_RISK_WRITE_PATHS:
        for method in UNSAFE_METHODS:
            assert not server._stage8_public_path(path, method=method), f'{method} {path} must require auth'

    for path in PUBLIC_UNSAFE_ALLOWED:
        assert server._stage8_public_path(path, method='POST'), f'{path} should remain public for login/reset compatibility'


def test_read_only_public_compatibility_is_preserved_for_get_routes():
    assert server._stage8_public_path('/api/playground/templates', method='GET')
    assert server._stage8_public_path('/api/playground/templates/example-id', method='GET')
    assert server._stage8_public_path('/api/playground/exports/example-id', method='GET')
    assert server._stage8_public_path('/api/preferences', method='GET')
    assert server._stage8_public_path('/api/studio/improve/rules', method='GET')


def test_csrf_exemptions_do_not_cover_dashboard_write_routes():
    for path in HIGH_RISK_WRITE_PATHS:
        assert not _is_csrf_exempt(path), f'{path} must require CSRF on unsafe methods'

    for path in CSRF_EXEMPT_ALLOWED:
        assert _is_csrf_exempt(path), f'{path} should remain in the explicit compatibility exemption set'


def test_post_and_delete_handlers_check_auth_before_csrf():
    src = _source()
    for method in ('do_POST', 'do_DELETE'):
        body = _method_body(src, method)
        auth_pos = body.index('_stage8_check_auth(self, parsed)')
        csrf_pos = body.index('_r3_check_csrf_or_warn(self, parsed)')
        assert auth_pos < csrf_pos


def test_unsafe_public_policy_is_used_by_auth_gate():
    src = _source()
    auth_gate = src[src.index('def _stage8_check_auth'):src.index('def _stage8_client_ip')]
    assert "method = getattr(handler, 'command', 'GET')" in auth_gate
    assert '_stage8_public_path(path, method=method)' in auth_gate
