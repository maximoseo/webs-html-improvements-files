from pathlib import Path
import unittest

import server

REPO_ROOT = Path(server.__file__).resolve().parent
INDEX_HTML = REPO_ROOT / 'index.html'


class PromptStudioDevicePreviewTests(unittest.TestCase):
    def test_prompt_studio_has_device_tabs_for_live_preview(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('id="prompt-preview-device-tabs"', html)
        self.assertIn("setPromptPreviewDevice('mobile'", html)
        self.assertIn("setPromptPreviewDevice('tablet'", html)
        self.assertIn("setPromptPreviewDevice('desktop'", html)
        self.assertIn('prompt-preview-device-label', html)
        self.assertIn('prompt-preview-device-frame', html)

    def test_prompt_studio_has_js_to_switch_preview_device_modes(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('function setPromptPreviewDevice(mode,btn){', html)
        self.assertIn("previewDeviceMode:'desktop'", html)
        self.assertIn('prompt-preview-frame-wrap', html)
        self.assertIn('prompt-preview-device-label', html)


if __name__ == '__main__':
    unittest.main()
