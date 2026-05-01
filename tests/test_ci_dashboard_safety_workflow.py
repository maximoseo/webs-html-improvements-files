from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (ROOT / ".github" / "workflows" / "test.yml").read_text(encoding="utf-8")


def test_ci_does_not_mask_test_failures():
    forbidden = ["|| true", "|| exit 0", "continue-on-error: true"]
    for marker in forbidden:
        assert marker not in WORKFLOW, f"CI must not mask failures with {marker!r}"


def test_ci_runs_dashboard_runtime_and_static_safety_checks():
    assert "pytest tests/" in WORKFLOW
    assert "tests/smoke_boot.py" in WORKFLOW
    assert "python -m py_compile server.py" in WORKFLOW
    assert "node" in WORKFLOW and "--check" in WORKFLOW
    assert "INLINE_SCRIPT_CHECK_OK" in WORKFLOW


def test_ci_has_secret_pattern_guard_for_accidental_commits():
    assert "Secret pattern guard" in WORKFLOW
    for pattern in ("ghp_", "github_pat_", "AIza", "sk-"):
        assert pattern in WORKFLOW
