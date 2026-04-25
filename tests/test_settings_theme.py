import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from unittest import mock

import server


class SettingsThemeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._old_auth = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: False
        cls.httpd = HTTPServer(('127.0.0.1', 0), server.DashboardHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=5)
        server._dashboard_auth_enabled = cls._old_auth

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.base_patch = mock.patch.object(server, '__file__', str(Path(self.tmpdir.name) / 'server.py'))
        self.base_patch.start()
        self.addCleanup(self.base_patch.stop)

    def _request(self, path, method='GET', body=None, headers=None):
        req = urllib.request.Request(
            f'http://127.0.0.1:{self.port}{path}',
            data=(json.dumps(body).encode('utf-8') if body is not None else None),
            method=method,
            headers=headers or ({'Content-Type': 'application/json'} if body is not None else {}),
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as exc:
            return exc.code, json.loads(exc.read().decode('utf-8'))

    def test_theme_color_default_and_persisted(self):
        status, body = self._request('/api/settings')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('theme_color'), 'purple')

        status, csrf = self._request('/api/csrf')
        self.assertEqual(status, 200)
        token = csrf.get('token')
        self.assertTrue(token)

        status, body = self._request(
            '/api/settings/theme',
            method='POST',
            body={'theme_color': 'blue'},
            headers={'Content-Type': 'application/json', 'X-CSRF-Token': token},
        )
        self.assertEqual(status, 200)
        self.assertTrue(body.get('ok'))
        self.assertEqual(body.get('theme_color'), 'blue')

        status, body = self._request('/api/settings')
        self.assertEqual(status, 200)
        self.assertEqual(body.get('theme_color'), 'blue')


if __name__ == '__main__':
    unittest.main()
