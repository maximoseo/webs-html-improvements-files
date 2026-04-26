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

    def test_prompt_studio_action_buttons_are_type_button_and_have_handlers(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertRegex(html, r'<button id="prompt-improve-btn"[^>]*\btype="button"[^>]*onclick="improvePrompt\(this\)"')
        self.assertRegex(html, r'<button id="prompt-tweak-btn"[^>]*\btype="button"[^>]*onclick="tweakTemplate\(this\)"')
        self.assertRegex(html, r'<button id="prompt-brainstorm-btn"[^>]*\btype="button"[^>]*onclick="brainstormPrompt\(this\)"')

    def test_prompt_studio_launch_pipeline_is_self_healing_and_visible(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn('PROMPT_STUDIO_ACTIONS_HARDENING_2026_04_26', html)
        self.assertIn('function ensurePromptStudioActionBindings()', html)
        self.assertIn("bind('prompt-tweak-btn', window.tweakTemplate);", html)
        self.assertIn('ensurePromptStudioActionBindings();', html)
        self.assertIn('el.onclick=function(ev){', html)
        hardening_script = html.split('<script id="prompt-studio-actions-hardening-2026-04-26">', 1)[1].split('</script>', 1)[0]
        self.assertNotIn('ev.stopPropagation();', hardening_script)
        self.assertRegex(html, r'#prompt-modal #prompt-tweak-btn\.ps-pipeline-launcher\s*\{[^}]*pointer-events:\s*auto\s*!important')
        self.assertRegex(html, r'#prompt-modal #prompt-tweak-btn\.ps-pipeline-launcher\s*\{[^}]*cursor:\s*pointer\s*!important')

    def test_prompt_studio_tweak_accepts_draft_fallback_and_reports_api_errors(self):
        html = INDEX_HTML.read_text(encoding='utf-8')
        self.assertIn("const draftFallback=(document.getElementById('prompt-draft').value||'').trim();", html)
        self.assertIn("const improved=improvedOutput||draftFallback;", html)
        self.assertIn("const errorDetail=data&&data.details?(' - '+data.details):'';", html)


if __name__ == '__main__':
    unittest.main()
