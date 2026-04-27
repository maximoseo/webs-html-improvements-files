import argparse
import datetime as dt
import json
from pathlib import Path

from n8n_originals_storage import build_indexes, store_original_workflow
from n8n_readonly_client import N8NReadOnlyClient


def sync_originals(root, client, date=None, max_workflows=None):
    date = date or dt.datetime.utcnow().strftime('%Y-%m-%d')
    summaries = client.get_all_workflows()
    if max_workflows is not None:
        summaries = summaries[: int(max_workflows)]
    records = []
    for summary in summaries:
        workflow_id = summary.get('id')
        if not workflow_id:
            continue
        detail = client.get_workflow_detail(workflow_id)
        records.append(store_original_workflow(Path(root), detail, date=date))
    indexes = build_indexes(Path(root), records, date=date)
    manifest = {
        'ok': True,
        'date': date,
        'workflow_count': len(records),
        'html_node_count': sum(len(r.get('html_nodes') or []) for r in records),
        'indexes': indexes,
        'records': records,
        'safety': 'n8n API GET-only; originals stored as additive reference copies',
    }
    manifest_path = Path(root) / 'n8n-sync' / 'sync-manifest.json'
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    manifest['manifest_path'] = manifest_path.as_posix()
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Read-only n8n originals sync')
    parser.add_argument('--root', default='.', help='Repository/root folder for n8n-sync output')
    parser.add_argument('--max-workflows', type=int, default=None, help='Optional limit for cautious sample sync')
    args = parser.parse_args()
    result = sync_originals(Path(args.root), N8NReadOnlyClient(), max_workflows=args.max_workflows)
    print(json.dumps({
        'ok': result['ok'],
        'workflow_count': result['workflow_count'],
        'html_node_count': result['html_node_count'],
        'manifest_path': result['manifest_path'],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
