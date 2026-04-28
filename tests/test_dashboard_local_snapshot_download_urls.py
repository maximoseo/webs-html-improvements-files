from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def test_local_snapshot_uses_local_download_urls_for_unpushed_artifacts():
    content = INDEX.read_text(encoding="utf-8")
    assert "DASHBOARD_QA_FIX_LOCAL_SNAPSHOT_DOWNLOAD_URLS_2026_04_27" in content
    assert "const LOCAL_SNAPSHOT_DOWNLOADS=" in content
    assert "source==='static'" in content
    assert "location.hostname==='127.0.0.1'||location.hostname==='localhost'" in content
    assert "download: LOCAL_SNAPSHOT_DOWNLOADS?`/${encodedPath}`:`${RAW_BASE}/${encodedPath}`" in content
