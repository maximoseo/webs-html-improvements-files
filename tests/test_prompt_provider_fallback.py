import os
from unittest import mock

import server


def test_gemini_native_429_falls_through_to_next_provider():
    calls = []

    def fake_fetch_json(url, headers=None, method='GET', body=None, timeout=None):
        calls.append(url)
        if 'generativelanguage.googleapis.com' in url:
            raise RuntimeError('429 Too Many Requests')
        return {'choices': [{'message': {'content': '<html>fallback ok</html>'}}]}

    with mock.patch.dict(os.environ, {
        'GEMINI_API_KEY': 'fake-gemini-key',
        'GEMINI_MODEL': 'gemini-2.5-flash',
        'OPENROUTER_API_KEY': 'fake-openrouter-key',
    }, clear=False), mock.patch.object(server, 'fetch_json', side_effect=fake_fetch_json):
        content, provider = server.call_with_fallback([
            {'role': 'system', 'content': 'Return HTML'},
            {'role': 'user', 'content': 'Smoke'},
        ], 'gemini-2.5-flash', timeout=5)

    assert content == '<html>fallback ok</html>'
    assert provider == 'openrouter'
    assert any('generativelanguage.googleapis.com' in url for url in calls)
    assert any('openrouter.ai' in url for url in calls)


def test_google_gemini_openrouter_slug_can_fallback_to_native_gemini():
    calls = []

    def fake_fetch_json(url, headers=None, method='GET', body=None, timeout=None):
        calls.append(url)
        if 'openrouter.ai' in url:
            raise RuntimeError('401 Unauthorized')
        return {'candidates': [{'content': {'parts': [{'text': '<html>native gemini ok</html>'}]}}]}

    with mock.patch.dict(os.environ, {
        'OPENROUTER_API_KEY': 'fake-openrouter-key',
        'GEMINI_API_KEY': 'fake-gemini-key',
        'GEMINI_MODEL': 'gemini-2.5-flash',
    }, clear=False), mock.patch.object(server, 'fetch_json', side_effect=fake_fetch_json):
        content, provider = server.call_with_fallback([
            {'role': 'system', 'content': 'Return HTML'},
            {'role': 'user', 'content': 'Smoke'},
        ], 'google/gemini-2.5-flash', timeout=5)

    assert content == '<html>native gemini ok</html>'
    assert provider == 'gemini'
    assert any('openrouter.ai' in url for url in calls)
    assert any('generativelanguage.googleapis.com' in url for url in calls)
