from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthHandoffCardTests(unittest.TestCase):
    def test_auth_health_panel_includes_handoff_card_container_and_action(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="settings-auth-handoff-card"', html)
        self.assertIn('Auth operator handoff card', html)
        self.assertIn('Copy Handoff Card', html)
        self.assertIn('onclick="copyAuthOperatorHandoffCard()"', html)

    def test_auth_health_panel_has_handoff_card_formatter_copy_flow_and_history_tracking(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._formatAuthOperatorHandoffCard = function(data, warningState, history) {', html)
        self.assertIn("lines.push('Latest note: ' + ((history.note || '').trim() || 'No note saved'));", html)
        self.assertIn("history.lastHandoffCardCopyAt = new Date().toISOString();", html)
        self.assertIn('window.copyAuthOperatorHandoffCard = function() {', html)
        self.assertGreaterEqual(html.count("window._recordSettingsAuthIncidentAction('handoff-card-copy');"), 2)
        self.assertGreaterEqual(html.count("window._renderSettingsAuthIncidentHistory('settings-auth-incident-history', updatedHistory);"), 6)

    def test_auth_health_panel_renders_handoff_card_from_live_state(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('window._renderSettingsAuthOperatorHandoffCard = function(targetId, data, warningState, history) {', html)
        self.assertIn("window._renderSettingsAuthOperatorHandoffCard('settings-auth-handoff-card', data, warningState, history);", html)
        self.assertIn('Ready to export a short operator handoff using live auth state, recent actions, and the latest note.', html)
        self.assertIn('Last handoff card copy:', html)


if __name__ == '__main__':
    unittest.main()
