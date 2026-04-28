from pathlib import Path
import json
import os
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.parse
import urllib.request
from http.server import HTTPServer

import server

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'
PORT = 0
BASE = ''


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def req(path, method='GET', data=None, headers=None):
    body = None
    h = headers or {}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        h = {'Content-Type': 'application/json', **h}
    request = urllib.request.Request(BASE + path, method=method, headers=h, data=body)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class ProductivityBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global PORT, BASE
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        cls._orig_prod_file = getattr(server, 'PRODUCTIVITY_HUB_FILE', None)
        cls._orig_template_file = server.TEMPLATE_IMPROVEMENTS_FILE
        server._dashboard_auth_enabled = lambda: False
        cls.tmpdir = tempfile.TemporaryDirectory()
        server.TEMPLATE_IMPROVEMENTS_FILE = Path(cls.tmpdir.name) / 'template_improvements.json'
        if hasattr(server, 'PRODUCTIVITY_HUB_FILE'):
            server.PRODUCTIVITY_HUB_FILE = Path(cls.tmpdir.name) / 'productivity_hub.json'
        cls.httpd = ReusableHTTPServer(('127.0.0.1', 0), server.DashboardHandler)
        PORT = cls.httpd.server_port
        BASE = f'http://127.0.0.1:{PORT}'
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled
        server.TEMPLATE_IMPROVEMENTS_FILE = cls._orig_template_file
        if cls._orig_prod_file is not None and hasattr(server, 'PRODUCTIVITY_HUB_FILE'):
            server.PRODUCTIVITY_HUB_FILE = cls._orig_prod_file
        cls.tmpdir.cleanup()

    def test_productivity_summary_endpoint_returns_15_feature_statuses(self):
        status, _, body = req('/api/productivity/summary')
        self.assertEqual(status, 200, body)
        data = json.loads(body)
        self.assertTrue(data['ok'])
        self.assertEqual(len(data['features']), 15)
        self.assertIn('generated_at', data)
        slugs = {row['slug'] for row in data['features']}
        self.assertIn('global-search', slugs)
        self.assertIn('cost-tracker', slugs)
        self.assertIn('scheduled-runs', slugs)
        self.assertIn('safety', data)
        self.assertTrue(data['safety']['additive_only'])
        self.assertTrue(data['safety']['no_n8n_workflow_modification'])

    def test_productivity_notifications_are_persisted_and_listed(self):
        payload = {'type': 'warning', 'title': 'Smoke alert', 'message': 'Budget threshold preview', 'link': '#page-productivity-hub'}
        status, _, body = req('/api/productivity/notifications', method='POST', data=payload)
        self.assertEqual(status, 200, body)
        created = json.loads(body)['notification']
        self.assertEqual(created['title'], 'Smoke alert')
        status, _, body = req('/api/productivity/notifications')
        self.assertEqual(status, 200, body)
        rows = json.loads(body)['notifications']
        self.assertTrue(any(row['id'] == created['id'] for row in rows))

    def test_productivity_audit_endpoint_records_and_searches_events(self):
        status, _, body = req('/api/productivity/audit', method='POST', data={'message': 'Instruction updated', 'entity_type': 'domain', 'entity_id': 'example.com'})
        self.assertEqual(status, 200, body)
        event = json.loads(body)['event']
        self.assertEqual(event['message'], 'Instruction updated')
        status, _, body = req('/api/productivity/search?q=Instruction')
        self.assertEqual(status, 200, body)
        results = json.loads(body)['results']
        self.assertTrue(any(row['type'] == 'audit' and row['title'] == 'Instruction updated' for row in results))

    def test_productivity_routes_are_auth_gated_when_auth_enabled(self):
        orig = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: True
        try:
            for path in ('/api/productivity/summary', '/api/productivity/notifications', '/api/productivity/audit', '/api/productivity/search?q=x'):
                status, _, body = req(path)
                self.assertEqual(status, 401, f'{path}: {body}')
        finally:
            server._dashboard_auth_enabled = orig

    def test_productivity_ui_fetches_backend_with_fallback(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('PRODUCTIVITY_HUB_BACKEND_SYNC_2026_04_27', html)
        self.assertIn("mfApi('/api/productivity/summary'", html)
        self.assertIn("mfApi('/api/productivity/notifications'", html)
        self.assertIn("mfApi('/api/productivity/audit'", html)
        self.assertIn("mfApi('/api/productivity/search?q='", html)
        self.assertIn('mfBackendAvailable', html)
        self.assertIn('mfRenderBackendSummary', html)


if __name__ == '__main__':
    unittest.main()
