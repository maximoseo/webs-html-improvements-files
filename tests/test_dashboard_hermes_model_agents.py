from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_model_specific_hermes_agents_are_detected_before_generic_hermes():
    content = INDEX.read_text(encoding="utf-8")
    marker = "DASHBOARD_QA_FIX_HERMES_MODEL_AGENT_DETECTION_2026_04_27"
    assert marker in content
    generic = "if(v.includes('hermes')) return 'Hermes Agent';"
    required = [
        "if(v.includes('hermes gpt')) return 'Hermes GPT 5.5';",
        "if(v.includes('hermes opus')) return 'Hermes Opus 4.7';",
        "if(v.includes('hermes gemini')) return 'Hermes Gemini 3.1';",
        "if(v.includes('hermes kimi')) return 'Hermes Kimi K2.6';",
        "if(v.includes('hermes glm')) return 'Hermes GLM 5.1';",
    ]
    generic_pos = content.index(generic)
    for needle in required:
        assert needle in content
        assert content.index(needle) < generic_pos
