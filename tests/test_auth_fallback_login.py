from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'server.py'


class AuthFallbackLoginTests(unittest.TestCase):
    def test_fallback_auth_guard_exists(self):
        src = SERVER.read_text(encoding='utf-8')
        self.assertIn('def _fallback_auth_enabled():', src)
        self.assertIn("DASHBOARD_DISABLE_FALLBACK_AUTH", src)
        self.assertIn("DASHBOARD_FALLBACK_PASSWORD", src)

    def test_fallback_admin_credentials_are_last_resort(self):
        src = SERVER.read_text(encoding='utf-8')
        self.assertIn("fallback_pass and _fallback_auth_enabled() and _hmac.compare_digest(username, 'admin') and _hmac.compare_digest(password, fallback_pass)", src)
        self.assertIn("matched = {'username': 'admin', 'role': 'admin', 'email': 'service@maximo-seo.com'}", src)


if __name__ == '__main__':
    unittest.main()
