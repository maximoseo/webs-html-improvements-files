from pathlib import Path
import re
import unittest
from unittest import mock

import server

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / 'server.py'
GITIGNORE = ROOT / '.gitignore'


class N8NReadOnlySafetyTests(unittest.TestCase):
    def test_no_embedded_n8n_api_jwt_fallback_in_server(self):
        source = SERVER.read_text(encoding='utf-8')
        self.assertNotIn('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9', source)
        self.assertNotRegex(source, r"os\.getenv\('N8N_API_KEY'\)\s+or\s+['\"]")

    def test_n8n_headers_require_environment_key(self):
        with mock.patch.dict('os.environ', {}, clear=True):
            self.assertIsNone(server.n8n_headers())

    def test_n8n_secret_files_are_gitignored(self):
        ignore = GITIGNORE.read_text(encoding='utf-8')
        self.assertIn('config/.env.n8n', ignore)
        self.assertIn('*.secret', ignore)

    def test_server_never_writes_to_n8n_workflow_api(self):
        source = SERVER.read_text(encoding='utf-8')
        unsafe_patterns = [
            r"api/v1/workflows/\{[^}]+\}[^\n]+method\s*=\s*['\"]PUT['\"]",
            r"api/v1/workflows/\{[^}]+\}[^\n]+method\s*=\s*['\"]POST['\"]",
            r"api/v1/workflows/\{[^}]+\}[^\n]+method\s*=\s*['\"]PATCH['\"]",
            r"api/v1/workflows/\{[^}]+\}[^\n]+method\s*=\s*['\"]DELETE['\"]",
            r"/api/v1/workflows/[^'\"]*/activate",
            r"/api/v1/workflows/[^'\"]*/deactivate",
            r"method\s*=\s*['\"]PUT['\"][^\n]+api/v1/workflows",
            r"method\s*=\s*['\"]POST['\"][^\n]+api/v1/workflows",
            r"method\s*=\s*['\"]PATCH['\"][^\n]+api/v1/workflows",
            r"method\s*=\s*['\"]DELETE['\"][^\n]+api/v1/workflows",
        ]
        for pattern in unsafe_patterns:
            self.assertIsNone(re.search(pattern, source), msg=f'Unsafe n8n write pattern found: {pattern}')

    def test_fetch_json_blocks_non_get_to_n8n_base_url(self):
        with self.assertRaises(ValueError):
            server.fetch_json('https://websiseo.app.n8n.cloud/api/v1/workflows/abc', method='PUT', body={'name': 'bad'})


if __name__ == '__main__':
    unittest.main()
