from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class ProjectSortStabilityTests(unittest.TestCase):
    def test_sort_observer_ignores_self_reorder_to_prevent_open_blink(self):
        html = INDEX_HTML.read_text(encoding='utf-8')

        self.assertIn('PROJECT_SORT_SELF_MUTATION_GUARD_2026_04_26', html)
        self.assertIn('window.__projectSortApplying', html)
        self.assertRegex(
            html,
            r'if\s*\(\s*window\.__projectSortApplying\s*\)\s*return;',
            msg='Sort MutationObserver must ignore mutations caused by applySort itself',
        )
        self.assertRegex(
            html,
            r'var\s+orderChanged\s*=\s*sorted\.some\(function\(c,i\)\{\s*return\s+cards\[i\]\s*!==\s*c;\s*\}\);[\s\S]*?if\s*\(\s*!orderChanged\s*\)\s*return;',
            msg='applySort must not re-append cards when the order is already correct',
        )
        self.assertRegex(
            html,
            r'window\.__projectSortApplying\s*=\s*true;[\s\S]*?sorted\.forEach\(function\(c\)\{\s*grid\.appendChild\(c\);\s*\}\);[\s\S]*?window\.__projectSortApplying\s*=\s*false;',
            msg='applySort must guard grid.appendChild reorder so it does not recursively re-sort and blink cards',
        )


if __name__ == '__main__':
    unittest.main()
