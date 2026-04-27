from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
MIGRATION = ROOT / 'supabase' / 'migrations' / '20260427_n8n_sync_schema.sql'


class N8NSupabaseMigrationTests(unittest.TestCase):
    def test_migration_file_exists(self):
        self.assertTrue(MIGRATION.exists(), 'Expected n8n Supabase migration SQL file')

    def test_required_tables_are_created(self):
        sql = MIGRATION.read_text(encoding='utf-8').lower()
        for table in [
            'n8n_workflows',
            'n8n_html_templates',
            'n8n_improved_templates',
            'n8n_improvement_prompts',
            'n8n_sync_log',
        ]:
            self.assertRegex(sql, rf'create\s+table\s+if\s+not\s+exists\s+{table}\b')

    def test_required_constraints_and_indexes_exist(self):
        sql = MIGRATION.read_text(encoding='utf-8').lower()
        self.assertIn('unique(n8n_workflow_id)', sql)
        for index in [
            'idx_n8n_workflows_domain',
            'idx_n8n_html_domain',
            'idx_improved_domain',
            'idx_improved_agent',
        ]:
            self.assertIn(index, sql)

    def test_schema_is_storage_only_not_n8n_api_execution(self):
        sql = MIGRATION.read_text(encoding='utf-8').lower()
        forbidden = ['http_post', 'http_put', 'http_delete', '/api/v1/workflows', 'activate', 'deactivate']
        for token in forbidden:
            self.assertNotIn(token, sql)

    def test_manual_import_safety_note_is_documented(self):
        sql = MIGRATION.read_text(encoding='utf-8')
        self.assertIn('MANUAL IMPORT ONLY', sql)
        self.assertIn('read-only reference', sql.lower())


if __name__ == '__main__':
    unittest.main()
