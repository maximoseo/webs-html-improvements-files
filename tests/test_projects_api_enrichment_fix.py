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
    assert "progress:metaProgressNumber" in html
    assert "starred:normalizeMetaFlag(meta.starred)" in html
    assert "deployed:normalizeMetaFlag(meta.deployed)" in html
    assert "const isStarred = !!p.starred" in html
    assert "const progressVal = p.progress || 25" not in html
    assert "deployed:!!meta.deployed" not in html
    assert "starred:!!meta.starred" not in html


def test_projects_boolean_metadata_normalizes_string_flags():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_BOOLEAN_METADATA_NORMALIZATION_FIX_2026_05_01" in html
    assert "const normalizeMetaFlag=value=>" in html
    assert "value===true||value===1" in html
    assert "['true','1','yes','y'].includes(value.trim().toLowerCase())" in html
    assert "normalizeMetaFlag(meta.deployed)" in html
    assert "normalizeMetaFlag(meta.starred)" in html


def test_projects_progress_accepts_numeric_strings_without_blank_zero_coercion():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_PROGRESS_NUMERIC_STRING_FIX_2026_05_01" in html
    assert "const metaProgressRaw=meta.progress;" in html
    assert "typeof metaProgressRaw==='number'&&Number.isFinite(metaProgressRaw)" in html
    assert "typeof metaProgressRaw==='string'&&metaProgressRaw.trim()!==''" in html
    assert "Number.isFinite(Number(metaProgressRaw))?Number(metaProgressRaw):null" in html


def test_projects_progress_preserves_zero_and_clamps_width():
    html = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_PROJECTS_PROGRESS_ZERO_CLAMP_FIX_2026_05_01" in html
    assert "const rawProgress = (typeof p.progress === 'number' && Number.isFinite(p.progress)) ? p.progress : 25;" in html
    assert "const progressVal = Math.max(0, Math.min(100, rawProgress));" in html
    assert "Progress: ${progressVal}%" in html
    assert "width:${progressVal}%" in html
