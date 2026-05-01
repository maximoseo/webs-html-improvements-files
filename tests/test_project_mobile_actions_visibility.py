from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')

MARKER = 'PROJECT_MOBILE_ACTIONS_VISIBLE_FIX_2026_05_01'


def _marker_block():
    assert MARKER in HTML
    start = HTML.index(MARKER)
    end = HTML.index('</style>', start)
    return HTML[start:end]


def test_mobile_project_quick_actions_have_visible_touch_guard_marker():
    block = _marker_block()
    assert '@media(max-width:640px),(hover:none) and (pointer:coarse)' in block
    assert '.project-card .star-btn' in block
    assert '.project-card .card-actions' in block


def test_mobile_project_quick_actions_override_hover_only_opacity():
    block = _marker_block()
    assert 'opacity:1!important' in block
    assert 'visibility:visible!important' in block
    assert 'pointer-events:auto!important' in block
    assert 'min-width:44px!important' in block
    assert 'min-height:44px!important' in block


def test_mobile_project_action_menu_stays_inside_card_on_small_screens():
    block = _marker_block()
    assert '.project-card .action-menu' in block
    assert 'right:0!important' in block
    assert 'max-width:calc(100vw - 32px)!important' in block
    assert 'z-index:50!important' in block


def test_desktop_hover_contract_is_still_present():
    assert '.card-actions{position:absolute;top:8px;right:8px;opacity:0;transition:opacity .2s}' in HTML
    assert '.project-card:hover .card-actions{opacity:1}' in HTML
    assert '.star-btn{position:absolute;top:8px;left:8px;background:none;border:none;font-size:1.1rem;cursor:pointer;opacity:0;transition:opacity .2s;color:#475569}' in HTML
    assert '.project-card:hover .star-btn{opacity:1}' in HTML
