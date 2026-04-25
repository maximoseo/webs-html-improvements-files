import json
import os
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path

import server

PORT = 18112
BASE = f'http://127.0.0.1:{PORT}'
REPO_ROOT = Path(server.__file__).resolve().parent
STARS_PATH = REPO_ROOT / 'data' / 'stars.json'
SETTINGS_PATH = REPO_ROOT / 'data' / 'settings.json'


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class ProjectQuickActionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: False
        cls.httpd = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled

    def tearDown(self):
        for path in (STARS_PATH, SETTINGS_PATH):
            if path.exists():
                path.unlink()

    def test_star_endpoint_accepts_json_body(self):
        payload = json.dumps({'domain': 'example.com', 'starred': True}).encode()
        status, _, body = req('/api/projects/star', method='POST', headers={'Content-Type': 'application/json'}, data=payload)
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        self.assertTrue(STARS_PATH.exists())
        saved = json.loads(STARS_PATH.read_text(encoding='utf-8'))
        self.assertTrue(saved.get('example.com'))

    def test_theme_endpoint_accepts_json_body(self):
        payload = json.dumps({'theme_color': 'blue'}).encode()
        status, _, body = req('/api/settings/theme', method='POST', headers={'Content-Type': 'application/json'}, data=payload)
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        saved = json.loads(SETTINGS_PATH.read_text(encoding='utf-8'))
        self.assertEqual(saved.get('theme_color'), 'blue')


if __name__ == '__main__':
    unittest.main()
