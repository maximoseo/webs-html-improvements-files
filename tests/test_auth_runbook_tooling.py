from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_auth_doctor_does_not_spoof_proxy_headers_by_default():
    src = (ROOT / 'scripts' / 'auth_doctor.py').read_text()
    assert '--spoof-forwarded-ip' in src
    assert 'if args.spoof_forwarded_ip:' in src
    primary_block = src.split('primary_headers = {', 1)[1].split('if args.spoof_forwarded_ip:', 1)[0]
    assert 'CF-Connecting-IP' not in primary_block
    assert 'X-Forwarded-For' not in primary_block
    assert 'X-Real-IP' not in primary_block


def test_auth_doctor_rate_limit_probe_is_opt_in():
    src = (ROOT / 'scripts' / 'auth_doctor.py').read_text()
    assert '--include-rate-limit' in src
    assert 'if args.include_rate_limit:' in src
    assert 'rate-limit probe disabled by default' in src


def test_auth_doctor_returns_nonzero_when_credentialed_auth_fails():
    src = (ROOT / 'scripts' / 'auth_doctor.py').read_text()
    assert 'if args.password:' in src
    assert 'return 2' in src
    assert 'primary.get("set_cookie")' in src
    assert 'me_after.get("user")' in src


def test_full_prod_runbook_has_no_forwarded_ip_default_and_no_admin_fallback():
    src = (ROOT / 'scripts' / 'auth-runbook.sh').read_text()
    full_prod = src.split('full-prod)', 1)[1].split(';;', 1)[0]
    assert '--forwarded-ip' not in full_prod
    assert 'TEST_ADMIN_USER or TEST_ADMIN_EMAIL is required for full-prod' in src
    assert 'DEFAULT_USER="${TEST_ADMIN_USER:-}"' in src
    assert 'DEFAULT_USER="${TEST_ADMIN_USER:-admin}"' not in src
