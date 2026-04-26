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


if __name__ == '__main__':
    unittest.main()
