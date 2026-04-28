from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class TourOverlayClickthroughTests(unittest.TestCase):
    def test_tour_backdrop_does_not_block_project_card_clicks(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        # Backdrop may dim the page, but must not intercept pointer events.
        self.assertRegex(
            html,
            r"#tour-backdrop\{[^}]*pointer-events:\s*none",
            msg='Tour backdrop should be click-through so project cards remain clickable',
        )

        # Tooltip remains visible, while only its controls are interactive.
        self.assertRegex(
            html,
            r"\.tour-tooltip\{[^}]*pointer-events:\s*none",
            msg='Tour tooltip shell should not block clicks outside its buttons',
        )
        self.assertRegex(
            html,
            r"\.tour-tooltip\s+button\{[^}]*pointer-events:\s*auto",
            msg='Tour tooltip buttons should keep pointer-events enabled',
        )


if __name__ == '__main__':
    unittest.main()
