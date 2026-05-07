from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _html() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_plan23_active_prompt_status_ui_contract_exists():
    html = _html()

    assert "PLAN23_ACTIVE_PROMPT_STATUS_UI_2026_05_07" in html
    assert "id=\"ps-active-prompt-status\"" in html
    assert "id=\"ps-active-prompt-check-btn\"" in html
    assert "onclick=\"checkPlan23ActivePromptStatus()\"" in html
    assert "Method B read-only API" in html
    assert "readOnlyN8n=true" in html
    assert "mutatesWorkflow=false" in html


def test_plan23_active_prompt_status_uses_read_only_get_and_authed_fetch():
    html = _html()

    assert "async function checkPlan23ActivePromptStatus(opts){" in html
    assert "const fetcher=window.authedFetch||fetch;" in html
    assert "fetcher('/api/prompts/active?domain='+encodeURIComponent(domain),{method:'GET'})" in html
    assert "promptStudioJsonPost('/api/prompts/active" not in html
    assert "fetch('/api/prompts/active" not in html


def test_plan23_active_prompt_status_handles_active_missing_invalid_without_html_injection():
    html = _html()

    assert "function setPlan23ActivePromptStatus(kind,message,detail){" in html
    assert "status.textContent=message||'';" in html
    assert "detailEl.textContent=detail||'';" in html
    assert ".innerHTML" not in html[html.find("function setPlan23ActivePromptStatus"):html.find("async function checkPlan23ActivePromptStatus")]

    assert "Active prompt available" in html
    assert "No active prompt saved yet" in html
    assert "Invalid domain for active prompt lookup" in html
    assert "Plan #23 lookup failed" in html


def test_plan23_active_prompt_status_autoloads_from_improve_workflow_form():
    html = _html()

    assert "ps-iw-main-url" in html
    assert "main.addEventListener('change',function(){checkPlan23ActivePromptStatus({silent:false});});" in html
    assert "window.checkPlan23ActivePromptStatus&&window.checkPlan23ActivePromptStatus({silent:true});" in html
    assert "promptStudioContext.activePromptStatus" in html
