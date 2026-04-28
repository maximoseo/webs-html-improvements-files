import json
import unittest
from unittest import mock

import n8n_readonly_client as client


class FakeResponse:
    def __init__(self, payload, status=200):
        self.payload = payload
        self.status = status
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        return False
    def read(self):
        return json.dumps(self.payload).encode('utf-8')


class N8NReadOnlyClientTests(unittest.TestCase):
    def test_rejects_non_get_methods(self):
        c = client.N8NReadOnlyClient('https://websiseo.app.n8n.cloud', 'key')
        with self.assertRaises(ValueError):
            c.request('/api/v1/workflows', method='POST')

    def test_rejects_mutating_paths_even_with_get(self):
        c = client.N8NReadOnlyClient('https://websiseo.app.n8n.cloud', 'key')
        with self.assertRaises(ValueError):
            c.request('/api/v1/workflows/123/activate')

    def test_lists_workflows_with_pagination(self):
        c = client.N8NReadOnlyClient('https://websiseo.app.n8n.cloud', 'key')
        responses = [
            FakeResponse({'data': [{'id': '1', 'name': 'one'}], 'nextCursor': 'abc'}),
            FakeResponse({'data': [{'id': '2', 'name': 'two'}]}),
        ]
        seen_urls = []
        def fake_urlopen(req, timeout=30):
            seen_urls.append(req.full_url)
            return responses.pop(0)
        with mock.patch('urllib.request.urlopen', side_effect=fake_urlopen):
            workflows = c.get_all_workflows(limit=1)
        self.assertEqual([w['id'] for w in workflows], ['1', '2'])
        self.assertIn('cursor=abc', seen_urls[1])

    def test_get_workflow_detail_uses_get_endpoint(self):
        c = client.N8NReadOnlyClient('https://websiseo.app.n8n.cloud', 'key')
        with mock.patch('urllib.request.urlopen', return_value=FakeResponse({'id': 'abc', 'nodes': []})) as mocked:
            detail = c.get_workflow_detail('abc')
        self.assertEqual(detail['id'], 'abc')
        req = mocked.call_args.args[0]
        self.assertEqual(req.get_method(), 'GET')
        self.assertTrue(req.full_url.endswith('/api/v1/workflows/abc'))


if __name__ == '__main__':
    unittest.main()
