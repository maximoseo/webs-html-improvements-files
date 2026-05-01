from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = REPO_ROOT / "index.html"


def html() -> str:
    return INDEX_HTML.read_text(encoding="utf-8")


def test_project_card_preview_uses_latest_version_that_contains_html():
    body = html()
    assert "PROJECT_PREVIEW_LATEST_HTML_VERSION_FIX_2026_04_30" in body
    assert "function selectProjectPreviewVersion(versions){" in body
    assert "const htmlVersions=(versions||[]).filter(v=>v.files&&v.files.some(f=>(f.name||'').toLowerCase().endsWith('.html')));" in body
    assert "const latestHtmlVersion=selectProjectPreviewVersion(p.versions)||latest;" in body
    assert "if(latestHtmlVersion){" in body
    assert "const htmlFile=latestHtmlVersion.files.find(f=>(f.name||'').toLowerCase().endsWith('.html'));" in body


def test_project_card_preview_prefers_gpt55_for_same_date_over_five_agent_runs():
    body = html()
    assert "PROJECT_PREVIEW_GPT55_PREFERENCE_2026_04_30" in body
    assert "if(agent==='GPT 5.5') score+=100;" in body
    assert "if(v.includes('five agents')) score-=25;" in body
    assert "const prefCmp=projectPreviewPreference(b.name)-projectPreviewPreference(a.name);" in body


def test_project_card_preview_context_uses_html_version_not_notes_only_latest():
    body = html()
    assert "const _psAgent=latestHtmlVersion?detectAgent(latestHtmlVersion.name):(latest?detectAgent(latest.name):'Agent');" in body
    assert "const _psVersion=latestHtmlVersion?latestHtmlVersion.name:(latest?latest.name:'');" in body
    assert "const _psFiles=latestHtmlVersion?latestHtmlVersion.files.map(f=>({name:f.name,path:f.path,download:f.download,url:f.url,size:f.size})):(latest?latest.files.map(f=>({name:f.name,path:f.path,download:f.download,url:f.url,size:f.size})):[]);" in body


def test_project_preview_inline_onclick_arguments_are_escaped():
    body = html()
    assert "PROJECT_PREVIEW_INLINE_ONCLICK_ARG_ESCAPE_2026_05_01" in body
    assert "function previewOnclickArg(value){" in body
    assert ".replace(/\\\\/g,'\\\\\\\\')" in body
    assert ".replace(/'/g,\"\\\\'\")" in body
    assert ".replace(/\"/g,'&quot;')" in body
    assert "const _previewDownloadArg=previewOnclickArg(f.download);" in body
    assert "const _previewNameArg=previewOnclickArg(p.name+' - '+f.name);" in body
    assert "openPreview('${_previewDownloadArg}','${_previewNameArg}','${_fCtxEnc}')" in body
    assert "const _latestHtmlUrlArg=previewOnclickArg(latestHtmlUrl);" in body
    assert "const _latestHtmlNameArg=previewOnclickArg(latestHtmlName);" in body
    assert "openPreview('${_latestHtmlUrlArg}','${_latestHtmlNameArg}','${_previewCtxEnc}')" in body
    assert "openPreview('${f.download}','${p.name} - ${f.name}','${_fCtxEnc}')" not in body
    assert "openPreview('${latestHtmlUrl}','${latestHtmlName}','${_previewCtxEnc}')" not in body
