from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class HeaderSafeTopSpacingTests(unittest.TestCase):
    def test_latest_header_safe_spacing_uses_dynamic_measured_offset(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="main-menu-safe-top-spacing-v2-2026-04-26"', html)
        self.assertIn('max(var(--header-safe-offset, 0px), calc(var(--header-h, 80px) + 36px))', html)
        self.assertIn('ResizeObserver(syncHeaderHeight)', html)
        self.assertIn('scroll-padding-top: var(--page-safe-top', html)

    def test_no_later_static_body_padding_can_override_safe_header_offset(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        marker = 'id="main-menu-safe-top-spacing-v2-2026-04-26"'
        self.assertIn(marker, html)
        tail = html.split(marker, 1)[1]
        self.assertNotRegex(tail, re.compile(r'body\s*\{[^}]*padding-top\s*:\s*\d+px\s*!important', re.S))


if __name__ == '__main__':
    unittest.main()
