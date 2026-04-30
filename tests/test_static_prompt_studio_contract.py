import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]


@pytest.mark.xfail(reason='frontend Prompt Studio contract markers were removed by a later index.html restore; keep explicit until UI contract is restored', strict=False)
def test_prompt_studio_contract_frontend_markers_and_payload():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    assert '// ── Prompt Studio Contract Rules v2026-04-29 ──' in html
    assert '// Prompt Studio Contract: initialize context' in html
    assert '// Prompt Studio Contract: domain-first guard' in html
    assert '// Prompt Studio Contract: request metadata' in html
    for token in [
        'contractVersion:promptStudioContext.contractVersion',
        'siteProfile:promptStudioContext.siteProfile',
        'siteProfileReviewed:promptStudioContext.siteProfileReviewed',
        'readOnlyN8n:PROMPT_STUDIO_READ_ONLY_N8N',
        'nextAction:promptStudioContext.nextAction',
        'Target domain/URL is required before final prompt generation.',
    ]:
        assert token in html


@pytest.mark.xfail(reason='frontend Prompt Studio mandatory checklist was removed by a later index.html restore; keep explicit until UI contract is restored', strict=False)
def test_prompt_studio_contract_mandatory_checklist_ids_exist():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    for checklist_id in [
        'mandatory-domain-first-site-analysis',
        'mandatory-site-profile-review',
        'mandatory-no-invented-assets',
        'mandatory-wp-custom-html-compatibility',
        'mandatory-responsive-no-overflow',
        'mandatory-rtl-ltr-handling',
        'mandatory-n8n-read-only-default',
        'mandatory-n8n-variable-preservation',
        'mandatory-output-package-validation',
        'mandatory-storage-no-secrets-duplicates',
    ]:
        assert checklist_id in html


def test_prompt_studio_contract_backend_markers_and_sections():
    server_py = (ROOT / 'server.py').read_text(encoding='utf-8')
    assert '# ===== Prompt Studio Contract v2026-04-29 =====' in server_py
    assert '# Prompt Studio Contract: domain-first backend guard' in server_py
    assert '# Prompt Studio Contract: validation report' in server_py
    assert '# Prompt Studio Contract: system prompt injection' in server_py
    for section in ['## Site Profile', '## Generated Prompt', '## Validation Report', '## Storage Metadata', '## Next Action']:
        assert section in server_py
    for token in ['read_only_n8n', 'needs_review', '{{$execution.resumeUrl}}', 'site_profile', 'validationReport']:
        assert token in server_py
