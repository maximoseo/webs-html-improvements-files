import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def test_qa_override_marker_exists():
    assert 'DASHBOARD_QA_FIX_PASS_2026_04_27' in HTML


def test_main_nav_does_not_clip_settings_tab():
    assert '#fixer-tab-nav' in HTML
    assert '#tab-settings' in HTML
    assert 'DASHBOARD_QA_FIX_NAV_NO_CLIP_2026_04_27' in HTML
    assert re.search(r'#fixer-tab-nav\s*\{[^}]*overflow-x\s*:\s*auto\s*!important', HTML, re.S)
    assert re.search(r'#tab-settings\s*\{[^}]*display\s*:\s*inline-flex\s*!important', HTML, re.S)


def test_kwr_history_panel_is_scoped_to_kwr_page_only():
    assert 'DASHBOARD_QA_FIX_KWR_HISTORY_SCOPE_2026_04_27' in HTML
    assert re.search(r'body:not\(\.page-kwr-active\)\s+#kwr-history-panel\s*\{[^}]*display\s*:\s*none\s*!important', HTML, re.S)
    assert re.search(r'body\.page-kwr-active\s+#kwr-history-panel\s*\{[^}]*display\s*:\s*block\s*!important', HTML, re.S)
    assert "document.body.classList.toggle('page-kwr-active', isKwr);" in HTML


def test_task_manager_page_has_forced_visible_active_layout():
    assert 'DASHBOARD_QA_FIX_TASKS_VISIBLE_2026_04_27' in HTML
    assert re.search(r'#page-tasks\.active\s*\{[^}]*display\s*:\s*block\s*!important', HTML, re.S)
    assert re.search(r'#page-tasks\.active\s*\{[^}]*width\s*:\s*auto\s*!important', HTML, re.S)
    assert re.search(r'#page-tasks\.active\s*\{[^}]*min-height\s*:\s*', HTML, re.S)
    assert 'DASHBOARD_QA_FIX_TASKS_REPARENT_2026_04_27' in HTML
    assert 'mainContent.insertBefore(tasksPage' in HTML or 'mainContent.appendChild(tasksPage' in HTML


def test_dropdown_listbox_option_readability_css_exists():
    assert 'DASHBOARD_QA_FIX_DROPDOWN_READABILITY_2026_04_27' in HTML
    for selector in ['[role="listbox"]', '[role="option"]', '[role="menuitem"]', 'select option']:
        assert selector in HTML


def test_tour_dismiss_cleanup_removes_tooltip_and_spotlight():
    assert 'DASHBOARD_QA_FIX_TOUR_CLEANUP_2026_04_27' in HTML
    assert 'function forceDismissDashboardTour' in HTML
    assert "document.querySelectorAll('.tour-spotlight,.tour-tooltip'" in HTML
    assert 'window.dismissTour = function' in HTML
