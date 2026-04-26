from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


class TaskManagerRedesignPromptTests(unittest.TestCase):
    def test_task_manager_tab_contains_embedded_redesign_prompt(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('TASK_MANAGER_REDESIGN_PROMPT_2026_04_26', html)
        self.assertIn('id="task-manager-redesign-prompt"', html)
        self.assertIn('Task Manager Tab Redesign Plan', html)
        self.assertIn('professional, full-featured task tracking system', html)
        self.assertIn('**Multiple views** — List, Kanban board, Calendar, Timeline', html)
        self.assertIn('Supabase Schema', html)
        self.assertIn('Obsidian Vault Sync', html)
        self.assertIn('GET    /api/tasks/projects', html)
        self.assertIn('Phase 1: Core Data &amp; List View', html)

    def test_prompt_panel_has_copy_and_download_actions(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('copyTaskManagerRedesignPrompt()', html)
        self.assertIn('downloadTaskManagerRedesignPrompt()', html)
        self.assertRegex(html, r'function\s+copyTaskManagerRedesignPrompt\s*\(')
        self.assertRegex(html, r'function\s+downloadTaskManagerRedesignPrompt\s*\(')


if __name__ == '__main__':
    unittest.main()
