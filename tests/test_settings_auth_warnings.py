from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class SettingsAuthWarningsTests(unittest.TestCase):
    def test_settings_auth_warning_analysis_includes_backend_drift_warnings(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn("warnings = warnings.concat(data.driftWarnings || []);", html)


if __name__ == '__main__':
    unittest.main()
