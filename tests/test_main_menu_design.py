from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class MainMenuDesignTests(unittest.TestCase):
    def test_main_menu_has_premium_shell_and_accessible_tabs(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('MAIN MENU FINAL OVERRIDE', html)
        self.assertIn('id="main-menu-final-override-2026-04-25"', html)
        self.assertIn('class="fixer-tab-nav main-menu"', html)
        self.assertIn('aria-orientation="horizontal"', html)
        self.assertIn('data-menu-label="Main menu"', html)

        # The menu override must be after the late operations refresh layer;
        # otherwise the dashboard looks unchanged in production.
        self.assertGreater(html.rfind('MAIN MENU FINAL OVERRIDE'), html.rfind('dashboard-ops-refresh-2026-04-24'))

        # Visual shell: labeled glass container, visible selected state, and hover affordance.
        self.assertRegex(html, r'\.header\s+\.fixer-tab-nav\.main-menu\s*\{[^}]*border-radius:\s*18px')
        self.assertRegex(html, r'\.header\s+\.fixer-tab-nav\.main-menu\s*\{[^}]*box-shadow:')
        self.assertIn("content:'Main menu'", html)
        self.assertRegex(html, r'\.header\s+\.main-menu\s+\.fixer-tab-btn\.active,[^{]+\{[^}]*linear-gradient')
        self.assertRegex(html, r'\.header\s+\.main-menu\s+\.fixer-tab-btn:hover')

    def test_main_menu_responsive_rules_preserve_mobile_drawer(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('@media (max-width:1180px)', html)
        self.assertIn('.header .fixer-tab-nav.main-menu{overflow-x:auto !important;', html)
        self.assertIn('@media (max-width:820px)', html)
        self.assertIn('.header .fixer-tab-nav{ display:none !important; }', html)

    def test_desktop_main_menu_has_safe_top_spacing(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('DESKTOP MAIN MENU SAFE TOP SPACING', html)
        self.assertIn('id="main-menu-safe-top-spacing-2026-04-26"', html)
        safe_spacing_start = html.index('id="main-menu-safe-top-spacing-2026-04-26"')
        safe_spacing = html[safe_spacing_start:html.index('</style>', safe_spacing_start)]
        self.assertIn('@media (min-width:821px){', safe_spacing)
        self.assertIn('header.header,.header{top:12px !important;', safe_spacing)
        self.assertIn('left:16px !important;', safe_spacing)
        self.assertIn('right:16px !important;', safe_spacing)
        self.assertIn('body{padding-top:108px !important;}', safe_spacing)
        self.assertIn('.header .fixer-tab-nav.main-menu{transform:none !important;', safe_spacing)
        self.assertIn('@media (max-width:820px){.header{top:0 !important;left:0 !important;right:0 !important;border-radius:0 !important;}.header .fixer-tab-nav.main-menu{display:none !important;}}', safe_spacing)


if __name__ == '__main__':
    unittest.main()
