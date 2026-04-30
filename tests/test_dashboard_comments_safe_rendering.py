from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def _block_between(start_marker: str, end_marker: str) -> str:
    text = _index()
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    return text[start:end]


def test_comments_renderer_has_safe_dom_marker_and_helpers():
    text = _index()
    assert "DASHBOARD_XSS_FIX_COMMENTS_SAFE_RENDER_2026_04_30" in text
    assert "function createCommentEmptyState" in text
    assert "function createCommentItem" in text
    assert "function setCommentText" in text


def test_render_comments_list_does_not_template_api_values_with_innerhtml():
    block = _block_between("function renderCommentsList", "async function loadComments")
    assert "innerHTML" not in block
    assert "insertAdjacentHTML" not in block
    assert "replaceChildren" in block
    assert "createCommentItem(item)" in block


def test_comment_item_uses_text_nodes_not_html_interpolation():
    block = _block_between("function createCommentItem", "function renderCommentsList")
    assert "setCommentText(" in block
    assert "innerHTML" not in block
    assert "insertAdjacentHTML" not in block
    assert "escapeHtml" not in block  # escaping should be unnecessary because DOM text nodes are used


def test_load_comments_loading_state_uses_safe_empty_state_helper():
    block = _block_between("async function loadComments", "async function saveComment")
    assert "list.innerHTML='<div class=\"comments-empty\">Loading comments…</div>'" not in block
    assert "list.replaceChildren(createCommentEmptyState('Loading comments…'))" in block
