import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def _qa_block():
    return HTML.split('<style id="dashboard-qa-fix-pass-2026-04-27">', 1)[1].split('</style>', 1)[0]


def test_projects_view_toggle_uses_scoped_active_state_not_global_view_btn_clear():
    fn = HTML.split('function setView(mode,btn){', 1)[1].split('\n}', 1)[0]
    assert 'DASHBOARD_QA_FIX_VIEW_TOGGLE_SCOPE_2026_04_27' in HTML
    assert "btn.closest('.view-toggle')" in fn
    assert 'document.querySelectorAll(\'.view-btn\').forEach' not in fn
    assert "mode==='list'?' list-view':''" in fn


def test_tasks_view_toggle_uses_scoped_active_state_not_global_task_btn_clear():
    fn = HTML.split('function setTaskView(view, btn) {', 1)[1].split('\n}', 1)[0]
    assert 'DASHBOARD_QA_FIX_TASK_VIEW_TOGGLE_SCOPE_2026_04_27' in HTML
    assert "btn.closest('.tasks-view-toggle')" in fn
    assert "document.querySelectorAll('.tasks-view-btn').forEach" not in fn
    assert "view==='board'?'block':'none'" in fn


def test_view_toggle_active_state_is_visually_distinct_in_final_qa_block():
    css = _qa_block()
    assert 'DASHBOARD_QA_FIX_VIEW_TOGGLE_ACTIVE_VISUAL_2026_04_27' in css
    assert '.view-toggle .view-btn.active' in css
    assert '.tasks-view-toggle .tasks-view-btn.active' in css
    active_block = re.search(r'\.view-toggle\s+\.view-btn\.active\s*,\s*\.tasks-view-toggle\s+\.tasks-view-btn\.active\s*\{(?P<body>[^}]+)\}', css, re.S)
    assert active_block, 'active view toggle CSS block missing'
    body = active_block.group('body')
    for expected in ['background:', 'border-color:', 'color:#fff', 'box-shadow:']:
        assert expected in body
    assert 'rgba(74,163,255,0.28)' in body or 'linear-gradient' in body


def test_projects_list_view_has_late_css_that_changes_actual_layout_not_only_button_state():
    css = _qa_block()
    assert 'DASHBOARD_QA_FIX_PROJECTS_LIST_VIEW_LAYOUT_2026_04_27' in css
    list_block = re.search(r'#projects-grid\.projects-grid\.list-view\s*\{(?P<body>[^}]+)\}', css, re.S)
    assert list_block, 'late projects list-view layout override missing'
    body = list_block.group('body')
    assert 'grid-template-columns:1fr!important' in body.replace(' ', '')
    assert 'max-width:' in body
    card_block = re.search(r'#projects-grid\.projects-grid\.list-view\s+\.project-card\s*\{(?P<body>[^}]+)\}', css, re.S)
    assert card_block, 'list-view project-card row styling missing'
    assert 'grid-column:auto!important' in card_block.group('body').replace(' ', '')


def test_tasks_board_and_list_views_have_explicit_late_visibility_guards():
    css = _qa_block()
    assert 'DASHBOARD_QA_FIX_TASK_VIEW_LAYOUT_SWITCH_2026_04_27' in css
    assert '#tasks-list-view' in css
    assert '#tasks-board-view' in css
    assert 'body.page-tasks-active #tasks-list-view' in css
    assert 'body.page-tasks-active #tasks-board-view' in css


def test_native_select_options_have_dark_readable_popup_styles_across_dashboard():
    css = _qa_block()
    assert 'DASHBOARD_QA_FIX_NATIVE_SELECT_OPTION_READABILITY_2026_04_27' in css
    required_selectors = [
        '#main-content select',
        '.header select',
        '#main-content select option',
        '.header select option',
        '#main-content select optgroup',
        '.header select optgroup',
        '.fixer-select option',
        '.tasks-filter-sel option',
        '.task-select option',
        '.search-box option',
        '.settings-input option',
        '#projects-sort option',
    ]
    for selector in required_selectors:
        assert selector in css
    options_block = re.search(r'#main-content\s+select\s+option\s*,.*?#projects-sort\s+option\s*\{(?P<body>[^}]+)\}', css, re.S)
    assert options_block, 'global native option readability block missing'
    body = options_block.group('body')
    assert 'background:#111827' in body or 'background:var(--surface-strong' in body
    assert 'color:#f8fafc' in body or 'color:var(--text' in body
