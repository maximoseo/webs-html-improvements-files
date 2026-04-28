from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'index.html'


def test_projects_sort_filter_fix_markers_and_controls():
    html = INDEX.read_text(encoding='utf-8')
    assert 'DASHBOARD_QA_FIX_PROJECTS_SORT_FILTERS_2026_04_27' in html
    assert 'id="projects-sort-filter-fix-2026-04-27"' in html
    assert "controls.id='projects-controls-wrap'" in html
    assert "filterWrap.id='projects-filter-wrap'" in html
    assert '<option value="agents">Most agents</option>' in html
    assert '<option value="multi-agent">Multi-agent only</option>' in html
    assert '<option value="hermes">Hermes/model outputs</option>' in html


def test_projects_sort_filter_rehydrates_cards_and_wraps_dashboard_render():
    html = INDEX.read_text(encoding='utf-8')
    assert 'card.dataset.projectUpdated' in html
    assert 'card.dataset.projectAgents' in html
    assert 'card.dataset.projectSets' in html
    assert 'window.loadDashboard=async function()' in html
    assert 'ensureControls();applyProjectsSortFilter();return result;' in html
    assert 'window.filterProjects=function(q)' in html


def test_projects_sort_filter_has_stable_sort_modes_and_empty_state():
    html = INDEX.read_text(encoding='utf-8')
    assert "if(mode==='oldest')" in html
    assert "if(mode==='az')" in html
    assert "if(mode==='za')" in html
    assert "if(mode==='agents')" in html
    assert "return (bd-ad)||an.localeCompare(bn);" in html
    assert 'No projects match the current search/filter.' in html
