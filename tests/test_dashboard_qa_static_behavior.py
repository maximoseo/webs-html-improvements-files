from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def test_tasks_reparent_logic_is_before_page_display_toggles():
    reparent_idx = HTML.index('DASHBOARD_QA_FIX_TASKS_REPARENT_2026_04_27')
    display_idx = HTML.index("tasksPage.style.display = isTask ? 'block' : 'none'")
    assert reparent_idx < display_idx
    assert "tasksPage.parentElement.id === 'page-radar'" in HTML
    assert 'mainContent.appendChild(tasksPage);' in HTML


def test_navigation_body_state_classes_are_set_from_showpage_booleans():
    showpage_idx = HTML.index('window.showPage = function(name)')
    kwr_idx = HTML.index("document.body.classList.toggle('page-kwr-active', isKwr);")
    tasks_idx = HTML.index("document.body.classList.toggle('page-tasks-active', isTask);")
    assert showpage_idx < kwr_idx < HTML.index('const container = document.querySelector')
    assert showpage_idx < tasks_idx < HTML.index('const container = document.querySelector')


def test_kwr_history_hidden_by_default_and_only_body_state_reveals_it():
    assert 'body:not(.page-kwr-active) #kwr-history-panel{display:none !important;}' in HTML
    assert 'body.page-kwr-active #kwr-history-panel' in HTML
    # Guard against the baseline bug: an unconditional global full-bleed show rule in the QA block.
    qa_block = HTML.split('<style id="dashboard-qa-fix-pass-2026-04-27">', 1)[1].split('</style>', 1)[0]
    assert '#kwr-history-panel{display:block' not in qa_block.replace(' ', '')


def test_tour_cleanup_removes_all_overlay_node_types():
    cleanup = HTML.split('<script id="dashboard-qa-fix-tour-cleanup-2026-04-27">', 1)[1].split('</script>', 1)[0]
    for selector in ['.tour-spotlight,.tour-tooltip', '#tour-backdrop,.tour-backdrop,.tour-overlay']:
        assert f"document.querySelectorAll('{selector}')" in cleanup
    assert 'el.remove();' in cleanup
    assert 'window.dismissTour = function(markDone)' in cleanup
    assert "data-act" in cleanup


def test_dropdown_readability_selectors_are_in_final_qa_block():
    qa_block = HTML.split('<style id="dashboard-qa-fix-pass-2026-04-27">', 1)[1].split('</style>', 1)[0]
    for selector in ['select option', '[role="listbox"]', '[role="option"]', '[role="menuitem"]']:
        assert selector in qa_block
