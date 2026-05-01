from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _html() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_project_file_actions_escape_inline_prompt_studio_arguments_and_href_attrs():
    html = _html()

    assert "PROJECT_FILE_ACTION_INLINE_ATTR_ESCAPE_2026_05_01" in html
    assert "function projectActionAttr(value){" in html

    # Per-file Prompt Studio buttons must not inject raw download URLs into a
    # single-quoted JS string inside a double-quoted onclick attribute.
    assert "const _promptDownloadArg=previewOnclickArg(f.download);" in html
    assert "openPromptStudioForFile('${encodeURIComponent(p.name)}','${encodeURIComponent(agentName)}','${encodeURIComponent(f.name)}','${_promptDownloadArg}')" in html
    assert "openPromptStudioForFile('${encodeURIComponent(p.name)}','${encodeURIComponent(agentName)}','${encodeURIComponent(f.name)}','${f.download}')" not in html

    # File action href attributes must escape HTML attribute delimiters.
    assert "const _fileUrlAttr=projectActionAttr(f.url);" in html
    assert "const _fileDownloadAttr=projectActionAttr(f.download);" in html
    assert '<a href="${_fileUrlAttr}" target="_blank" class="action-btn">View Code</a>' in html
    assert '<a href="${_fileDownloadAttr}" class="action-btn primary">Download</a>' in html
    assert '<a href="${f.url}" target="_blank" class="action-btn">View Code</a>' not in html
    assert '<a href="${f.download}" class="action-btn primary">Download</a>' not in html


def test_project_card_and_compare_prompt_actions_escape_url_arguments():
    html = _html()

    # Project-card Prompt Studio and Compare CTAs use escaped inline args.
    assert "const _compareProjectArg=previewOnclickArg(p.name);" in html
    assert "const _latestHtmlUrlPromptArg=previewOnclickArg(latestHtmlUrl);" in html
    assert "openCompare('${_compareProjectArg}')" in html
    assert "openCompare('${p.name}')" not in html
    assert "openPromptStudio('${encodeURIComponent(p.name)}','${encodeURIComponent(_psAgent)}','${encodeURIComponent(_psVersion)}','${_latestHtmlUrlPromptArg}','${_psFilesEnc}')" in html
    assert "${latestHtmlUrl.replace(/'/g,\"%27\")}" not in html

    # Compare modal actions also escape Prompt Studio, Expand, and View Code args.
    assert "const _comparePromptDownloadArg=previewOnclickArg(item.file.download);" in html
    assert "const _focusedDownloadArg=previewOnclickArg(item.file.download);" in html
    assert "const _focusedAgentArg=previewOnclickArg(item.agent);" in html
    assert "const _focusedVersionArg=previewOnclickArg(item.version);" in html
    assert "const _compareFileUrlAttr=projectActionAttr(item.file.url);" in html
    assert "openPromptStudio('${encodeURIComponent(projectName)}','${encodeURIComponent(item.agent)}','${encodeURIComponent(item.version)}','${_comparePromptDownloadArg}','${filesEnc}')" in html
    assert "openFocusedCompare('${_focusedDownloadArg}','${_focusedAgentArg}','${_focusedVersionArg}')" in html
    assert '<a href="${_compareFileUrlAttr}" target="_blank" class="action-btn">View Code</a>' in html
    assert "${item.file.download.replace(/'/g,'%27')}" not in html
