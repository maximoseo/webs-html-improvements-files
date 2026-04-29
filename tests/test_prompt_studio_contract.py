from unittest import mock
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_server():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location('dashboard_server_contract', ROOT / 'server.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_prompt_studio_contract_missing_domain_rejected():
    server = load_server()
    with mock.patch.object(server, '_get_provider_chain', return_value=['test']):
        try:
            server.improve_prompt_with_model({'draftPrompt': 'Improve this prompt', 'domain': ''})
        except ValueError as exc:
            assert 'Target domain or URL is required' in str(exc)
        else:
            raise AssertionError('missing domain should be rejected')


def test_prompt_studio_contract_validation_defaults_to_needs_review():
    server = load_server()
    report = server._prompt_studio_build_validation_report({
        'domain': 'example.com',
        'readOnlyN8n': True,
        'analysisStatus': 'not_started',
    }, 'draft')
    assert report['status'] == 'needs_review'
    assert report['site_profile_status'] == 'needs_review'
    assert report['read_only_n8n'] is True
    assert report['next_action'] == 'review_site_profile'
    assert 'business_name' in report['missing_site_profile_fields']


def test_prompt_studio_contract_response_preserves_content_and_adds_metadata():
    server = load_server()
    captured = {}

    def fake_call(messages, model, timeout=120):
        captured['messages'] = messages
        return ('## Site Profile\nneeds_review\n\n## Generated Prompt\nDo work\n\n## Validation Report\nneeds_review\n\n## Storage Metadata\nnone\n\n## Next Action\nreview_site_profile', 'test-provider')

    with mock.patch.object(server, '_get_provider_chain', return_value=['test']), \
         mock.patch.object(server, 'call_with_fallback', side_effect=fake_call):
        result = server.improve_prompt_with_model({
            'draftPrompt': 'Improve this prompt',
            'domain': 'example.com',
            'agentName': 'Hermes',
            'versionName': 'v1',
            'checklist': [],
            'model': 'test-model',
            'readOnlyN8n': True,
        })

    assert result['content'].startswith('## Site Profile')
    assert result['contractVersion'] == server.PROMPT_STUDIO_CONTRACT_VERSION
    assert result['validationReport']['status'] == 'needs_review'
    assert result['nextAction'] == 'review_site_profile'
    system_prompt = captured['messages'][0]['content']
    for section in ['## Site Profile', '## Generated Prompt', '## Validation Report', '## Storage Metadata', '## Next Action']:
        assert section in system_prompt
    assert 'read-only by default' in system_prompt
    assert 'preserve all' in system_prompt.lower()


def test_prompt_studio_contract_system_prompt_has_no_conflicting_publish_schema():
    server = load_server()
    captured = {}

    def fake_call(messages, model, timeout=120):
        captured['system'] = messages[0]['content']
        return ('## Site Profile\nneeds_review\n\n## Generated Prompt\nPrompt\n\n## Validation Report\nneeds_review\n\n## Storage Metadata\nnone\n\n## Next Action\nreview_site_profile', 'test-provider')

    with mock.patch.object(server, '_get_provider_chain', return_value=['test']), \
         mock.patch.object(server, 'call_with_fallback', side_effect=fake_call):
        server.improve_prompt_with_model({
            'draftPrompt': 'Improve this prompt',
            'domain': 'example.com',
            'agentName': 'Hermes',
            'versionName': 'v1',
            'checklist': [],
            'model': 'test-model',
            'readOnlyN8n': True,
        })

    system_prompt = captured['system']
    assert 'reviewable Prompt Studio package' in system_prompt
    assert 'Inside ## Generated Prompt' in system_prompt
    assert '\n## Objective — one paragraph' not in system_prompt
    assert '\n## Delivery — mandatory export and publish instructions' not in system_prompt
    assert '### Objective — one paragraph' in system_prompt
    assert '### Delivery Targets After Approval' in system_prompt
    assert 'production-ready, well-structured prompt' not in system_prompt
    assert 'must explicitly require exporting the final improved files' not in system_prompt
    assert 'requires explicit task-specific approval after review' in system_prompt
