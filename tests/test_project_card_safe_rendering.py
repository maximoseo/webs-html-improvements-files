from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'index.html').read_text(encoding='utf-8')
MARKER = 'PROJECT_CARD_SAFE_RENDER_ESCAPE_2026_05_01'


def _render_projects_block() -> str:
    start = HTML.index('card.innerHTML=`')
    end = HTML.index('grid.appendChild(card);', start)
    # Include setup immediately before the template plus the full template body.
    return HTML[max(0, start - 2500):end]


def test_project_card_renderer_has_explicit_safe_render_marker_and_helpers():
    block = _render_projects_block()
    assert MARKER in block
    assert 'function projectCardText(value){return projectActionAttr(value).replace(/\'/g,\'&#39;\');}' in HTML
    for helper in (
        'const _projectNameText=projectCardText(p.name);',
        'const _projectNameAttr=projectActionAttr(p.name);',
        'const _projectNameArg=previewOnclickArg(p.name);',
        'const _lastUpdatedAttr=projectActionAttr(p.last_updated || \'\');',
        'const _projectDomainAttr=projectActionAttr(encodeURIComponent(p.domain||p.name));',
        'const _projectInitialsText=projectCardText(initials);',
    ):
        assert helper in block


def test_project_card_no_longer_interpolates_raw_project_name_into_html_or_handlers():
    block = _render_projects_block()
    unsafe_patterns = [
        "toggleStar('${p.name}',this,event)",
        "toggleActionMenu('${p.name}',this,event)",
        "duplicateProject('${p.name}')",
        "deleteProject('${p.name}')",
        'aria-label="${isStarred?\'Unstar\':\'Star\'} project ${p.name}"',
        'aria-controls="menu-${p.name}"',
        'id="menu-${p.name}"',
        '<h3>${p.name}</h3>',
        '<span class="icon-initials">${initials}</span>',
        'aria-label="Open project ${p.name}"',
        'title="${p.last_updated || \'\'}"',
    ]
    for pattern in unsafe_patterns:
        assert pattern not in block
    for safe_pattern in (
        "toggleStar('${_projectNameArg}',this,event)",
        "toggleActionMenu('${_projectNameArg}',this,event)",
        "duplicateProject('${_projectNameArg}')",
        "deleteProject('${_projectNameArg}')",
        'aria-label="${isStarred?\'Unstar\':\'Star\'} project ${_projectNameAttr}"',
        'aria-controls="menu-${_projectNameAttr}"',
        'id="menu-${_projectNameAttr}"',
        '<h3>${_projectNameText}</h3>',
        '<span class="icon-initials">${_projectInitialsText}</span>',
        'aria-label="Open project ${_projectNameAttr}"',
        'title="${_lastUpdatedAttr}"',
    ):
        assert safe_pattern in block


def test_project_card_favicon_and_icon_attributes_are_escaped():
    block = _render_projects_block()
    assert 'const _projectDomainAttr=projectActionAttr(encodeURIComponent(p.domain||p.name));' in block
    assert 'id="icon-${_projectIconId}"' in block
    assert 'src="https://www.google.com/s2/favicons?domain=${_projectDomainAttr}&sz=64"' in block
    assert 'id="icon-${p.name.replace(/[^a-z0-9]/gi,\'-\')}"' not in block
