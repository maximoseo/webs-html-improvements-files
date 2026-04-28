from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class AnalyticsHeaderCollisionTests(unittest.TestCase):
    def test_analytics_table_header_class_does_not_reuse_global_header_class(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('analytics-proj-row-head', html)
        # Runtime rendering should use the dedicated analytics header class.
        self.assertIn('class="analytics-proj-row analytics-proj-row-head"', html)

    def test_legacy_analytics_header_class_is_safely_neutralized(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        # Safety net: if an old bundle injects `.analytics-proj-row.header`,
        # it must be forced static so it can never overlap the top navigation.
        self.assertIn('.analytics-proj-row.header{position:static !important;', html)


if __name__ == '__main__':
    unittest.main()
