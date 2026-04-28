from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def _page_fixer_block():
    start = HTML.index('<div id="page-fixer"')
    end = HTML.index('</div><!-- end #page-fixer -->', start)
    return HTML[start:end]


def test_fixer_tab_declares_read_only_manual_import_policy():
    block = _page_fixer_block()
    assert 'N8N_FIXER_READ_ONLY_UI_2026_04_27' in HTML
    assert 'MANUAL IMPORT ONLY' in block
    assert 'READ-ONLY' in block or 'read-only' in block.lower()


def test_fixer_tab_no_longer_advertises_direct_n8n_deploy_or_overwrite():
    block = _page_fixer_block()
    forbidden = [
        'Then deploy directly to your N8N account',
        'Ready to Deploy',
        'Deploy to N8N',
        'Deploy Fixed Workflow to N8N',
        'Overwrites the selected workflow',
        'DEPLOY CONFIRMATION',
        'This will OVERWRITE the existing workflow',
    ]
    for text in forbidden:
        assert text not in block
    assert "fetch('/api/fixer/deploy'" not in block


def test_fixer_tab_keeps_safe_output_actions():
    block = _page_fixer_block()
    assert 'downloadFixedJson()' in block
    assert 'copyFixedJson()' in block
    assert 'saveFixRecord(null)' in block
    assert 'Download Fixed .json' in block
    assert 'Copy JSON' in block


def test_fetch_from_n8n_copy_is_read_only_not_auto_import():
    assert 'Fetch from N8N (read-only)' in HTML
    assert 'Auto-Import from N8N' not in HTML
