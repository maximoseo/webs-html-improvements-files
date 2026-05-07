from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = (ROOT / "index.html").read_text(encoding="utf-8")


def test_dashboard_exposes_named_authed_fetch_helper_for_phase04_migration():
    """Phase 04 needs a stable helper before fetch callsites are migrated."""
    assert "DASHBOARD_AUTHED_FETCH_HELPER_2026_05_07" in INDEX
    assert "window.authedFetch = function(url, opts){" in INDEX
    assert "return _dashboardFetch(url, opts);" in INDEX
    assert "window.fetch = window.authedFetch;" in INDEX


def test_fetch_json_uses_authed_fetch_instead_of_raw_fetch():
    start = INDEX.find("async function fetchJSON(url){")
    assert start != -1, "fetchJSON helper not found"
    end = INDEX.find("\n}\n\n// Agent hide/show", start)
    assert end != -1, "fetchJSON block boundary not found"
    block = INDEX[start:end]
    assert "const fetcher=window.authedFetch||fetch;" in block
    assert "const r=await fetcher(url);" in block
    assert "const r=await fetch(url);" not in block
