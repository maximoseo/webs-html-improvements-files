from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class ProjectHoverStabilityTests(unittest.TestCase):
    def test_project_card_hover_does_not_shift_layout(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        # Hover should highlight only (border/shadow/background), not move the card,
        # otherwise pointer can oscillate at edges and create visible blinking.
        self.assertRegex(
            html,
            r'\.project-card:hover\{[^}]*transform:\s*none',
            msg='Project card hover must keep transform:none for stable pointer hover',
        )

    def test_expanded_project_cards_disable_hover_repaint_flicker(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('PROJECT CARD HOVER FLICKER FIX', html)
        self.assertIn('id="project-card-hover-flicker-fix-2026-04-26"', html)
        fix_start = html.index('id="project-card-hover-flicker-fix-2026-04-26"')
        fix_css = html[fix_start:html.index('</style>', fix_start)]

        self.assertIn('.project-card.expanded,.project-card:hover,.project-card:focus-within{', fix_css)
        self.assertIn('content-visibility:visible !important;', fix_css)
        self.assertIn('contain-intrinsic-size:auto !important;', fix_css)
        self.assertIn('contain:layout paint !important;', fix_css)
        self.assertIn('will-change:auto !important;', fix_css)
        self.assertIn('transition:border-color 120ms', fix_css)
        self.assertIn('transform:none !important;', fix_css)
        self.assertIn('.project-card.expanded .card-body{transition:none !important;}', fix_css)

    def test_file_rows_inside_projects_disable_hover_blink_triggers(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('PROJECT FILE ROW HOVER BLINK FIX', html)
        self.assertIn('id="project-file-row-hover-blink-fix-2026-04-26"', html)
        fix_start = html.index('id="project-file-row-hover-blink-fix-2026-04-26"')
        fix_css = html[fix_start:html.index('</style>', fix_start)]

        self.assertIn('.project-card .file-row,.project-card .file-row:hover,.project-card .file-row:focus-within{', fix_css)
        self.assertIn('transform:none !important;', fix_css)
        self.assertIn('animation:none !important;', fix_css)
        self.assertIn('will-change:auto !important;', fix_css)
        self.assertIn('contain:paint !important;', fix_css)
        self.assertIn('backface-visibility:hidden !important;', fix_css)
        self.assertIn('transition:background-color 120ms cubic-bezier(.2,0,0,1),border-color 120ms cubic-bezier(.2,0,0,1) !important;', fix_css)
        self.assertIn('.project-card .file-row *{animation:none !important;}', fix_css)
        self.assertIn('.project-card .file-row .action-btn{transform:none !important;', fix_css)

    def test_file_rows_disable_all_nested_hover_motion_and_shadows(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('PROJECT FILE ROW HOVER BLINK FIX V2', html)
        self.assertIn('id="project-file-row-hover-blink-fix-v2-2026-04-26"', html)
        fix_start = html.index('id="project-file-row-hover-blink-fix-v2-2026-04-26"')
        fix_css = html[fix_start:html.index('</style>', fix_start)]

        self.assertIn('.project-card.expanded .file-row,.project-card.expanded .file-row:hover,.project-card.expanded .file-row:focus-within{', fix_css)
        self.assertIn('transition:none !important;', fix_css)
        self.assertIn('box-shadow:none !important;', fix_css)
        self.assertIn('filter:none !important;', fix_css)
        self.assertIn('backdrop-filter:none !important;', fix_css)
        self.assertIn('-webkit-backdrop-filter:none !important;', fix_css)
        self.assertIn('background:rgba(255,255,255,0.025) !important;', fix_css)
        self.assertIn('.project-card.expanded .file-row:hover{background:rgba(255,255,255,0.045) !important;', fix_css)
        self.assertIn('.project-card.expanded .file-row .action-btn,.project-card.expanded .file-row .action-btn:hover,.project-card.expanded .file-row .action-btn:focus-visible{', fix_css)
        self.assertIn('transition:none !important;', fix_css)
        self.assertIn('transform:none !important;', fix_css)
        self.assertIn('box-shadow:none !important;', fix_css)
        self.assertIn('.project-card.expanded .file-badge,.project-card.expanded .file-details,.project-card.expanded .file-name,.project-card.expanded .file-size{transition:none !important;', fix_css)

    def test_open_project_cards_disable_open_animation_blink_triggers(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('PROJECT OPEN BLINK FIX', html)
        self.assertIn('id="project-open-blink-fix-2026-04-26"', html)
        fix_start = html.index('id="project-open-blink-fix-2026-04-26"')
        fix_css = html[fix_start:html.index('</style>', fix_start)]

        self.assertIn('.project-card.expanded,.project-card.expanded:hover,.project-card.expanded:focus-within{', fix_css)
        self.assertIn('transition:none !important;', fix_css)
        self.assertIn('box-shadow:none !important;', fix_css)
        self.assertIn('filter:none !important;', fix_css)
        self.assertIn('backdrop-filter:none !important;', fix_css)
        self.assertIn('contain:layout paint style !important;', fix_css)
        self.assertIn('.project-card.expanded::before,.project-card.expanded::after{display:none !important;', fix_css)
        self.assertIn('.project-card.expanded .card-body{max-height:none !important;', fix_css)
        self.assertIn('overflow:visible !important;', fix_css)
        self.assertIn('.project-card.expanded .progress-bar,.project-card.expanded .toggle-icon,.project-card.expanded .preview-cta{transition:none !important;', fix_css)
        self.assertIn('PROJECT_OPEN_SCROLL_FIX_2026_04_26', html)
        self.assertIn("card.scrollIntoView({behavior:'auto',block:'nearest'})", html)


if __name__ == '__main__':
    unittest.main()
