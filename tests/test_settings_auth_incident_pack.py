from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthIncidentPackTests(unittest.TestCase):
    def test_auth_health_panel_includes_incident_pack_container_and_action(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-incident-pack"', html)
        self.assertIn('Auth incident handoff pack', html)
        self.assertIn('Copy Incident Pack', html)
        self.assertIn('onclick="copyAuthIncidentPack()"', html)

    def test_auth_health_panel_has_incident_pack_formatter_and_copy_flow(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._formatAuthIncidentPack = function(data, warningState, checklistItems, runbookItems) {', html)
        self.assertIn("lines.push('Severity: ' + (warningState.badge || 'Runtime checks'));", html)
        self.assertIn("lines.push('Immediate checklist:');", html)
        self.assertIn("lines.push('Incident runbook:');", html)
        self.assertIn('window.copyAuthIncidentPack = function() {', html)
        self.assertIn('window._formatAuthIncidentPack(payload || {}, window._lastSettingsAuthWarningState || warningState, checklistItems, runbookItems);', html)

    def test_auth_health_panel_renders_incident_pack_summary_from_live_data(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._renderSettingsAuthIncidentPack = function(targetId, warningState, checklistItems, runbookItems) {', html)
        self.assertIn("window._renderSettingsAuthIncidentPack('settings-auth-incident-pack', warningState, checklistItems, runbookItems);", html)
        self.assertIn('Ready to copy a safe operator handoff with live auth state, warning summary, checklist, and incident runbook.', html)


if __name__ == '__main__':
    unittest.main()
