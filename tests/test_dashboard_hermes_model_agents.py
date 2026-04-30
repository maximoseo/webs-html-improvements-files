from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_model_specific_hermes_agents_are_detected_before_generic_hermes():
    content = INDEX.read_text(encoding="utf-8")
    marker = "DASHBOARD_QA_FIX_HERMES_MODEL_AGENT_DETECTION_2026_04_27"
    assert marker in content
    generic = "if(v.includes('hermes')) return 'Hermes Agent';"
    required = [
        "if(v.includes('hermes gpt')||v.includes('gpt 5.5')||v.includes('openai-gpt-5.5')) return 'GPT 5.5';",
        "if(v.includes('hermes opus')||v.includes('opus 4.7')||v.includes('claude-opus-4.7')) return 'Opus 4.7';",
        "if(v.includes('hermes gemini')||v.includes('gemini 3.1')||v.includes('/gemini/')||v==='gemini'||v.startsWith('gemini/')) return 'Gemini 3.1';",
        "if(v.includes('hermes kimi')||v.includes('kimi k2.6')||v.includes('moonshotai-kimi-k2.6')) return 'Kimi K2.6';",
        "if(v.includes('hermes glm')||v.includes('glm 5.1')) return 'GLM 5.1';",
    ]
    generic_pos = content.index(generic)
    for needle in required:
        assert needle in content
        assert content.index(needle) < generic_pos
