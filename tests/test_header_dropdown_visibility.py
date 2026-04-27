from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def _block(style_id: str) -> str:
    marker = f'<style id="{style_id}">'
    assert marker in HTML
    return HTML.split(marker, 1)[1].split('</style>', 1)[0]


def test_header_dropdown_visibility_fix_marker_exists():
    block = _block('header-dropdown-visibility-fix-2026-04-27')
    assert 'HEADER_DROPDOWN_VISIBILITY_FIX_2026_04_27' in block


def test_header_overflow_dropdown_escapes_header_stacking_and_clipping():
    block = _block('header-dropdown-visibility-fix-2026-04-27')
    assert '.header .hdr-overflow-wrap.open .hdr-overflow-dropdown' in block
    assert 'position:fixed !important;' in block
    assert 'z-index:30000 !important;' in block
    assert '.mobile-drawer.open' in block
    assert 'z-index:30020 !important;' in block
    assert 'overflow:visible !important;' in block
    assert 'max-height:calc(100vh - 96px) !important;' in block
    assert 'overflow-y:auto !important;' in block


def test_header_dropdown_button_updates_aria_expanded():
    assert 'HEADER_DROPDOWN_VISIBILITY_FIX_JS_2026_04_27' in HTML
    assert "btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');" in HTML
    assert "btn.setAttribute('aria-controls', 'hdr-overflow-dropdown');" in HTML
    assert "btn.setAttribute('aria-expanded', 'false');" in HTML
