import json
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import server

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


class TestN8NFixerBackendSafety:
    @classmethod
    def setup_class(cls):
        global PORT, BASE
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: False
        cls.httpd = ReusableHTTPServer(('127.0.0.1', 0), server.DashboardHandler)
        PORT = cls.httpd.server_port
        BASE = f'http://127.0.0.1:{PORT}'
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    @classmethod
    def teardown_class(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled

    def test_validate_endpoint_accepts_valid_n8n_workflow_and_returns_metadata(self):
        workflow = {
            'name': 'Broken Article Workflow',
            'nodes': [{'id': '1', 'name': 'Start', 'type': 'n8n-nodes-base.manualTrigger', 'parameters': {}}],
            'connections': {'Start': {'main': [[]]}},
            'settings': {'executionOrder': 'v1'},
        }
        body = json.dumps({'workflowJson': json.dumps(workflow)}).encode('utf-8')
        status, _, raw = req('/api/n8n-fixer/validate', method='POST', headers={'Content-Type': 'application/json'}, data=body)
        data = json.loads(raw)
        assert status == 200
        assert data['ok'] is True
        assert data['validJson'] is True
        assert data['looksLikeN8N'] is True
        assert data['workflowName'] == 'Broken Article Workflow'
        assert data['nodeCount'] == 1
        assert data['connectionCount'] == 1
        assert data['validation']['allNodesPreserved'] is True

    def test_validate_endpoint_rejects_invalid_json(self):
        body = json.dumps({'workflowJson': '{broken'}).encode('utf-8')
        status, _, raw = req('/api/n8n-fixer/validate', method='POST', headers={'Content-Type': 'application/json'}, data=body)
        data = json.loads(raw)
        assert status == 400
        assert data['ok'] is False
        assert data['validJson'] is False
        assert 'error' in data

    def test_validate_endpoint_warns_on_non_n8n_json(self):
        body = json.dumps({'workflowJson': json.dumps({'hello': 'world'})}).encode('utf-8')
        status, _, raw = req('/api/n8n-fixer/validate', method='POST', headers={'Content-Type': 'application/json'}, data=body)
        data = json.loads(raw)
        assert status == 200
        assert data['ok'] is True
        assert data['validJson'] is True
        assert data['looksLikeN8N'] is False
        assert any('nodes' in warning or 'connections' in warning for warning in data['warnings'])

    def test_n8n_write_endpoints_remain_blocked(self):
        for path in ('/api/fixer/deploy', '/api/n8n/deploy'):
            status, _, raw = req(path, method='POST', headers={'Content-Type': 'application/json'}, data=b'{}')
            data = json.loads(raw)
            assert status == 403
            assert data['ok'] is False
            assert 'MANUAL IMPORT ONLY' in data.get('safety', '')

    def test_n8n_api_guard_blocks_mutating_methods(self):
        with mock.patch.dict(server.os.environ, {'N8N_BASE_URL': 'https://websiseo.app.n8n.cloud'}):
            with pytest_raises(ValueError):
                server.fetch_json('https://websiseo.app.n8n.cloud/api/v1/workflows/abc', method='PUT', body={'x': 1})


def pytest_raises(exc_type):
    class Ctx:
        def __enter__(self):
            return self
        def __exit__(self, typ, value, tb):
            assert typ is not None, f'expected {exc_type.__name__}'
            assert issubclass(typ, exc_type), f'expected {exc_type.__name__}, got {typ}'
            return True
    return Ctx()
