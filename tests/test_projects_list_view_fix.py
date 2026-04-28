from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX_HTML = ROOT / 'index.html'


def html():
    return INDEX_HTML.read_text(encoding='utf-8')


def test_projects_list_view_has_compact_row_marker_and_guards():
    s = html()
    assert 'PROJECTS_LIST_VIEW_COMPACT_FIX_2026_04_27' in s
    assert '#projects-grid.projects-grid.list-view .project-card' in s
    assert '#projects-grid.projects-grid.list-view .project-card:not(.expanded) .card-header' in s
    assert '#projects-grid.projects-grid.list-view .project-card:not(.expanded) .card-info' in s
    assert '#projects-grid.projects-grid.list-view .project-card:not(.expanded) .card-actions' in s
    assert '@media(max-width:768px)' in s


def test_set_view_marks_body_state_and_scopes_active_buttons():
    s = html()
    assert "document.body.classList.toggle('projects-list-view-active', mode === 'list')" in s
    assert "document.body.classList.toggle('projects-grid-view-active', mode !== 'list')" in s
    assert "btn.closest('.view-toggle')" in s
    assert re.search(r"grid\.className\s*=\s*'projects-grid'\s*\+\s*\(mode === 'list'", s)


def test_projects_list_view_is_not_only_grid_template_columns():
    s = html()
    start = s.find('<style id="projects-list-view-compact-fix-2026-04-27">')
    assert start != -1
    block = s[start:start+5000]
    for needle in ['display:flex', 'align-items:center', 'min-height:auto', 'grid-template-columns:1fr']:
        assert needle in block
