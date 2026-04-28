from pathlib import Path
import json
import os
import re
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


def req(path, method='GET', data=None, headers=None):
    body = None
    h = headers or {}
    if data is not None:
        body = json.dumps(data).encode('utf-8')
        h = {'Content-Type': 'application/json', **h}
    request = urllib.request.Request(BASE + path, method=method, headers=h, data=body)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.status, dict(response.headers), response.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read().decode('utf-8', 'replace')


class TemplateImprovementsFeatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global PORT, BASE
        cls._orig_auth_enabled = server._dashboard_auth_enabled
        cls._orig_file = server.TEMPLATE_IMPROVEMENTS_FILE
        server._dashboard_auth_enabled = lambda: False
        cls.tmpdir = tempfile.TemporaryDirectory()
        server.TEMPLATE_IMPROVEMENTS_FILE = Path(cls.tmpdir.name) / 'template_improvements.json'
        os.environ['TEMPLATE_IMPROVEMENTS_DRY_RUN'] = '1'
        cls.httpd = ReusableHTTPServer(('127.0.0.1', 0), server.DashboardHandler)
        PORT = cls.httpd.server_port
        BASE = f'http://127.0.0.1:{PORT}'
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=2)
        server._dashboard_auth_enabled = cls._orig_auth_enabled
        server.TEMPLATE_IMPROVEMENTS_FILE = cls._orig_file
        cls.tmpdir.cleanup()
        os.environ.pop('TEMPLATE_IMPROVEMENTS_DRY_RUN', None)

    def test_static_ui_markers_are_additive_and_scoped(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('TEMPLATE_IMPROVEMENTS_UI_2026_04_27', html)
        self.assertIn('tab-template-improvements', html)
        self.assertIn('data-testid="tab-template-improvements"', html)
        self.assertIn('data-testid="mobile-nav-template-improvements"', html)
        self.assertIn('page-template-improvements', html)
        self.assertIn('data-testid="page-template-improvements"', html)
        self.assertIn('TEMPLATE_IMPROVEMENTS_STYLE_2026_04_27', html)
        self.assertIn('.template-improvements .ti-panel', html)
        self.assertIn('TEMPLATE_IMPROVEMENTS_JS_2026_04_27', html)
        self.assertIn("showPage('template-improvements')", html)
        self.assertIn("['glm-4.6-agent','GLM 4.6','Analytics Integrator']", html)
        # Ensure the script/style were appended to the real document, not inside an earlier JS doc.write('</body>') string.
        self.assertGreater(html.rfind('<script id="template-improvements-script">'), html.find('<nav class="bottom-nav"'))
        self.assertGreater(html.rfind('<style id="template-improvements-style">'), html.find('<nav class="bottom-nav"'))

    def test_template_improvements_navigation_hooks_are_unique_and_stable(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertEqual(len(re.findall(r'<button[^>]*id="tab-template-improvements"', html)), 1)
        self.assertEqual(len(re.findall(r'<button[^>]*data-testid="tab-template-improvements"', html)), 1)
        self.assertEqual(len(re.findall(r'<button[^>]*data-testid="mobile-nav-template-improvements"', html)), 1)
        self.assertEqual(len(re.findall(r'<div[^>]*id="page-template-improvements"', html)), 1)
        self.assertEqual(len(re.findall(r'<div[^>]*data-testid="page-template-improvements"', html)), 1)
        self.assertRegex(html, r'id="tab-template-improvements"[^>]+onclick="showPage\(\'template-improvements\'\)"')
        self.assertRegex(html, r'data-testid="mobile-nav-template-improvements"[^>]+onclick="showPage\(\'template-improvements\'\);closeMobileMenu\(\)"')
        show_page_pos = html.find('window.showPage = function(name)')
        template_page_pos = html.find("var templateImprovementsPage = document.getElementById('page-template-improvements')")
        self.assertGreater(show_page_pos, -1)
        self.assertGreater(template_page_pos, show_page_pos)
        self.assertIn("templateImprovementsPage.style.display = isTemplateImprovements ? 'block' : 'none'", html)
        self.assertIn("templateImprovementsPage.classList.toggle('active', isTemplateImprovements)", html)

    def test_playwright_qa_script_is_committed_without_embedded_secrets(self):
        script = ROOT / 'scripts' / 'qa_template_improvements_playwright.py'
        self.assertTrue(script.exists())
        code = script.read_text(encoding='utf-8')
        self.assertIn('REQUIRED_AGENTS', code)
        self.assertIn('data-testid="tab-template-improvements"', code)
        self.assertIn('--use-render-env', code)
        self.assertNotRegex(code, r'sk-proj-[A-Za-z0-9_-]{20,}')
        self.assertNotRegex(code, r'ghp_[A-Za-z0-9]{20,}')
        self.assertNotRegex(code, r'Bearer\s+[A-Za-z0-9_-]{20,}')

    def test_backend_markers_exist(self):
        code = (ROOT / 'server.py').read_text(encoding='utf-8')
        self.assertIn('TEMPLATE IMPROVEMENTS — additive live pipeline MVP', code)
        self.assertIn('TEMPLATE_IMPROVEMENTS_API_2026_04_27', code)
        self.assertIn('TEMPLATE_IMPROVEMENTS_API_POST_2026_04_27', code)
        self.assertIn('TEMPLATE_IMPROVEMENTS_API_PUT_2026_04_27', code)

    def test_start_job_and_poll_results_dry_run(self):
        payload = {
            'domain': 'example.com',
            'subdomain': 'blog',
            'template_name': 'article.html',
            'original_html': '<article><h1>Hello</h1><p>{{$json.title}}</p></article>',
            'change_instructions': 'Keep variables untouched and improve layout.'
        }
        status, _, body = req('/api/improve/start', method='POST', data=payload)
        self.assertEqual(status, 200, body)
        data = json.loads(body)
        self.assertTrue(data['ok'])
        job_id = data['job']['id']
        for _ in range(30):
            status, _, body = req('/api/improve/jobs/' + job_id)
            data = json.loads(body)
            if data['job']['status'] == 'completed':
                break
            time.sleep(0.1)
        self.assertEqual(data['job']['status'], 'completed')
        self.assertEqual(len(data['outputs']), 5)
        self.assertIn('{{$json.title}}', data['outputs'][-1]['output_html'])

    def test_start_job_rejects_oversized_html(self):
        payload = {
            'domain': 'example.com',
            'template_name': 'huge.html',
            'original_html': 'x' * (server.TEMPLATE_IMPROVEMENTS_MAX_HTML_CHARS + 1),
            'change_instructions': 'too large test'
        }
        status, _, body = req('/api/improve/start', method='POST', data=payload)
        self.assertEqual(status, 400, body)
        self.assertIn('original_html too large', json.loads(body)['error'])

    def test_save_and_load_instruction(self):
        payload = {'domain': 'example.com', 'subdomain': 'blog', 'instructions': 'Use larger CTA buttons.'}
        status, _, body = req('/api/improve/instructions', method='POST', data=payload)
        self.assertEqual(status, 200, body)
        status, _, body = req('/api/improve/instructions/example.com')
        self.assertEqual(status, 200, body)
        rows = json.loads(body)['instructions']
        self.assertTrue(any(r['instructions'] == 'Use larger CTA buttons.' for r in rows))

    def test_improve_get_routes_are_auth_gated_when_auth_enabled(self):
        orig = server._dashboard_auth_enabled
        server._dashboard_auth_enabled = lambda: True
        try:
            for path in ('/api/improve/jobs', '/api/improve/results/demo', '/api/improve/instructions/example.com'):
                status, _, body = req(path)
                self.assertEqual(status, 401, f'{path}: {body}')
        finally:
            server._dashboard_auth_enabled = orig

    def test_cancelled_job_is_not_overwritten_after_inflight_agent_returns(self):
        original_call = server._template_improvement_call_agent
        gate = threading.Event()
        def slow_call(agent, prompt, timeout=180):
            gate.wait(timeout=2)
            return '<article>late output</article>', {'mock': True}
        server._template_improvement_call_agent = slow_call
        try:
            payload = {
                'domain': 'cancel-test.com',
                'template_name': 'cancel.html',
                'original_html': '<article><h1>Cancel</h1></article>',
                'change_instructions': 'test cancel race'
            }
            status, _, body = req('/api/improve/start', method='POST', data=payload)
            self.assertEqual(status, 200, body)
            job_id = json.loads(body)['job']['id']
            # Wait until first agent is in-flight, then cancel.
            for _ in range(30):
                status, _, body = req('/api/improve/jobs/' + job_id)
                job = json.loads(body)['job']
                if job['status'] == 'agent-1-running':
                    break
                time.sleep(0.05)
            status, _, body = req(f'/api/improve/jobs/{job_id}/cancel', method='POST', data={})
            self.assertEqual(status, 200, body)
            gate.set()
            time.sleep(0.3)
            status, _, body = req('/api/improve/jobs/' + job_id)
            job = json.loads(body)['job']
            self.assertEqual(job['status'], 'cancelled')
        finally:
            gate.set()
            server._template_improvement_call_agent = original_call


if __name__ == '__main__':
    unittest.main()
