import importlib.util
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_server():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("dashboard_server", ROOT / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_improvement_rules_include_16_backend_categories():
    server = load_server()
    assert len(server.IMPROVEMENT_RULES) == 16
    keys = {rule["rule_key"] for rule in server.IMPROVEMENT_RULES}
    assert "rule_wordpress_html" in keys
    assert "rule_api_secrets" in keys
    assert "rule_validation" in keys


def test_assemble_improve_workflow_prompt_uses_inputs_rules_and_no_secrets():
    server = load_server()
    payload = {
        "mainWebsiteUrl": "https://example.com/",
        "originalArticleUrl": "https://example.com/blog/article",
        "originalPrompt": "כתוב מאמר בעברית על מוצרים אמיתיים",
        "htmlTemplate": '<article lang="he" dir="rtl"><p>שלום</p></article>',
        "workflowJson": '{"nodes":[{"name":"WooCommerce Products"}],"connections":{}}',
        "externalProductUrl": "https://store.example.com/",
        "customInstructions": "Keep author bio last",
        "model": "google/gemini-2.5-flash",
    }
    result = server.assemble_improve_workflow_prompt(payload)
    prompt = result["assembledPrompt"]
    assert result["ok"] is True
    assert result["discoveredData"]["site_language"] == "he"
    assert result["discoveredData"]["site_direction"] == "rtl"
    assert result["discoveredData"]["store_decision"] == "store"
    assert "Improved_N8N_Prompt.txt" in prompt
    assert "Improved_HTML_Template.html" in prompt
    assert "Improved_N8N_Workflow.json" in prompt
    assert "Rule 5: WordPress HTML Output" in prompt
    assert "Rule 16: API & Secret Handling" in prompt
    assert "Never print, echo, expose, or include API keys" in prompt
    assert "https://example.com/blog/article" in prompt


def test_index_exposes_improve_workflow_ui_and_endpoint():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert 'data-template="improve-workflow"' in html
    assert 'id="ps-improve-workflow-form"' in html
    assert '/api/studio/improve' in html
    assert 'PLAN21_IMPROVE_WORKFLOW_PROMPT_STUDIO_2026_04_28' in html


def test_server_routes_expose_rules_and_assembly_endpoint():
    server_py = (ROOT / "server.py").read_text(encoding="utf-8")
    assert "/api/studio/improve/rules" in server_py
    assert "/api/studio/improve" in server_py
    assert "assemble_improve_workflow_prompt(payload)" in server_py
