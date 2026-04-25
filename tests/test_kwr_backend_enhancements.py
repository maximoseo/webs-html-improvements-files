import os
import shutil
import unittest
from unittest import mock

import kwr_backend


class KwResearchEnhancementTests(unittest.TestCase):
    def test_prepare_kwr_rows_removes_semantic_duplicates_and_scores_quality(self):
        raw_rows = [
            {
                'existing_parent_page': '/garage-door-repair/',
                'pillar': 'Garage Door Repair',
                'cluster': 'Emergency Garage Door Repair',
                'intent': 'transactional',
                'primary_keyword': 'garage door repair san antonio',
                'keywords': 'Acme, garage door repair san antonio, emergency garage repair san antonio',
            },
            {
                'existing_parent_page': '/garage-door-repair/',
                'pillar': 'Garage Door Repair',
                'cluster': 'San Antonio Garage Door Repair',
                'intent': 'transactional',
                'primary_keyword': 'san antonio garage door repair',
                'keywords': 'Acme, san antonio garage door repair, same day garage repair san antonio',
            },
            {
                'existing_parent_page': '-',
                'pillar': 'Garage Door Installation',
                'cluster': 'Garage Door Installation',
                'intent': 'pillar',
                'primary_keyword': 'garage door installation',
                'keywords': 'Acme, garage door installation, new garage doors',
            },
        ]

        clean_rows, stats = kwr_backend.prepare_kwr_rows(raw_rows, existing_pages=['/garage-door-repair/'], brand='Acme', source_model='openai/gpt-5.4')

        self.assertEqual(len(clean_rows), 2)
        self.assertGreaterEqual(stats['semantic_duplicates_removed'], 1)
        self.assertIn('quality_summary', stats)
        self.assertEqual(stats['quality_summary']['total'], 2)
        for row in clean_rows:
            self.assertIn('quality_score', row)
            self.assertIn('quality_tier', row)
            self.assertIn('quality_reasons', row)
            self.assertEqual(row['source_model'], 'openai/gpt-5.4')

    def test_build_model_participation_summarizes_kept_rows(self):
        child_jobs = [
            {
                'inputs': {'model': 'openai/gpt-5.4'},
                'rows': [{}, {}, {}],
            },
            {
                'inputs': {'model': 'anthropic/claude-opus-4.7'},
                'rows': [{}, {}],
            },
        ]
        merged_rows = [
            {'primary_keyword': 'kw1', 'source_model': 'openai/gpt-5.4'},
            {'primary_keyword': 'kw2', 'source_model': 'openai/gpt-5.4'},
            {'primary_keyword': 'kw3', 'source_model': 'anthropic/claude-opus-4.7'},
        ]

        summary = kwr_backend.build_model_participation(child_jobs, merged_rows)

        self.assertEqual(summary[0]['model'], 'openai/gpt-5.4')
        self.assertEqual(summary[0]['kept_rows'], 2)
        self.assertEqual(summary[0]['total_rows'], 3)
        self.assertEqual(summary[1]['model'], 'anthropic/claude-opus-4.7')
        self.assertEqual(summary[1]['kept_rows'], 1)
        self.assertEqual(summary[1]['total_rows'], 2)

    def test_build_excel_prefers_cached_file_for_live_job_downloads(self):
        run_id = 'test-cached-download'
        run_dir = kwr_backend._run_dir(run_id)
        shutil.rmtree(run_dir, ignore_errors=True)
        os.makedirs(run_dir, exist_ok=True)
        cached = b'cached-xlsx-bytes'
        with open(os.path.join(run_dir, 'file.xlsx'), 'wb') as f:
            f.write(cached)

        with kwr_backend._lock:
            kwr_backend._state[run_id] = {
                'inputs': {'brand_name': 'Cache Brand'},
                'rows': [{'existing_parent_page': '-', 'pillar': 'A', 'cluster': 'A', 'intent': 'pillar'}],
                'status': 'ready',
            }

        try:
            with mock.patch('openpyxl.Workbook', side_effect=AssertionError('should not rebuild cached workbook')):
                data, ws_name, err = kwr_backend.build_excel(run_id)
        finally:
            with kwr_backend._lock:
                kwr_backend._state.pop(run_id, None)
            shutil.rmtree(run_dir, ignore_errors=True)

        self.assertIsNone(err)
        self.assertEqual(data, cached)
        self.assertIn('cache-brand', ws_name)


if __name__ == '__main__':
    unittest.main()
