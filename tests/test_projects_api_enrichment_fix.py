from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_projects_api_enrichment_supports_fetchjson_wrapped_payload():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_API_ENRICHMENT_FIX_2026_05_01" in html
    assert "const apiPayload = apiRes && apiRes.data ? apiRes.data : apiRes;" in html
    assert "Array.isArray(apiPayload.projects)" in html
    assert "apiPayload.projects.forEach(proj => { apiProjects[proj.name] = proj; });" in html


def test_projects_api_enrichment_no_longer_reads_projects_from_fetchjson_wrapper_directly():
    html = INDEX.read_text(encoding="utf-8")
    broken = "if (apiRes && apiRes.ok && apiRes.projects)"
    assert broken not in html


def test_projects_api_enrichment_metadata_passes_through_to_cards():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_METADATA_PASS_THROUGH_2026_05_01" in html
    assert "progress:typeof meta.progress==='number'?meta.progress:null" in html
    assert "starred:!!meta.starred" in html
    assert "const isStarred = !!p.starred" in html
    assert "const progressVal = p.progress || 25" not in html


def test_projects_progress_preserves_zero_and_clamps_width():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_PROGRESS_ZERO_CLAMP_FIX_2026_05_01" in html
    assert "const rawProgress = (typeof p.progress === 'number' && Number.isFinite(p.progress)) ? p.progress : 25;" in html
    assert "const progressVal = Math.max(0, Math.min(100, rawProgress));" in html
    assert "Progress: ${progressVal}%" in html
    assert "width:${progressVal}%" in html
