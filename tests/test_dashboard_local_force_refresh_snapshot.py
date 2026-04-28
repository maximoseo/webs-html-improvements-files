from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_local_force_refresh_keeps_bundled_snapshot_authoritative():
    content = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_QA_FIX_FORCE_REFRESH_LOCAL_SNAPSHOT_2026_04_27" in content
    assert "location.hostname!=='127.0.0.1'" in content
    assert "location.hostname!=='localhost'" in content
    assert "newly generated local artifacts before commit/push" in content
