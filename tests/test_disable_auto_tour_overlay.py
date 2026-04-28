from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'


def test_disable_auto_tour_overlay_marker_and_persistence():
    html = INDEX.read_text(encoding='utf-8')
    assert 'DASHBOARD_QA_FIX_DISABLE_AUTO_TOUR_OVERLAY_2026_04_28' in html
    assert 'id="disable-auto-tour-overlay-fix-2026-04-28"' in html
    assert "localStorage.setItem('dash-tour-done-v2','1')" in html
    assert "sessionStorage.setItem('dash-tour-done-v2','1')" in html
    assert 'dash_tour_done=1' in html


def test_disable_auto_tour_overlay_hides_without_user_started_class():
    html = INDEX.read_text(encoding='utf-8')
    assert 'body:not(.tour-user-started) #tour-backdrop.open' in html
    assert 'cleanupAutoTour()' in html
    assert 'window.__tourActive=false' in html
    assert "document.body.classList.contains('tour-user-started')" in html
    assert 'window.startTour=function()' in html
