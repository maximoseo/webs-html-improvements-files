import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')


def test_performance_radar_tabs_use_scoped_handler_not_colliding_switch_radar_tab():
    assert 'DASHBOARD_FILTER_FIX_PERFORMANCE_RADAR_TAB_SCOPE_2026_04_27' in HTML
    assert 'function switchPerformanceRadarTab(tabId, btnElement)' in HTML
    for tab_id in ['radar-tab-scores', 'radar-tab-trends', 'radar-tab-ai', 'radar-tab-reports', 'radar-tab-export']:
        assert f"switchPerformanceRadarTab('{tab_id}', this)" in HTML
        assert f"switchRadarTab('{tab_id}', this)" not in HTML


def test_daily_skills_radar_switch_radar_tab_still_exists_for_results_tabs():
    assert re.search(r'function\s+switchRadarTab\s*\(\s*tab\s*\)', HTML), 'Daily Skills Radar status tab switcher should remain available'
    fn = HTML.split('function switchRadarTab(tab) {', 1)[1].split('\n}', 1)[0]
    assert "radarActiveTab = tab" in fn
    assert "loadRadarResults(tab)" in fn


def test_performance_radar_scoped_handler_changes_visible_tab_content():
    fn = HTML.split('function switchPerformanceRadarTab(tabId, btnElement) {', 1)[1].split('\n}', 1)[0]
    assert "document.querySelectorAll('.radar-tab-content').forEach" in fn
    assert "document.querySelectorAll('.radar-inner-tab-btn').forEach" in fn
    assert "var targetTab = document.getElementById(tabId)" in fn
    assert "if (!targetTab) return" in fn
    assert "targetTab.style.display = 'block'" in fn
    assert "if (!btnElement) return" in fn
    assert "btnElement.classList.add('active')" in fn
