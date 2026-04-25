from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthIncidentHistoryTests(unittest.TestCase):
    def test_auth_health_panel_includes_incident_history_container_and_note_field(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-incident-history"', html)
        self.assertIn('Auth incident history', html)
        self.assertIn('id="settings-auth-history-note"', html)
        self.assertIn('Last action note', html)
        self.assertIn('onclick="saveAuthIncidentHistoryNote()"', html)

    def test_auth_health_panel_has_history_state_and_recorder_functions(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn("window._settingsAuthHistoryStorageKey = 'settings.auth.incidentHistory';", html)
        self.assertIn('window._getSettingsAuthIncidentHistory = function() {', html)
        self.assertIn('window._recordSettingsAuthIncidentAction = function(actionType, detail) {', html)
        self.assertIn("history.lastRefreshAt = new Date().toISOString();", html)
        self.assertIn("history.lastDiagnosticsCopyAt = new Date().toISOString();", html)
        self.assertIn("history.lastIncidentPackCopyAt = new Date().toISOString();", html)
        self.assertGreaterEqual(html.count("window._recordSettingsAuthIncidentAction('diagnostics-copy');"), 2)
        self.assertGreaterEqual(html.count("window._recordSettingsAuthIncidentAction('incident-pack-copy');"), 2)
        self.assertIn('window.saveAuthIncidentHistoryNote = function() {', html)

    def test_auth_health_panel_renders_incident_history_from_live_state(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._renderSettingsAuthIncidentHistory = function(targetId, history) {', html)
        self.assertIn("window._renderSettingsAuthIncidentHistory('settings-auth-incident-history', history);", html)
        self.assertIn('Last refresh:', html)
        self.assertIn('Last diagnostics copy:', html)
        self.assertIn('Last incident pack copy:', html)
        self.assertIn('No auth incident note saved yet.', html)


if __name__ == '__main__':
    unittest.main()
