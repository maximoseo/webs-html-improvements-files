from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class KwResearchRedesignPromptTests(unittest.TestCase):
    def test_kw_research_tab_contains_embedded_redesign_prompt(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('KW_RESEARCH_REDESIGN_PROMPT_2026_04_26', html)
        self.assertIn('id="kw-research-redesign-prompt"', html)
        self.assertIn('KW Research Page Redesign Plan', html)
        self.assertIn('Domain dropdown', html)
        self.assertIn('Report history under the form', html)
        self.assertIn('CREATE TABLE domains', html)
        self.assertIn('Obsidian Vault Sync', html)
        self.assertIn('GET    /api/kw/domains', html)
        self.assertIn('Phase 1: Data Layer', html)

    def test_kw_prompt_panel_has_copy_and_download_actions(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('copyKwResearchRedesignPrompt()', html)
        self.assertIn('downloadKwResearchRedesignPrompt()', html)
        self.assertRegex(html, r'function\s+copyKwResearchRedesignPrompt\s*\(')
        self.assertRegex(html, r'function\s+downloadKwResearchRedesignPrompt\s*\(')


if __name__ == '__main__':
    unittest.main()
