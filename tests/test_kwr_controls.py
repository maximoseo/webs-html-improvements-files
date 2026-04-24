import json
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path
from unittest import mock

import server

PORT = 18113
BASE = f'http://127.0.0.1:{PORT}'
REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


def req(path, method='GET', headers=None, data=None):
    request = urllib.request.Request(BASE + path, method=method, headers=headers or {}, data=data)
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class KwResearchControlsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: False
        cls.httpd = HTTPServer(('127.0.0.1', PORT), server.DashboardHandler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.25)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled

    def test_kwr_ui_has_distinct_selected_model_and_best_text_swarm_actions(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('Run Selected Model', html)
        self.assertIn('Best Text Swarm', html)
        self.assertIn('Used only for the selected-model run', html)
        self.assertNotIn('__ensemble__', html)
        self.assertIn("kwrSetButtons && kwrSetButtons(false);", html)

    def test_swarm_endpoint_uses_best_text_models(self):
        payload = json.dumps({'website_url': 'https://example.com', 'model': 'openai/gpt-5.4'}).encode()
        with mock.patch.object(server.kwr_backend, 'start_best_text_swarm', return_value=('swarm-123', None)) as mocked:
            status, _, body = req('/api/kwr/swarm', method='POST', headers={'Content-Type': 'application/json'}, data=payload)
        data = json.loads(body)
        self.assertEqual(status, 200)
        self.assertTrue(data['ok'])
        self.assertEqual(data['run_id'], 'swarm-123')
        mocked.assert_called_once()
        args, _ = mocked.call_args
        self.assertEqual(args[0]['website_url'], 'https://example.com')
        self.assertEqual(args[0]['model'], 'openai/gpt-5.4')

    def test_start_best_text_swarm_stores_swarm_model_marker(self):
        captured = {}

        def fake_start_ensemble(payload, call_llm, default_models=None, mode_label='ensemble'):
            captured['payload'] = payload
            captured['default_models'] = default_models
            captured['mode_label'] = mode_label
            return 'swarm-abc', None

        with mock.patch.object(server.kwr_backend, 'start_ensemble', side_effect=fake_start_ensemble):
            run_id, err = server.kwr_backend.start_best_text_swarm({'website_url': 'https://example.com', 'model': 'openai/gpt-5.4'}, object())

        self.assertEqual((run_id, err), ('swarm-abc', None))
        self.assertEqual(captured['payload']['model'], 'best-text-swarm')
        self.assertEqual(captured['payload']['_mode'], 'swarm')
        self.assertEqual(captured['default_models'], server.kwr_backend.BEST_TEXT_SWARM_MODELS)
        self.assertEqual(captured['mode_label'], 'swarm')


if __name__ == '__main__':
    unittest.main()
