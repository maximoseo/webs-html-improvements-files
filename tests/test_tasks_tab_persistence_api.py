from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'
SERVER_PY = ROOT / 'server.py'


class TasksTabPersistenceApiTests(unittest.TestCase):
    def test_tasks_frontend_uses_backend_api_not_direct_supabase(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn("fetch('/api/tasks'", html)
        self.assertNotIn("SUPABASE_URL = 'https://wtpczvyupmavzrxisvcm.supabase.co'", html)

    def test_server_exposes_tasks_get_and_post_endpoints(self):
        src = SERVER_PY.read_text(encoding='utf-8')
        self.assertIn("if parsed.path == '/api/tasks':", src)


if __name__ == '__main__':
    unittest.main()
