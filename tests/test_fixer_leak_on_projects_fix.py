from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'


def test_fixer_leak_guard_marker_and_scope():
    html = INDEX.read_text(encoding='utf-8')
    assert 'DASHBOARD_QA_FIX_FIXER_LEAK_ON_PROJECTS_2026_04_28' in html
    assert 'id="fixer-leak-on-projects-fix-2026-04-28"' in html
    assert 'body:not(.page-fixer-active) #fixer-analyze-btn' in html
    assert 'body:not(.page-fixer-active) #fixer-triple-btn' in html
    assert 'body:not(.page-fixer-active) #fixer-history' in html
    assert 'body.page-fixer-active #fixer-analyze-btn > svg' in html


def test_fixer_leak_guard_preserves_navigation_by_wrapping_show_page():
    html = INDEX.read_text(encoding='utf-8')
    assert 'window.showPage.__fixerLeakGuarded' in html
    assert 'var original = window.showPage;' in html
    assert 'original.apply(this, arguments)' in html
    assert "document.body.classList.toggle('page-fixer-active'" in html


def test_fixer_leak_guard_is_global_for_all_non_fixer_tabs():
    html = INDEX.read_text(encoding='utf-8')
    # The selector is body-state based, not Projects-only, so it applies to
    # Radar, KWR, Tasks, Analytics, Improvements, Productivity, Settings, etc.
    assert 'body:not(.page-fixer-active) #fixer-analyze-btn' in html
    assert 'body:not(.page-fixer-active) #fixer-triple-btn' in html
    assert 'body:not(.page-fixer-active) #fixer-history' in html
    assert 'isFixer = name === \'fixer\'' in html
    assert "setFixerBodyState('projects')" in html
