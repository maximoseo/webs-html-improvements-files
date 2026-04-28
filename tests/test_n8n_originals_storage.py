import json
import tempfile
import unittest
from pathlib import Path

from n8n_originals_storage import store_original_workflow, build_indexes


class N8NOriginalsStorageTests(unittest.TestCase):
    def test_store_original_workflow_writes_additive_domain_structure(self):
        workflow = {
            'id': 'wf-1',
            'name': 'Newsletter for Example',
            'active': True,
            'nodes': [
                {'name': 'HTML Email', 'type': 'n8n-nodes-base.html', 'parameters': {'html': '<html><h1>{{$json.title}}</h1></html>'}}
            ],
            'tags': [{'name': 'example.com'}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            result = store_original_workflow(Path(tmp), workflow, date='2026-04-27')
            workflow_path = Path(result['workflow_path'])
            html_paths = [Path(p) for p in result['html_node_paths']]

            self.assertTrue(workflow_path.exists())
            self.assertIn('n8n-sync/originals/example.com/workflows', workflow_path.as_posix())
            self.assertTrue(workflow_path.name.endswith('-original-2026-04-27.json'))
            self.assertEqual(len(html_paths), 1)
            self.assertTrue(html_paths[0].exists())
            self.assertIn('{{$json.title}}', html_paths[0].read_text(encoding='utf-8'))

    def test_store_original_workflow_does_not_overwrite_existing_original(self):
        workflow = {'id': 'wf-1', 'name': 'Example', 'nodes': [], 'tags': [{'name': 'example.com'}]}
        with tempfile.TemporaryDirectory() as tmp:
            first = store_original_workflow(Path(tmp), workflow, date='2026-04-27')
            path = Path(first['workflow_path'])
            path.write_text('sentinel', encoding='utf-8')
            second = store_original_workflow(Path(tmp), workflow, date='2026-04-27')
            self.assertEqual(path.read_text(encoding='utf-8'), 'sentinel')
            self.assertNotEqual(first['workflow_path'], second['workflow_path'])
            self.assertIn('-copy-2', second['workflow_path'])

    def test_build_indexes_creates_workflow_and_html_indexes(self):
        records = [
            {
                'workflow_id': 'wf-1',
                'workflow_name': 'Newsletter',
                'domain': 'example.com',
                'workflow_path': 'n8n-sync/originals/example.com/workflows/newsletter-original-2026-04-27.json',
                'html_nodes': [{'node_name': 'HTML Email', 'source': 'html_node', 'path': 'n8n-sync/originals/example.com/html-nodes/html-email-original-2026-04-27.html'}],
            }
        ]
        with tempfile.TemporaryDirectory() as tmp:
            out = build_indexes(Path(tmp), records, date='2026-04-27')
            index = Path(out['workflow_index'])
            html_index = Path(out['html_index'])
            self.assertTrue(index.exists())
            self.assertTrue(html_index.exists())
            self.assertIn('Newsletter', index.read_text(encoding='utf-8'))
            self.assertIn('HTML Email', html_index.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
