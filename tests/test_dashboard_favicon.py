from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'
LOGIN_HTML = ROOT / 'login-page.html'


class DashboardFaviconTests(unittest.TestCase):
    def assert_purple_logo_favicon(self, html):
        self.assertIn('DASHBOARD PURPLE LOGO FAVICON (2026-04-26)', html)
        self.assertIn('rel="icon"', html)
        self.assertIn('data:image/svg+xml', html)

        match = re.search(r'<link[^>]+rel="icon"[^>]+href="([^"]+)"', html)
        self.assertIsNotNone(match)
        favicon_href = unquote(match.group(1))

        self.assertIn('viewBox="0 0 100 100"', favicon_href)
        self.assertIn('linearGradient id="purpleLogoGradient"', favicon_href)
        self.assertIn('#7170ff', favicon_href)
        self.assertIn('#5e6ad2', favicon_href)
        self.assertIn('stroke="white"', favicon_href)
        self.assertIn('stroke-width="7"', favicon_href)
        self.assertNotIn('&#9672;', favicon_href)

    def test_main_dashboard_favicon_uses_purple_logo_layers_icon(self):
        self.assert_purple_logo_favicon(INDEX_HTML.read_text(encoding='utf-8'))

    def test_login_page_favicon_uses_same_purple_logo_layers_icon(self):
        self.assert_purple_logo_favicon(LOGIN_HTML.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
