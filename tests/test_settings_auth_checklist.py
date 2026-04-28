from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthChecklistTests(unittest.TestCase):
    def test_auth_health_panel_includes_operator_checklist_container(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-checklist"', html)
        self.assertIn('Auth operator checklist', html)

    def test_auth_health_panel_has_js_builder_for_operator_checklist(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._buildSettingsAuthChecklist = function(data, warningState) {', html)
        self.assertIn('Compare Render env values for DASHBOARD_USER / DASHBOARD_EMAIL against the operator identity shown in users.json.', html)
        self.assertIn('Validate a real login via /api/auth/login after any password or env rotation.', html)
        self.assertIn("window._renderSettingsAuthChecklist('settings-auth-checklist',", html)


if __name__ == '__main__':
    unittest.main()
