from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


def html():
    return INDEX_HTML.read_text(encoding='utf-8')


def test_prompt_studio_html_file_info_falls_back_to_direct_download_url():
    s = html()
    assert 'PROMPT_STUDIO_FILE_URL_FALLBACK_2026_04_27' in s
    assert 'promptStudioContext.htmlDownloadUrl' in s
    assert 'promptStudioContext.htmlFileName||' in s
    assert 'download: promptStudioContext.htmlDownloadUrl' in s


def test_prompt_studio_launch_pipeline_surfaces_missing_html_in_tweak_status():
    s = html()
    assert "const noHtmlMessage='No HTML template found in the selected version.'" in s
    assert 'tweakStatus.textContent=noHtmlMessage' in s
    assert 'status.textContent=noHtmlMessage' in s


def test_prompt_studio_mobile_polish_marker_and_layout_guards_exist():
    s = html()
    assert 'PROMPT_STUDIO_MOBILE_POLISH_2026_04_27' in s
    assert '<option value="google/gemini-2.5-flash" selected>' in s
    assert "selectedModel=modelEl?modelEl.value:'google/gemini-2.5-flash'" in s
    assert "model:selectedModel||'google/gemini-2.5-flash'" in s
    assert 'claude-opus-4-7" selected' not in s
    assert '#prompt-modal .modal.prompt-modal' in s
    assert '#prompt-modal .prompt-dialog' in s  # legacy-compatible fallback selector only
    assert '#prompt-modal .modal.prompt-modal > .prompt-container' in s
    assert '#prompt-modal.modal-overlay.open .modal.prompt-modal .prompt-container > .prompt-panel:first-child > .prompt-actions' in s
    assert '#prompt-modal .modal.prompt-modal .prompt-panel > .prompt-actions' in s
    assert '#prompt-modal .modal.prompt-modal .prompt-panel + .prompt-panel > .prompt-actions' in s
    assert '#prompt-modal .prompt-panel > .prompt-actions' in s
    assert '#prompt-modal .prompt-panel + .prompt-panel > .prompt-actions' in s
    assert '@media(max-width:768px)' in s
    assert 'grid-template-columns:1fr' in s
    assert 'max-height:calc(100vh - 16px)' in s
    assert 'max-height:calc(100dvh - 16px)' in s
    assert 'display:grid !important' in s
    assert 'backdrop-filter:none !important' in s
