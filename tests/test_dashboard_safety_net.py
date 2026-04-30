from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ci_does_not_mask_pytest_failures():
    workflow = (ROOT / '.github' / 'workflows' / 'test.yml').read_text(encoding='utf-8')
    assert 'pytest tests/ -v --tb=short' in workflow
    assert 'exit 0' not in workflow
    assert '|| true' not in workflow


def test_dashboard_handler_legacy_send_json_helper_exists():
    server_py = (ROOT / 'server.py').read_text(encoding='utf-8')
    assert 'def _send_json(self, status, payload):' in server_py
    assert 'return json_response(self, status, payload)' in server_py


def test_kwr_serp_button_avoids_interpolated_js_string_context():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert "data-kw=\"${kwrEsc(kw)}\"" in html
    assert "data-pillar=\"${kwrEsc(r.pillar || '')}\"" in html
    assert 'onclick="kwrShowSerp(this.dataset.kw, this.dataset.pillar)"' in html
    assert "kwrShowSerp('${kwrEsc(kw)}'" not in html


def test_kwr_html_escape_covers_single_quotes():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert ".replace(/'/g,'&#39;')" in html


def test_kwr_poll_returns_fetch_promise_for_backoff():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert "if (window.__kwrPollerActive && _kwrRunId) _kwrPoller = setTimeout(tick, 5000);" in html
    assert "if (window.__kwrPollerActive && _kwrRunId) _kwrPoller = setTimeout(tick, _kwrPollDelay);" in html
    assert "if (!_kwrRunId) return Promise.resolve();" in html
    assert "return fetch('/api/kwr/status?run_id=' + encodeURIComponent(_kwrRunId))" in html
    assert "throw new Error('HTTP ' + r.status);" in html
    assert "throw err;" in html
