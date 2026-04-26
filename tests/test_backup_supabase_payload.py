import json
import os
import unittest

import backup


class _FakeResponse:
    def __init__(self, status=200, payload=b'[]'):
        self.status = status
        self._payload = payload

    def read(self):
        return self._payload


class BackupSupabasePayloadTests(unittest.TestCase):
    def setUp(self):
        self._orig_url = os.environ.get('SUPABASE_URL')
        self._orig_key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
        os.environ['SUPABASE_URL'] = 'https://example.supabase.co'
        os.environ['SUPABASE_SERVICE_ROLE_KEY'] = 'test-service-role'

    def tearDown(self):
        if self._orig_url is None:
            os.environ.pop('SUPABASE_URL', None)
        else:
            os.environ['SUPABASE_URL'] = self._orig_url
        if self._orig_key is None:
            os.environ.pop('SUPABASE_SERVICE_ROLE_KEY', None)
        else:
            os.environ['SUPABASE_SERVICE_ROLE_KEY'] = self._orig_key

    def test_list_supabase_payload_includes_prefix(self):
        calls = []
        orig_http = backup._http
        try:
            def fake_http(url, method='GET', headers=None, data=None, timeout=120):
                calls.append({'url': url, 'method': method, 'data': data})
                return _FakeResponse(status=200, payload=b'[]')

            backup._http = fake_http
            out = backup.list_supabase()
            self.assertEqual(out, [])
            self.assertTrue(calls)
            body = json.loads(calls[0]['data'].decode('utf-8'))
            self.assertIn('prefix', body)
            self.assertEqual(body['prefix'], '')
        finally:
            backup._http = orig_http

    def test_supa_prune_payload_includes_prefix(self):
        calls = []
        orig_http = backup._http
        try:
            def fake_http(url, method='GET', headers=None, data=None, timeout=120):
                calls.append({'url': url, 'method': method, 'data': data})
                return _FakeResponse(status=200, payload=b'[]')

            backup._http = fake_http
            backup._supa_prune()
            self.assertTrue(calls)
            body = json.loads(calls[0]['data'].decode('utf-8'))
            self.assertIn('prefix', body)
            self.assertEqual(body['prefix'], '')
        finally:
            backup._http = orig_http


if __name__ == '__main__':
    unittest.main()
