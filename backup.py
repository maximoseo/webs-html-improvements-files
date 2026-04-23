"""
Stage 14 — Backup & Restore for the dashboard.

Creates a timestamped tar.gz of the local `data/` directory + key JSON files,
then mirrors it to:
  1. GitHub Releases (repo: maximoseo/webs-html-improvements-files, release tag "backups")
  2. Supabase Storage  (bucket: dashboard-backups)
  3. (Obsidian mirroring is handled out-of-band by a Hermes cronjob)

Also supports listing and restoring backups.

Env vars required:
  GITHUB_TOKEN           — PAT with repo scope
  SUPABASE_URL           — e.g. https://xxx.supabase.co
  SUPABASE_SERVICE_ROLE_KEY — server-only key

All operations are best-effort: a failure in one channel does not block the others.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tarfile
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
BACKUP_DIR = ROOT / "data" / "_backups"   # local cache (last 7 only)
KEEP_LOCAL = 7
KEEP_REMOTE = 30

GITHUB_REPO = "maximoseo/webs-html-improvements-files"
GITHUB_RELEASE_TAG = "backups"
SUPABASE_BUCKET = "dashboard-backups"


# ---------- helpers ----------

def _log(msg: str) -> None:
    print(f"[backup {datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def _http(url, method="GET", headers=None, data=None, timeout=120):
    req = urllib.request.Request(url, method=method, headers=headers or {}, data=data)
    return urllib.request.urlopen(req, timeout=timeout)


# ---------- snapshot creation ----------

def _iter_backup_files():
    """Yield (relative_path_str, absolute_Path) for everything we want to back up."""
    if DATA_DIR.exists():
        for p in DATA_DIR.rglob("*"):
            # Skip the backups dir itself to avoid recursion
            if BACKUP_DIR in p.parents or p == BACKUP_DIR:
                continue
            if p.is_file():
                yield str(p.relative_to(ROOT)), p
    # Top-level JSON files (data.json, etc.)
    for p in ROOT.glob("*.json"):
        if p.is_file():
            yield p.name, p


def create_snapshot() -> dict:
    """Create local tar.gz snapshot. Returns metadata dict."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"dash-backup-{ts}.tar.gz"
    out_path = BACKUP_DIR / name

    file_count = 0
    with tarfile.open(out_path, "w:gz", compresslevel=6) as tar:
        for rel, abs_path in _iter_backup_files():
            try:
                tar.add(abs_path, arcname=rel)
                file_count += 1
            except Exception as e:
                _log(f"skip {rel}: {e}")

    size = out_path.stat().st_size
    sha256 = hashlib.sha256(out_path.read_bytes()).hexdigest()
    meta = {
        "name": name,
        "path": str(out_path),
        "size": size,
        "sha256": sha256,
        "files": file_count,
        "created_at": ts,
    }
    _log(f"snapshot {name} ({size//1024} KB, {file_count} files, sha {sha256[:12]})")
    _prune_local()
    return meta


def _prune_local() -> None:
    files = sorted(BACKUP_DIR.glob("dash-backup-*.tar.gz"))
    for old in files[:-KEEP_LOCAL]:
        try:
            old.unlink()
            _log(f"pruned local {old.name}")
        except Exception as e:
            _log(f"prune fail {old.name}: {e}")


# ---------- GitHub Releases ----------

def _gh_headers():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "dashboard-backup",
    }


def _gh_get_or_create_release() -> dict | None:
    h = _gh_headers()
    if not h:
        _log("github: GITHUB_TOKEN not set, skipping")
        return None
    # Try to fetch existing release
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/tags/{GITHUB_RELEASE_TAG}"
    try:
        r = _http(url, headers=h)
        return json.loads(r.read())
    except urllib.error.HTTPError as e:
        if e.code != 404:
            _log(f"github: get release failed {e.code}")
            return None
    # Create
    create_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"
    body = json.dumps({
        "tag_name": GITHUB_RELEASE_TAG,
        "name": "Automated Backups",
        "body": "Rolling snapshots of dashboard data. Managed by backup.py.",
        "prerelease": True,
    }).encode()
    try:
        r = _http(create_url, method="POST", headers={**h, "Content-Type": "application/json"}, data=body)
        return json.loads(r.read())
    except Exception as e:
        _log(f"github: create release failed: {e}")
        return None


def upload_to_github(meta: dict) -> bool:
    rel = _gh_get_or_create_release()
    if not rel:
        return False
    upload_url = rel["upload_url"].split("{")[0]
    name = meta["name"]
    upload_url += f"?name={urllib.parse.quote(name)}"
    h = _gh_headers()
    if not h:
        return False
    h2 = {**h, "Content-Type": "application/gzip"}
    data = Path(meta["path"]).read_bytes()
    try:
        r = _http(upload_url, method="POST", headers=h2, data=data)
        if r.status in (200, 201):
            _log(f"github: uploaded {name}")
            _gh_prune(rel)
            return True
        _log(f"github: upload status {r.status}")
        return False
    except urllib.error.HTTPError as e:
        # 422 = already exists; treat as ok
        if e.code == 422:
            _log(f"github: {name} already exists, ok")
            return True
        _log(f"github: upload failed {e.code} {e.read()[:200]!r}")
        return False
    except Exception as e:
        _log(f"github: upload error {e}")
        return False


def _gh_prune(release: dict) -> None:
    h = _gh_headers()
    if not h:
        return
    assets = release.get("assets", [])
    # Re-fetch fresh assets list
    try:
        r = _http(f"https://api.github.com/repos/{GITHUB_REPO}/releases/{release['id']}/assets?per_page=100", headers=h)
        assets = json.loads(r.read())
    except Exception:
        pass
    backups = sorted(
        [a for a in assets if a["name"].startswith("dash-backup-")],
        key=lambda a: a["name"],
    )
    for old in backups[:-KEEP_REMOTE]:
        try:
            _http(f"https://api.github.com/repos/{GITHUB_REPO}/releases/assets/{old['id']}",
                  method="DELETE", headers=h)
            _log(f"github: pruned {old['name']}")
        except Exception as e:
            _log(f"github: prune fail {old['name']}: {e}")


def list_github() -> list[dict]:
    h = _gh_headers()
    if not h:
        return []
    try:
        r = _http(f"https://api.github.com/repos/{GITHUB_REPO}/releases/tags/{GITHUB_RELEASE_TAG}", headers=h)
        rel = json.loads(r.read())
        return [
            {"name": a["name"], "size": a["size"], "url": a["browser_download_url"],
             "created_at": a["created_at"], "source": "github"}
            for a in rel.get("assets", [])
            if a["name"].startswith("dash-backup-")
        ]
    except Exception as e:
        _log(f"github: list failed {e}")
        return []


# ---------- Supabase Storage ----------

def _supa_headers():
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        return None
    return {
        "Authorization": f"Bearer {key}",
        "apikey": key,
    }


def _supa_url(path: str) -> str | None:
    base = os.environ.get("SUPABASE_URL")
    if not base:
        return None
    return f"{base.rstrip('/')}/storage/v1/{path.lstrip('/')}"


def _supa_ensure_bucket() -> bool:
    h = _supa_headers()
    url = _supa_url(f"bucket/{SUPABASE_BUCKET}")
    if not h or not url:
        return False
    try:
        _http(url, headers=h)
        return True
    except urllib.error.HTTPError as e:
        if e.code != 404:
            _log(f"supabase: bucket check failed {e.code}")
            return False
    # Create
    try:
        body = json.dumps({"id": SUPABASE_BUCKET, "name": SUPABASE_BUCKET, "public": False}).encode()
        _http(_supa_url("bucket"), method="POST",
              headers={**h, "Content-Type": "application/json"}, data=body)
        _log(f"supabase: created bucket {SUPABASE_BUCKET}")
        return True
    except Exception as e:
        _log(f"supabase: bucket create failed {e}")
        return False


def upload_to_supabase(meta: dict) -> bool:
    h = _supa_headers()
    if not h:
        _log("supabase: SUPABASE_URL/SERVICE_ROLE_KEY not set, skipping")
        return False
    if not _supa_ensure_bucket():
        return False
    name = meta["name"]
    url = _supa_url(f"object/{SUPABASE_BUCKET}/{name}")
    data = Path(meta["path"]).read_bytes()
    headers = {**h, "Content-Type": "application/gzip", "x-upsert": "true"}
    try:
        r = _http(url, method="POST", headers=headers, data=data)
        if r.status in (200, 201):
            _log(f"supabase: uploaded {name}")
            _supa_prune()
            return True
        _log(f"supabase: upload status {r.status}")
        return False
    except Exception as e:
        _log(f"supabase: upload failed {e}")
        return False


def _supa_prune() -> None:
    h = _supa_headers()
    if not h:
        return
    url = _supa_url(f"object/list/{SUPABASE_BUCKET}")
    try:
        body = json.dumps({"limit": 1000, "offset": 0,
                           "sortBy": {"column": "name", "order": "desc"}}).encode()
        r = _http(url, method="POST",
                  headers={**h, "Content-Type": "application/json"}, data=body)
        items = json.loads(r.read())
    except Exception as e:
        _log(f"supabase: list failed {e}")
        return
    backups = sorted([i for i in items if i.get("name", "").startswith("dash-backup-")],
                     key=lambda i: i["name"])
    for old in backups[:-KEEP_REMOTE]:
        try:
            _http(_supa_url(f"object/{SUPABASE_BUCKET}/{old['name']}"),
                  method="DELETE", headers=h)
            _log(f"supabase: pruned {old['name']}")
        except Exception as e:
            _log(f"supabase: prune fail {old['name']}: {e}")


def list_supabase() -> list[dict]:
    h = _supa_headers()
    base = os.environ.get("SUPABASE_URL")
    if not h or not base:
        return []
    url = _supa_url(f"object/list/{SUPABASE_BUCKET}")
    try:
        body = json.dumps({"limit": 200, "offset": 0,
                           "sortBy": {"column": "name", "order": "desc"}}).encode()
        r = _http(url, method="POST",
                  headers={**h, "Content-Type": "application/json"}, data=body)
        items = json.loads(r.read())
        return [
            {"name": i["name"], "size": (i.get("metadata") or {}).get("size", 0),
             "url": f"{base.rstrip('/')}/storage/v1/object/{SUPABASE_BUCKET}/{i['name']}",
             "created_at": i.get("created_at", ""), "source": "supabase"}
            for i in items if i.get("name", "").startswith("dash-backup-")
        ]
    except Exception as e:
        _log(f"supabase: list failed {e}")
        return []


# ---------- public API ----------

def run_backup() -> dict:
    """Create snapshot and push to all destinations. Returns combined report."""
    meta = create_snapshot()
    gh_ok = upload_to_github(meta)
    sb_ok = upload_to_supabase(meta)
    return {
        "ok": True,
        "name": meta["name"],
        "size": meta["size"],
        "sha256": meta["sha256"],
        "files": meta["files"],
        "destinations": {"local": True, "github": gh_ok, "supabase": sb_ok},
    }


def list_local() -> list[dict]:
    if not BACKUP_DIR.exists():
        return []
    return [
        {"name": p.name, "size": p.stat().st_size,
         "url": f"/api/admin/backup/local/{p.name}",
         "created_at": datetime.fromtimestamp(p.stat().st_mtime, timezone.utc).isoformat(),
         "source": "local"}
        for p in sorted(BACKUP_DIR.glob("dash-backup-*.tar.gz"), reverse=True)
    ]


def list_all() -> dict:
    return {
        "local": list_local(),
        "github": list_github(),
        "supabase": list_supabase(),
    }


def restore_from_local(name: str) -> dict:
    """Extract a local backup over the project root. Use with care."""
    p = BACKUP_DIR / name
    if not p.exists() or not p.name.startswith("dash-backup-"):
        return {"ok": False, "error": "not_found"}
    # Safety: write to a staging area first
    staging = ROOT / "data" / "_restore_staging"
    if staging.exists():
        import shutil
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    with tarfile.open(p, "r:gz") as tar:
        tar.extractall(staging)
    return {"ok": True, "staged_at": str(staging),
            "note": "Inspect staging dir, then move files manually."}


# ---------- CLI ----------

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    if cmd == "run":
        print(json.dumps(run_backup(), indent=2))
    elif cmd == "list":
        print(json.dumps(list_all(), indent=2))
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("usage: backup.py restore <name>")
            sys.exit(2)
        print(json.dumps(restore_from_local(sys.argv[2]), indent=2))
    else:
        print("commands: run | list | restore <name>")
        sys.exit(2)
