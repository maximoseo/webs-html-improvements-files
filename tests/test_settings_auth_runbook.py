from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthRunbookTests(unittest.TestCase):
    def test_auth_health_panel_includes_mini_runbook_container(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-runbook"', html)
        self.assertIn('Auth incident mini-runbook', html)

    def test_auth_health_panel_has_js_builder_for_mini_runbook(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._buildSettingsAuthRunbook = function(data, warningState) {', html)
        self.assertIn('1. Refresh /api/auth/status and confirm whether the issue is drift, missing secrets, or a bad credential rotation.', html)
        self.assertIn('2. Test one real login via /api/auth/login before changing anything else.', html)
        self.assertIn("window._renderSettingsAuthRunbook('settings-auth-runbook',", html)


if __name__ == '__main__':
    unittest.main()
