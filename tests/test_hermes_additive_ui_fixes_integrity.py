from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _html() -> str:
    return INDEX.read_text(encoding="utf-8")


def test_hermes_additive_ui_fix_block_is_not_duplicated_or_embedded_in_fallback_strings():
    html = _html()
    marker = "HERMES ADDITIVE FIXES FOR ROUTING & UI/UX (V4)"

    assert html.count(marker) == 1
    assert html.count('id="hermes-additive-ui-fixes"') == 1
    assert html.count('id="hermes-additive-routing-fix"') == 1

    # Regression for commit 014435b: an automated insertion placed the full
    # additive block inside several JS fallback strings, creating literal
    # </script> tags inside the main inline script and breaking dashboard JS.
    assert "Failed to load preview. The file may be missing or the network request failed.<br><br><a" in html
    assert "</a>\n\n</body>" not in html
    assert "preview.\n\n</body>" not in html
    assert "Preview unavailable.\n\n</body>" not in html
    first_marker = html.index(marker)
    final_body = html.rindex("</body>")
    assert first_marker < final_body


def test_hermes_additive_ui_fix_block_is_kept_near_document_end_only():
    html = _html()
    marker = "HERMES ADDITIVE FIXES FOR ROUTING & UI/UX (V4)"
    marker_line = html[: html.index(marker)].count("\n") + 1
    total_lines = html.count("\n") + 1

    # The additive block is intended as a late override, not as content inside
    # Preview/Prompt Studio fallback HTML strings around the main script body.
    assert total_lines - marker_line < 300
