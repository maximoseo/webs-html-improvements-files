import json
import os
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

import server

PORT = 18112
BASE = f'http://127.0.0.1:{PORT}'


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class AuthToolingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._old_env = {name: os.environ.get(name) for name in (
            'DASHBOARD_USERS',
            'DASHBOARD_USER',
            'DASHBOARD_PASSWORD',
            'DASHBOARD_EMAIL',
            'SUPABASE_URL',
            'SUPABASE_ANON_KEY',
        )}
        os.environ['DASHBOARD_USERS'] = 'admin:Maximo2025!'
        os.environ['DASHBOARD_USER'] = 'admin'
        os.environ['DASHBOARD_PASSWORD'] = 'Maximo2025!'
        os.environ['DASHBOARD_EMAIL'] = 'service@maximo-seo.com'
        os.environ.pop('SUPABASE_URL', None)
        os.environ.pop('SUPABASE_ANON_KEY', None)
        server._R2_RATE_BUCKETS.clear()
        cls.httpd = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._R2_RATE_BUCKETS.clear()
        for key, value in cls._old_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    def setUp(self):
        server._R2_RATE_BUCKETS.clear()

    def test_auth_status_endpoint_reports_runtime_config_without_secrets(self):
        status, _, body = req('/api/auth/status')
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        self.assertTrue(data['authEnabled'])
        self.assertEqual(data['cookieName'], 'dash_auth')
        self.assertEqual(data['loginPaths'], ['/api/auth/login', '/api/login', '/login'])
        self.assertEqual(
            data['rateLimit']['ipSourceOrder'],
            ['CF-Connecting-IP', 'X-Forwarded-For', 'X-Real-IP', 'client_address'],
        )
        self.assertTrue(data['configuredSources']['breakGlassEnv'])
        self.assertTrue(data['configuredSources']['breakGlassEmailAlias'])
        self.assertTrue(data['configuredSources']['stage8UsersEnv'])
        self.assertEqual(data['counts']['stage8Users'], 1)
        self.assertNotIn('Maximo2025!', body)
        self.assertNotIn('service@maximo-seo.com', body)

    def test_auth_status_warns_when_break_glass_password_drifts_from_users_json(self):
        users_path = server._USERS_JSON_PATH
        original_users = None
        if os.path.exists(users_path):
            with open(users_path, 'r', encoding='utf-8') as fh:
                original_users = fh.read()
        try:
            with open(users_path, 'w', encoding='utf-8') as fh:
                json.dump([
                    {
                        'id': 'user-1',
                        'username': 'admin',
                        'email': 'service@maximo-seo.com',
                        'role': 'admin',
                        'password_hash': server._mu_hash_password('DifferentPass123!'),
                    }
                ], fh)
            status, _, body = req('/api/auth/status')
            data = json.loads(body)
            self.assertEqual(status, 200)
            warnings = data.get('driftWarnings') or []
            self.assertTrue(any('users.json password hash does not match the configured break-glass password' in item for item in warnings), warnings)
            self.assertNotIn('DifferentPass123!', body)
            self.assertNotIn('Maximo2025!', body)
        finally:
            if original_users is None:
                try:
                    os.remove(users_path)
                except FileNotFoundError:
                    pass
            else:
                with open(users_path, 'w', encoding='utf-8') as fh:
                    fh.write(original_users)

    def test_login_rate_limit_uses_forwarded_ip_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'CF-Connecting-IP': '203.0.113.10',
            'X-Forwarded-For': '203.0.113.10, 10.0.0.1',
            'X-Real-IP': '203.0.113.10',
        }
        payload = json.dumps({'user': 'admin', 'password': 'wrong-password'}).encode()
        codes = []
        retry_after = None
        for _ in range(12):
            status, response_headers, _ = req('/api/auth/login', method='POST', headers=headers, data=payload)
            codes.append(status)
            if status == 429:
                retry_after = response_headers.get('Retry-After')
                break
        self.assertIn(429, codes, codes)
        self.assertTrue(retry_after)

        other_headers = {
            'Content-Type': 'application/json',
            'CF-Connecting-IP': '203.0.113.11',
            'X-Forwarded-For': '203.0.113.11, 10.0.0.1',
            'X-Real-IP': '203.0.113.11',
        }
        status, _, body = req('/api/auth/login', method='POST', headers=other_headers, data=payload)
        self.assertEqual(status, 401)
        self.assertEqual(json.loads(body)['error'], 'invalid_credentials')


if __name__ == '__main__':
    unittest.main()
