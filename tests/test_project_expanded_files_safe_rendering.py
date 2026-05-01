from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _html() -> str:
    return INDEX.read_text(encoding="utf-8")


def _versions_renderer_block() -> str:
    html = _html()
    start = html.index("versionsHTML=Object.entries(versionsByAgent).map")
    end = html.index("    const _psAgent=", start)
    return html[start:end]


def test_expanded_project_file_rows_escape_display_text_and_attrs():
    html = _html()
    block = _versions_renderer_block()

    assert "PROJECT_EXPANDED_FILE_ROWS_SAFE_RENDER_ESCAPE_2026_05_01" in html
    assert "function projectCardText(value){" in html
    assert "function projectActionAttr(value){" in html

    # File row display values come from repo/API metadata and must not be raw
    # interpolated into parsed HTML text nodes.
    assert "const _fileNameText=projectCardText(f.name);" in block
    assert "const _fileSizeText=projectCardText(formatSize(f.size));" in block
    assert '<div class="file-name">${_fileNameText}</div>' in block
    assert '<div class="file-size">${_fileSizeText}</div>' in block
    assert '<div class="file-name">${f.name}</div>' not in block
    assert '<div class="file-size">${formatSize(f.size)}</div>' not in block

    # Agent grouping attributes/text also come from version names via detectAgent.
    assert "const _agentText=projectCardText(agentName);" in block
    assert "const _agentAttr=projectActionAttr(agentName);" in block
    assert "const _projectNameDataAttr=projectActionAttr(p.name);" in block
    assert 'data-domain="${_projectNameDataAttr}"' in block
    assert 'data-agent="${_agentAttr}"' in block
    assert '<strong>${_agentText}</strong>' in block
    assert 'data-domain="${p.name}"' not in block
    assert 'data-agent="${agentName.replace(/\\"/g,\'&quot;\')}"' not in block
    assert '<strong>${agentName}</strong>' not in block


def test_expanded_project_version_titles_escape_display_text():
    block = _versions_renderer_block()

    assert "const _versionTitleText=projectCardText(v.date||v.name);" in block
    assert '<span class="version-title">${_versionTitleText} <span class="v-badge">&#x2605; Latest</span></span>' in block
    assert '<span class="version-title">${v.date||v.name} <span class="v-badge">&#x2605; Latest</span></span>' not in block


def test_expanded_project_bulk_bar_uses_escaped_domain_attr():
    block = _versions_renderer_block()

    assert 'data-domain-bar="${_projectNameDataAttr}"' in block
    assert 'data-domain-bar="${p.name}"' not in block
