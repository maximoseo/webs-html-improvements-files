from pathlib import Path
import json
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from unittest import mock

import server

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'

PORT = 0
BASE = ''


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class DashboardRefreshCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global PORT, BASE
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: False
        cls.httpd = ReusableHTTPServer(('127.0.0.1', 0), server.DashboardHandler)
        PORT = cls.httpd.server_port
        BASE = f'http://127.0.0.1:{PORT}'
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled

    def test_refresh_button_and_frontend_cache_clear_hooks_exist(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('DASHBOARD_REFRESH_CACHE_BUTTON_2026_04_26', html)
        self.assertIn('id="hdr-refresh-cache-btn"', html)
        self.assertIn('onclick="refreshDashboardHard(this)"', html)
        self.assertIn('window.refreshDashboardHard = refreshDashboardHard', html)
        self.assertIn('window.dashboardEnsureCsrf = _ensureCsrf', html)
        self.assertIn("const csrf=await window.dashboardEnsureCsrf()", html)
        self.assertIn("headers['X-CSRF-Token']=csrf", html)
        self.assertIn("localStorage.removeItem('dashboard_cache')", html)
        self.assertIn("sessionStorage.removeItem('dashboard_cache')", html)
        self.assertIn("fetch('/api/dashboard/clear-cache'", html)
        self.assertIn('loadDashboard({forceRefresh:true})', html)

    def test_backend_clear_cache_endpoint_reports_safe_targets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / 'data.json').write_text('{"tree": []}', encoding='utf-8')
            (root / 'outputs').mkdir()
            (root / 'n8n-workflow-map.json').write_text('{}', encoding='utf-8')
            with mock.patch.object(server, 'ROOT', root), \
                 mock.patch.object(server, 'MAP_FILE', root / 'n8n-workflow-map.json'):
                status, _, body = req('/api/dashboard/clear-cache', method='POST', headers={'Content-Type': 'application/json'}, data=b'{}')
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        self.assertIn('backend-cache-check', data['acknowledged'])
        self.assertIn('frontend', data['client_should_clear'])
        self.assertEqual(data['server_cache_control'], 'no-store')
        targets = {item['name']: item for item in data['targets']}
        self.assertIn('data.json', targets)
        self.assertIn('outputs', targets)
        self.assertIn('n8n-workflow-map.json', targets)
        self.assertTrue(targets['data.json']['exists'])
        self.assertTrue(targets['outputs']['exists'])


if __name__ == '__main__':
    unittest.main()
