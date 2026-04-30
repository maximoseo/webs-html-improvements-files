import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def _kwr_reports_block() -> str:
    text = _index()
    start = text.index("window.kwrFetchReports = async function")
    end = text.index("window.kwrDeleteReport = async function", start)
    return text[start:end]


def test_kwr_reports_renderer_has_safe_rendering_marker_and_dom_helpers():
    text = _index()
    assert "DASHBOARD_XSS_FIX_KWR_REPORTS_SAFE_RENDER_2026_04_30" in text
    assert "function kwrCreateReportCard" in text
    assert "function kwrEncodeRunIdForDownload" in text
    assert "function kwrSetText" in text


def test_kwr_fetch_reports_no_longer_renders_api_list_with_innerhtml_template():
    block = _kwr_reports_block()
    assert "grid.innerHTML = list.map" not in block
    assert "grid.replaceChildren" in block
    assert "kwrCreateReportCard(r)" in block


def test_kwr_report_card_uses_text_content_for_api_controlled_fields():
    text = _index()
    start = text.index("function kwrCreateReportCard")
    end = text.index("window.kwrFetchReports = async function", start)
    block = text[start:end]

    # API-controlled report values should be inserted through the text helper/attributes,
    # not interpolated into an HTML template.
    assert "kwrSetText(" in block
    assert "innerHTML" not in block
    assert "insertAdjacentHTML" not in block
    assert "onclick=" not in block
    assert "addEventListener('click'" in block or 'addEventListener("click"' in block


def test_kwr_flat_download_encoding_preserves_route_delimiter_colon():
    text = _index()
    start = text.index("function kwrEncodeRunIdForDownload")
    end = text.index("function kwrCreateReportCard", start)
    block = text[start:end]
    assert "flat:" in block
    assert "encodeURIComponent(String(runId).slice(5))" in block
    assert "'flat:' +" in block or '"flat:" +' in block
