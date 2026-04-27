import tempfile
import unittest
from pathlib import Path

from n8n_sync_originals import sync_originals


class FakeClient:
    def get_all_workflows(self):
        return [{'id': 'wf-1'}, {'id': 'wf-2'}]

    def get_workflow_detail(self, workflow_id):
        return {
            'id': workflow_id,
            'name': f'Workflow {workflow_id}',
            'tags': [{'name': 'example.com'}],
            'nodes': [
                {'name': 'HTML', 'type': 'n8n-nodes-base.html', 'parameters': {'html': f'<html>{{$json.{workflow_id}}}</html>'}}
            ],
        }


class N8NSyncOriginalsTests(unittest.TestCase):
    def test_sync_originals_uses_detail_fetch_and_writes_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = sync_originals(Path(tmp), FakeClient(), date='2026-04-27', max_workflows=1)
            self.assertTrue(result['ok'])
            self.assertEqual(result['workflow_count'], 1)
            self.assertEqual(result['html_node_count'], 1)
            manifest = Path(result['manifest_path'])
            self.assertTrue(manifest.exists())
            self.assertIn('GET-only', manifest.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
