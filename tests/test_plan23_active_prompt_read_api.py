import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVER_TEXT = (ROOT / "server.py").read_text(encoding="utf-8")


def load_server():
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    spec = importlib.util.spec_from_file_location("dashboard_server_plan23", ROOT / "server.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_plan23_active_prompt_endpoint_is_read_only_get_contract():
    assert "PLAN23_ACTIVE_PROMPT_READ_API_2026_05_07" in SERVER_TEXT
    assert "if parsed.path == '/api/prompts/active':" in SERVER_TEXT
    do_get = SERVER_TEXT[SERVER_TEXT.find("    def do_GET(self):"):SERVER_TEXT.find("    def do_POST(self):")]
    do_post = SERVER_TEXT[SERVER_TEXT.find("    def do_POST(self):"):]
    assert "/api/prompts/active" in do_get
    assert "/api/prompts/active" not in do_post
    assert "readOnlyN8n" in SERVER_TEXT
    assert "mutatesWorkflow" in SERVER_TEXT


def test_active_prompt_domain_normalization_and_invalid_rejection():
    server = load_server()
    assert server._normalize_active_prompt_domain("https://WWW.Example.com/some/path?x=1") == "www.example.com"
    assert server._normalize_active_prompt_domain("client-site.co.il") == "client-site.co.il"
    for bad in ["", "localhost", "127.0.0.1", "../secret", "https://127.0.0.1/admin"]:
        try:
            server._normalize_active_prompt_domain(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"invalid domain accepted: {bad!r}")


def test_active_prompt_missing_domain_returns_safe_404_without_prompt():
    server = load_server()
    status, payload = server.active_prompt_read_response("missing-plan23-example.test")
    assert status == 404
    assert payload["ok"] is False
    assert payload["error"] == "no_active_prompt"
    assert payload["domain"] == "missing-plan23-example.test"
    assert payload["readOnlyN8n"] is True
    assert payload["n8nIntegration"]["mutatesWorkflow"] is False
    assert payload["nextAction"] == "create_or_commit_prompt_via_prompt_studio"
    assert "prompt" not in payload


def test_active_prompt_reads_latest_prompt_file_under_domain(tmp_path, monkeypatch):
    server = load_server()
    monkeypatch.setattr(server, "ROOT", tmp_path)
    prompt_dir = tmp_path / "example.com" / "gpt" / "v1"
    prompt_dir.mkdir(parents=True)
    prompt_file = prompt_dir / "Improved_N8N_Prompt.txt"
    prompt_file.write_text("Use the verified site profile only. No secrets.", encoding="utf-8")

    status, payload = server.active_prompt_read_response("example.com")
    assert status == 200
    assert payload["ok"] is True
    assert payload["domain"] == "example.com"
    assert payload["prompt"] == "Use the verified site profile only. No secrets."
    assert payload["sourcePath"] == "example.com/gpt/v1/Improved_N8N_Prompt.txt"
    assert payload["readOnlyN8n"] is True
    assert payload["n8nIntegration"]["method"] == "GET"
    assert payload["n8nIntegration"]["mutatesWorkflow"] is False
