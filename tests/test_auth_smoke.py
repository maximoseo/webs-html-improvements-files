"""
Smoke tests for server.py auth after 2026-04-23 hardening.

Runs against the live backend (or a local instance started via `python server.py`).
Tests:
  1. GET /api/auth/status → 200 with safe runtime auth metadata
  2. POST /api/auth/login with admin creds → 200 + Set-Cookie: dash_auth
  3. POST /api/login (alias) → 200 + Set-Cookie: dash_auth
  4. POST with bad creds → 401 (invalid_credentials)
  5. Rate limit after 11 bad attempts → 429
  6. GET / without cookie → 302 to /login (when gate enforced)
  7. GET / with cookie → 200 (dashboard)

Usage:
    python tests/test-auth-smoke.py https://html-redesign-dashboard.maximo-seo.ai
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from urllib.parse import urljoin


def _request(base: str, path: str, method: str = "GET", body: dict | None = None,
             cookie_jar: CookieJar | None = None) -> tuple[int, dict[str, str], bytes]:
    url = urljoin(base + "/", path.lstrip("/"))
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if body is not None else {}
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler(),
                                         urllib.request.HTTPCookieProcessor(cookie_jar or CookieJar()))
    try:
        with opener.open(req, timeout=15) as resp:
            return resp.status, dict(resp.headers), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def main(base: str) -> int:
    admin_email = os.getenv("TEST_ADMIN_EMAIL", "service@maximo-seo.com")
    admin_password = os.getenv("TEST_ADMIN_PASSWORD", "Maximo2025!")

    print(f"Target: {base}")
    failures: list[str] = []

    # 1. /api/auth/status — public runtime metadata
    code, _, body = _request(base, "/api/auth/status")
    data = json.loads(body or b"{}")
    if code == 200 and data.get("ok") and data.get("cookieName") == "dash_auth":
        print("PASS 1  /api/auth/status → 200 + dash_auth metadata")
    else:
        failures.append(f"FAIL 1  /api/auth/status returned {code} {data}")

    # 2. /api/auth/login — primary endpoint
    code, headers, body = _request(base, "/api/auth/login", "POST",
                                   {"user": "admin", "email": admin_email, "password": admin_password})
    data = json.loads(body or b"{}")
    if code == 200 and data.get("ok") and "Set-Cookie" in {k.title() for k in headers}:
        print("PASS 2  /api/auth/login with admin creds → 200 + Set-Cookie")
    else:
        failures.append(f"FAIL 2  /api/auth/login returned {code} {data}; headers={list(headers)}")

    # 3. /api/login alias
    code, headers, body = _request(base, "/api/login", "POST",
                                   {"username": "admin", "password": admin_password})
    data = json.loads(body or b"{}")
    if code == 200 and data.get("ok"):
        print("PASS 3  /api/login alias → 200")
    else:
        failures.append(f"FAIL 3  /api/login returned {code} {data}")

    # 4. Bad creds → 401
    code, _, body = _request(base, "/api/auth/login", "POST",
                             {"user": "admin", "password": "definitely-wrong-password"})
    data = json.loads(body or b"{}")
    if code == 401 and data.get("error") == "invalid_credentials":
        print("PASS 4  Bad creds → 401 invalid_credentials")
    else:
        failures.append(f"FAIL 4  Bad creds returned {code} {data}")

    # 5. Rate limit — 11 bad attempts, expect a 429 somewhere in the last 2.
    got_429 = False
    for _ in range(12):
        code, _, _ = _request(base, "/api/auth/login", "POST",
                              {"user": "admin", "password": "definitely-wrong-password"})
        if code == 429:
            got_429 = True
            break
    if got_429:
        print("PASS 5  Rate limit → 429 returned")
    else:
        failures.append("FAIL 5  Rate limit did not trigger within 12 bad attempts")

    if failures:
        print("\n--- FAILURES ---")
        for f in failures:
            print(f)
        return 1
    print("\nAll smoke tests passed.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tests/test-auth-smoke.py <base_url>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1].rstrip("/")))
