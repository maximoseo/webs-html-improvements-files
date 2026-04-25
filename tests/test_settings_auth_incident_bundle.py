from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthIncidentBundleTests(unittest.TestCase):
    def test_auth_health_panel_includes_bundle_container_and_action(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-incident-bundle"', html)
        self.assertIn('Auth incident bundle', html)
        self.assertIn('Copy Incident Bundle', html)
        self.assertIn('onclick="copyAuthIncidentBundle()"', html)

    def test_auth_health_panel_has_bundle_formatter_copy_flow_and_history_tracking(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._formatAuthIncidentBundle = function(data, warningState, history, checklistItems, runbookItems) {', html)
        self.assertIn("lines.push('=== Diagnostics ===');", html)
        self.assertIn("lines.push('=== Incident pack ===');", html)
        self.assertIn("lines.push('=== Operator handoff card ===');", html)
        self.assertIn("lines.push('=== Latest note/history ===');", html)
        self.assertIn("history.lastIncidentBundleCopyAt = new Date().toISOString();", html)
        self.assertIn('window.copyAuthIncidentBundle = function() {', html)
        self.assertGreaterEqual(html.count("window._recordSettingsAuthIncidentAction('incident-bundle-copy');"), 2)

    def test_auth_health_panel_renders_bundle_panel_from_live_state(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._renderSettingsAuthIncidentBundle = function(targetId, warningState, history) {', html)
        self.assertIn("window._renderSettingsAuthIncidentBundle('settings-auth-incident-bundle', warningState, history);", html)
        self.assertIn('Ready to export diagnostics, incident pack, handoff card, and latest note/history in one copy action.', html)
        self.assertIn('Last incident bundle copy:', html)


if __name__ == '__main__':
    unittest.main()
