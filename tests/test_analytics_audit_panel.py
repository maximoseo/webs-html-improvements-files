from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class AnalyticsAuditPanelTests(unittest.TestCase):
    def test_analytics_page_includes_recent_audit_events_panel(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('Recent Audit Events', html)
        self.assertIn('analytics-audit-list', html)
        self.assertIn('analytics-audit-summary', html)

    def test_analytics_init_loads_audit_events_from_api(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn("fetch('/api/audit?limit=25')", html)
        self.assertIn('function renderAnalyticsAuditEvents(events)', html)
        self.assertIn('analytics-audit-list', html)
        self.assertIn('analytics-audit-summary', html)


if __name__ == '__main__':
    unittest.main()
