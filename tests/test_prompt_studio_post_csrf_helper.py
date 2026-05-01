from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _html() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_prompt_studio_posts_use_explicit_csrf_json_helper():
    html = _html()

    assert "PROMPT_STUDIO_POST_CSRF_JSON_HELPER_2026_05_01" in html
    assert "async function promptStudioJsonPost(url,payload,signal){" in html
    assert "window.dashboardEnsureCsrf&&typeof window.dashboardEnsureCsrf==='function'" in html
    assert "headers['X-CSRF-Token']=csrf" in html
    assert "const opts={method:'POST',headers,body:JSON.stringify(payload||{})};" in html
    assert "if(signal) opts.signal=signal;" in html
    assert "Endpoint returned a non-JSON response" in html

    # Definition + seven Prompt Studio POST callers.
    assert html.count("promptStudioJsonPost(") == 8


def test_prompt_studio_direct_prompt_fetches_are_removed_but_payload_shapes_remain():
    html = _html()

    assert "fetch('/api/prompt/" not in html
    assert "fetch('/api/studio/improve" not in html

    assert "promptStudioJsonPost('/api/studio/improve',payload,window._improveAbort.signal)" in html
    assert "promptStudioJsonPost('/api/prompt/improve',{" in html
    assert "promptStudioJsonPost('/api/prompt/brainstorm',{" in html
    assert "promptStudioJsonPost('/api/prompt/tweak',{domain:promptStudioContext.domain" in html
    assert "promptStudioJsonPost('/api/prompt/commit',{path,content,message,branch:'main'},window._ghSyncAbort.signal)" in html
    assert "promptStudioJsonPost('/api/prompt/commit',{path,content,message,branch:'main'},window._htmlApplyAbort.signal)" in html
    assert "promptStudioJsonPost('/api/prompt/palette',{url,maxColors:10},window._paletteAbort.signal)" in html

    # Critical provider payload shape for /api/prompt/tweak must stay UI-compatible.
    assert "htmlDownloadUrl:htmlFile.download" in html
    assert "improvedPrompt:improved" in html
    assert "model:selectedModel||'google/gemini-2.5-flash'" in html
    assert "latestOnly:true" in html
