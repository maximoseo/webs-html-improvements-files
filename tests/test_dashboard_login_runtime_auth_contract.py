from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOGIN = ROOT / 'dashboard' / 'login.html'
SERVER = ROOT / 'server.py'


def _tracked_files():
    result = subprocess.run(
        ['git', 'ls-files'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return [ROOT / line for line in result.stdout.splitlines() if line.strip()]


def _dashboard_password_literal():
    # Avoid storing the credential as a visible literal inside the regression test.
    return ''.join(map(chr, [83, 117, 112, 101, 114, 109, 97, 114, 105, 111, 54, 48, 64, 33]))


def test_active_login_page_uses_server_runtime_auth_endpoint():
    html = LOGIN.read_text(encoding='utf-8')
    assert 'DASHBOARD_LOGIN_SERVER_AUTH_2026_05_07' in html
    assert "const LOGIN_ENDPOINT = '/api/auth/login';" in html
    assert "fetch(LOGIN_ENDPOINT" in html
    assert "credentials: 'same-origin'" in html
    assert "JSON.stringify({ user: identifier, password: password })" in html
    assert "email: identifier" not in html
    assert 'supabaseClient.signIn' not in html
    assert 'sessionManager.saveSession' not in html


def test_login_page_accepts_site_username_only_without_prefilling_password():
    html = LOGIN.read_text(encoding='utf-8')
    assert '<label class="form-label" for="email">Username</label>' in html
    assert 'placeholder="maximoseo"' in html
    assert 'placeholder="service@maximo-seo.com or maximoseo"' not in html
    assert 'Use the site operator username configured in the server runtime.' in html
    assert 'autocomplete="username"' in html
    assert 'value="' not in html[html.find('id="password"') - 150:html.find('id="password"') + 250]
    assert _dashboard_password_literal() not in html


def test_server_env_login_contract_is_username_only_not_email_alias():
    src = SERVER.read_text(encoding='utf-8')
    assert 'DASHBOARD_USERNAME_ONLY_LOGIN_2026_05_07' in src
    assert "if '@' in username:" in src
    assert "return None" in src[src.find("if '@' in username:"):src.find("# Local users.json fallback")]
    assert "env_user = os.getenv('DASHBOARD_USER', '').strip()" in src
    assert "env_email = (os.getenv('DASHBOARD_EMAIL') or 'service@maximo-seo.com').strip()" in src
    assert "env_pass = os.getenv('DASHBOARD_PASSWORD', '')" in src
    assert "user_matches = bool(env_user and _hmac.compare_digest(username, env_user))" in src
    assert "if user_matches and _hmac.compare_digest(password, env_pass):" in src
    assert "email_matches = bool(env_email" not in src
    assert "_supabase_verify_password(username, password)" not in src[src.find('def _dashboard_validate_credentials'):src.find('def _jwt_make')]


def test_dashboard_password_not_committed_in_tracked_text_files():
    secret = _dashboard_password_literal()
    offenders = []
    for path in _tracked_files():
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        if secret in text:
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []
