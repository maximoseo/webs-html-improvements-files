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

import kwr_backend
import server

PORT = 0
BASE = ''


class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


class KwrPathSafetyTests(unittest.TestCase):
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

    def test_build_excel_rejects_traversal_cached_file_outside_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outputs = os.path.join(tmpdir, 'outputs')
            outside = os.path.join(tmpdir, 'outside')
            os.makedirs(outputs, exist_ok=True)
            os.makedirs(outside, exist_ok=True)
            with open(os.path.join(outside, 'file.xlsx'), 'wb') as fh:
                fh.write(b'outside-cache-must-not-be-readable')

            with mock.patch.object(kwr_backend, 'OUTPUTS_DIR', outputs):
                data, ws_name, err = kwr_backend.build_excel('../outside')

        self.assertIsNone(data)
        self.assertIsNone(ws_name)
        self.assertIn('invalid run_id', err or '')

    def test_delete_report_rejects_traversal_and_preserves_parent_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outputs = os.path.join(tmpdir, 'outputs')
            os.makedirs(outputs, exist_ok=True)
            sentinel = os.path.join(tmpdir, 'sentinel.txt')
            with open(sentinel, 'w', encoding='utf-8') as fh:
                fh.write('do not delete parent')

            with mock.patch.object(kwr_backend, 'OUTPUTS_DIR', outputs):
                ok, err = kwr_backend.delete_report('..')

            self.assertFalse(ok)
            self.assertIn('invalid run_id', err or '')
            self.assertTrue(os.path.exists(sentinel), 'delete_report must not delete outside OUTPUTS_DIR')

    def test_delete_report_removes_valid_report_inside_outputs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            outputs = os.path.join(tmpdir, 'outputs')
            run_dir = os.path.join(outputs, 'safe-run-123')
            os.makedirs(run_dir, exist_ok=True)
            with open(os.path.join(run_dir, 'meta.json'), 'w', encoding='utf-8') as fh:
                fh.write('{}')

            with mock.patch.object(kwr_backend, 'OUTPUTS_DIR', outputs):
                ok, err = kwr_backend.delete_report('safe-run-123')

            self.assertTrue(ok, err)
            self.assertFalse(os.path.exists(run_dir))

    def test_flat_download_rejects_invalid_slug_before_file_lookup(self):
        status, _, body = req('/api/kwr/download/flat:..')
        data = json.loads(body.decode('utf-8', 'replace'))
        self.assertEqual(status, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(data['error'], 'invalid flat report id')

    def test_live_download_rejects_encoded_traversal_run_id_as_bad_request(self):
        status, _, body = req('/api/kwr/download/%2e%2e')
        data = json.loads(body.decode('utf-8', 'replace'))
        self.assertEqual(status, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(data['error'], 'invalid run_id')

    def test_report_delete_rejects_encoded_traversal_run_id_as_bad_request(self):
        status, _, body = req('/api/kwr/reports/%2e%2e', method='DELETE')
        data = json.loads(body.decode('utf-8', 'replace'))
        self.assertEqual(status, 400)
        self.assertFalse(data['ok'])
        self.assertEqual(data['error'], 'invalid run_id')

    def test_flat_download_valid_report_still_works(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_server = os.path.join(tmpdir, 'server.py')
            with open(fake_server, 'w', encoding='utf-8') as fh:
                fh.write('# fake server path')
            outdir = os.path.join(tmpdir, 'outputs')
            os.makedirs(outdir, exist_ok=True)
            with open(os.path.join(outdir, 'kwr_demo.xlsx'), 'wb') as fh:
                fh.write(b'valid-flat-report')

            with mock.patch.object(server, '__file__', fake_server):
                status, headers, body = req('/api/kwr/download/flat:demo')

        self.assertEqual(status, 200)
        self.assertEqual(body, b'valid-flat-report')
        self.assertIn('spreadsheetml.sheet', headers.get('Content-Type', ''))


if __name__ == '__main__':
    unittest.main()
