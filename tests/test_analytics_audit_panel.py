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

    def test_analytics_audit_panel_has_toolbar_filters_copy_and_detail_region(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="analytics-audit-toolbar"', html)
        self.assertIn('id="analytics-audit-action-filter"', html)
        self.assertIn('id="analytics-audit-search"', html)
        self.assertIn('id="analytics-audit-copy"', html)
        self.assertIn('id="analytics-audit-detail"', html)

    def test_analytics_audit_panel_has_filtering_detail_and_copy_helpers(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('function applyAnalyticsAuditFilters(events)', html)
        self.assertIn('function showAnalyticsAuditDetail(index)', html)
        self.assertIn('function copyAnalyticsAuditSummary()', html)
        self.assertIn('analyticsAuditState = {', html)

    def test_analytics_audit_panel_has_loading_and_filtered_empty_states(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('analytics-panel-loading', html)
        self.assertIn('analytics-panel-empty', html)
        self.assertIn('No matching audit events.', html)
        self.assertIn('Select an audit event to inspect its details.', html)


if __name__ == '__main__':
    unittest.main()
