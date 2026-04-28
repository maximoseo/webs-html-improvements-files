from pathlib import Path
import json
import os
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


class SafeUiApiFixesTests(unittest.TestCase):
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

    def test_safe_ui_marker_and_responsive_overflow_guards_exist(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('SAFE_UI_API_FIXES_2026_04_26', html)
        self.assertIn('overflow-x:clip', html)
        self.assertIn('.mobile-drawer:not(.open)', html)
        self.assertIn('left:100% !important', html)
        self.assertIn('@media(max-width:900px)', html)
        self.assertIn('.deploy-status-panel{display:none !important;}', html)

    def test_tour_skip_persists_and_tooltip_is_clamped(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('setTourDone()', html)
        self.assertIn("if (act === 'skip'){ end(true); }", html)
        self.assertIn("type=\"button\" data-act=\"skip\"", html)
        self.assertIn('max-height:calc(100vh - ', html)
        self.assertIn('var availW = Math.max(1, window.innerWidth - margin * 2)', html)
        self.assertIn('Math.max(margin, Math.min(window.innerWidth - ttW - margin, left))', html)
        self.assertIn('Math.max(0, Math.min(window.innerWidth - spotLeft - 8', html)

    def test_flat_kwr_status_returns_completed_for_existing_flat_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_server = os.path.join(tmpdir, 'server.py')
            open(fake_server, 'w', encoding='utf-8').write('# fake')
            outdir = os.path.join(tmpdir, 'outputs')
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, 'kwr_demo.xlsx'), 'wb') as fh:
                fh.write(b'not a real workbook, just status artifact')
            with mock.patch.object(server, '__file__', fake_server):
                status, _, body = req('/api/kwr/status?run_id=flat:demo')
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        self.assertEqual(data['run_id'], 'flat:demo')
        self.assertEqual(data['status'], 'completed')
        self.assertEqual(data['progress'], 100)
        self.assertEqual(data['flat_file'], 'kwr_demo.xlsx')


    def test_flat_kwr_status_rejects_invalid_flat_report_id(self):
        status, _, body = req('/api/kwr/status?run_id=flat:../server')
        data = json.loads(body)
        self.assertEqual(status, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(data['error'], 'invalid flat report id')

    def test_flat_kwr_status_missing_returns_flat_specific_404(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_server = os.path.join(tmpdir, 'server.py')
            open(fake_server, 'w', encoding='utf-8').write('# fake')
            os.makedirs(os.path.join(tmpdir, 'outputs'), exist_ok=True)
            with mock.patch.object(server, '__file__', fake_server):
                status, _, body = req('/api/kwr/status?run_id=flat:missing')
        data = json.loads(body)
        self.assertEqual(status, 404)
        self.assertFalse(data['ok'])
        self.assertEqual(data['error'], 'flat report not found')


if __name__ == '__main__':
    unittest.main()
