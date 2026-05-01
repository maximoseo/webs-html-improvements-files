from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def test_project_action_menu_buttons_pass_event_and_expose_aria_state():
    assert 'PROJECT_CARD_ACTION_MENU_A11Y_FIX_2026_05_01' in HTML
    assert "toggleActionMenu('${p.name}',this,event)" in HTML
    assert 'aria-haspopup="menu"' in HTML
    assert 'aria-expanded="false"' in HTML
    assert 'aria-controls="menu-${p.name}"' in HTML
    assert '<div class="action-menu" id="menu-${p.name}" role="menu" aria-hidden="true">' in HTML
    assert 'role="menuitem"' in HTML


def test_toggle_action_menu_does_not_depend_on_global_window_event():
    start = HTML.index('function closeProjectActionMenus')
    block = HTML[start:HTML.index('async function duplicateProject', start)]
    fn = HTML[HTML.index('function toggleActionMenu(domain, btn', start):HTML.index('document.addEventListener', start)]
    assert 'function toggleActionMenu(domain, btn, ev)' in fn
    assert 'if(ev&&ev.stopPropagation) ev.stopPropagation();' in fn
    assert 'event.stopPropagation();' not in fn
    assert "m.setAttribute('aria-hidden','true')" in block
    assert "b.setAttribute('aria-expanded','false')" in block
    assert "btn.setAttribute('aria-expanded', show ? 'true' : 'false')" in fn
    assert "menu.setAttribute('aria-hidden', show ? 'false' : 'true')" in fn


def test_document_click_closes_project_action_menus_and_resets_aria():
    start = HTML.index('function closeProjectActionMenus')
    block = HTML[start:HTML.index('async function duplicateProject', start)]
    assert "document.addEventListener('click', closeProjectActionMenus);" in block
    assert "document.querySelectorAll('.action-menu.show').forEach" in block
    assert "document.querySelectorAll('.card-actions .action-btn[aria-expanded=\"true\"]').forEach" in block
