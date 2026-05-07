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
        os.environ['DASHBOARD_USERS'] = 'admin:HermesTestPassword123!'
        cls.httpd = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        os.environ.pop('DASHBOARD_USERS', None)

    def test_login_page_uses_server_auth_username_only_endpoint(self):
        status, _, body = req('/login')
        self.assertEqual(status, 200)
        self.assertIn('DASHBOARD_LOGIN_SERVER_AUTH_2026_05_07', body)
        self.assertIn("const LOGIN_ENDPOINT = '/api/auth/login';", body)
        self.assertIn("JSON.stringify({ user: identifier, password: password })", body)
        self.assertIn('placeholder="maximoseo"', body)
        self.assertNotIn("./auth/supabase-client.js", body)
        self.assertNotIn('/api/auth/supabase-sync', body)
        self.assertNotIn('/api/login', body)
        self.assertNotIn('/api/reset-password', body)

    def test_auth_login_sets_dash_auth_cookie_and_auth_me_accepts_it(self):
        payload = json.dumps({'username': 'admin', 'user': 'admin', 'password': 'HermesTestPassword123!'}).encode()
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

    def test_cookie_session_can_use_jwt_secret_in_production(self):
        old = {name: os.environ.get(name) for name in ('RENDER', 'DASHBOARD_AUTH_SECRET', 'DASHBOARD_JWT_SECRET', 'DASHBOARD_USERS')}
        try:
            os.environ['RENDER'] = 'true'
            os.environ['DASHBOARD_JWT_SECRET'] = 'test-production-jwt-secret'
            os.environ.pop('DASHBOARD_AUTH_SECRET', None)
            os.environ.pop('DASHBOARD_USERS', None)
            token = server._stage8_make_token('admin', 'admin')
            session = server._stage8_verify_session(token)
            self.assertEqual(session['username'], 'admin')
            self.assertEqual(session['role'], 'admin')
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

    def test_break_glass_login_requires_username_not_service_email_alias(self):
        keys = ('DASHBOARD_USER', 'DASHBOARD_PASSWORD', 'DASHBOARD_EMAIL', 'SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY')
        old = {name: os.environ.get(name) for name in keys}
        try:
            os.environ['DASHBOARD_USER'] = 'admin'
            os.environ['DASHBOARD_PASSWORD'] = 'HermesTestPassword123!'
            os.environ['DASHBOARD_EMAIL'] = 'service@maximo-seo.com'
            for key in ('SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY'):
                os.environ.pop(key, None)
            email_match = server._dashboard_validate_credentials('service@maximo-seo.com', 'HermesTestPassword123!')
            self.assertIsNone(email_match)
            username_match = server._dashboard_validate_credentials('admin', 'HermesTestPassword123!')
            self.assertIsNotNone(username_match)
            self.assertEqual(username_match['username'], 'admin')
            self.assertEqual(username_match['role'], 'admin')
        finally:
            for key, value in old.items():
                if value is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = value

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
