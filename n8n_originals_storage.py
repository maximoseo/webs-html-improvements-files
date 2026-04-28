import json
from pathlib import Path

from n8n_template_extractor import extract_html_nodes, identify_domain, sanitize_filename_part


def _unique_path(path):
    path = Path(path)
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for idx in range(2, 10000):
        candidate = path.with_name(f'{stem}-copy-{idx}{suffix}')
        if not candidate.exists():
            return candidate
    raise RuntimeError(f'Could not allocate unique path for {path}')


def store_original_workflow(root, workflow, date):
    """Store one original workflow and extracted HTML nodes additively.

    This never overwrites an existing original file. If the deterministic filename
    exists, a -copy-N suffix is used.
    """
    root = Path(root)
    info = identify_domain(workflow)
    domain = sanitize_filename_part(info.get('primary_domain') or 'uncategorized')
    workflow_name = sanitize_filename_part(workflow.get('name') or workflow.get('id') or 'workflow')
    workflow_id = str(workflow.get('id') or '')

    base = root / 'n8n-sync' / 'originals' / domain
    workflows_dir = base / 'workflows'
    html_dir = base / 'html-nodes'
    workflows_dir.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)

    workflow_path = _unique_path(workflows_dir / f'{workflow_name}-original-{date}.json')
    workflow_path.write_text(json.dumps(workflow, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')

    html_records = []
    for idx, html_node in enumerate(extract_html_nodes(workflow), start=1):
        node_name = sanitize_filename_part(html_node.get('node_name') or f'html-node-{idx}')
        html_path = _unique_path(html_dir / f'{node_name}-original-{date}.html')
        html_path.write_text(html_node.get('html_content') or '', encoding='utf-8')
        record = dict(html_node)
        record['path'] = html_path.relative_to(root).as_posix()
        html_records.append(record)

    return {
        'workflow_id': workflow_id,
        'workflow_name': workflow.get('name') or workflow_id or 'Unnamed workflow',
        'domain': domain,
        'workflow_path': workflow_path.as_posix(),
        'html_node_paths': [str((root / r['path']).resolve()) for r in html_records],
        'html_nodes': html_records,
    }


def build_indexes(root, records, date):
    root = Path(root)
    index_dir = root / 'n8n-sync' / 'indexes'
    index_dir.mkdir(parents=True, exist_ok=True)

    workflow_index = index_dir / '_index.md'
    html_index = index_dir / '_html-templates-index.md'

    lines = [
        '# n8n Workflow Originals Index',
        '',
        f'Date: {date}',
        '',
        '| Domain | Workflow | Workflow ID | Original JSON | HTML Nodes |',
        '|---|---|---|---|---|',
    ]
    html_lines = [
        '# n8n HTML Templates Index',
        '',
        f'Date: {date}',
        '',
        '| Domain | Workflow | Node | Source | Original HTML |',
        '|---|---|---|---|---|',
    ]

    for record in sorted(records, key=lambda r: (r.get('domain', ''), r.get('workflow_name', ''))):
        workflow_rel = _relative_display_path(root, record.get('workflow_path', ''))
        html_count = len(record.get('html_nodes') or [])
        lines.append(
            f"| {record.get('domain','')} | {record.get('workflow_name','')} | {record.get('workflow_id','')} | `{workflow_rel}` | {html_count} |"
        )
        for node in record.get('html_nodes') or []:
            html_lines.append(
                f"| {record.get('domain','')} | {record.get('workflow_name','')} | {node.get('node_name','')} | {node.get('source','')} | `{node.get('path','')}` |"
            )

    workflow_index.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    html_index.write_text('\n'.join(html_lines) + '\n', encoding='utf-8')
    return {'workflow_index': workflow_index.as_posix(), 'html_index': html_index.as_posix()}


def _relative_display_path(root, value):
    try:
        return Path(value).resolve().relative_to(Path(root).resolve()).as_posix()
    except Exception:
        return str(value)
