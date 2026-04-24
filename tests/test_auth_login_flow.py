import json
import os
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

import server

PORT = 18111
BASE = f'http://127.0.0.1:{PORT}'


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class AuthLoginFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['DASHBOARD_USERS'] = 'admin:Maximo2025!'
        cls.httpd = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        os.environ.pop('DASHBOARD_USERS', None)

    def test_login_page_uses_canonical_auth_endpoints(self):
        status, _, body = req('/login')
        self.assertEqual(status, 200)
        self.assertIn('/api/auth/login', body)
        self.assertIn('/api/auth/request-reset', body)
        self.assertIn('/api/auth/reset', body)
        self.assertNotIn('/api/login', body)
        self.assertNotIn('/api/reset-password', body)
        self.assertNotIn('dashboard_token', body)

    def test_auth_login_sets_dash_auth_cookie_and_auth_me_accepts_it(self):
        payload = json.dumps({'username': 'admin', 'user': 'admin', 'password': 'Maximo2025!'}).encode()
        status, headers, body = req('/api/auth/login', method='POST', headers={'Content-Type': 'application/json'}, data=payload)
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        cookie = headers.get('Set-Cookie', '')
        self.assertIn('dash_auth=', cookie)

        cookie_header = cookie.split(';', 1)[0]
        me_status, _, me_body = req('/api/auth/me', headers={'Cookie': cookie_header})
        me_data = json.loads(me_body)
        self.assertEqual(me_status, 200)
        self.assertEqual(me_data['user'], 'admin')
        self.assertTrue(me_data['auth_enabled'])

    def test_early_dashboard_api_routes_require_auth(self):
        for path in ('/api/analytics', '/api/audit', '/api/views', '/api/file/raw?path=index.html'):
            status, _, body = req(path)
            self.assertEqual(status, 401, path)
            self.assertEqual(json.loads(body)['error'], 'auth_required')

    def test_password_reset_endpoints_exist_and_do_not_enumerate_users(self):
        payload = json.dumps({'username': 'admin', 'user': 'admin'}).encode()
        status, _, body = req('/api/auth/request-reset', method='POST', headers={'Content-Type': 'application/json'}, data=payload)
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertEqual(data, {'ok': True})

        bad_reset = json.dumps({'token': 'bad-token', 'new_password': 'NewPass123!'}).encode()
        status, _, body = req('/api/auth/reset', method='POST', headers={'Content-Type': 'application/json'}, data=bad_reset)
        data = json.loads(body)
        self.assertEqual(status, 400)
        self.assertEqual(data['error'], 'invalid_or_expired_token')


if __name__ == '__main__':
    unittest.main()
