#!/usr/bin/env python3
"""Auth diagnostics for the HTML Redesign Dashboard.

Examples:
  python scripts/auth_doctor.py https://html-redesign-dashboard.maximo-seo.ai \
    --user admin --email service@maximo-seo.com --password "$TEST_ADMIN_PASSWORD"

  python scripts/auth_doctor.py http://127.0.0.1:8010 --user admin --password "$TEST_ADMIN_PASSWORD"
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from urllib.parse import urljoin

DEFAULT_EMAIL = "service@maximo-seo.com"


def _json_bytes(payload: dict | None) -> bytes | None:
    return json.dumps(payload).encode("utf-8") if payload is not None else None


def _request(base: str, path: str, *, method: str = "GET", body: dict | None = None,
             headers: dict[str, str] | None = None, cookie_jar: CookieJar | None = None) -> tuple[int, dict[str, str], bytes]:
    url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
    merged_headers = dict(headers or {})
    if body is not None:
        merged_headers.setdefault("Content-Type", "application/json")
    request = urllib.request.Request(url, data=_json_bytes(body), method=method, headers=merged_headers)
    opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler(),
        urllib.request.HTTPCookieProcessor(cookie_jar or CookieJar()),
    )
    try:
        with opener.open(request, timeout=20) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers), exc.read()


def _decode_json(raw: bytes) -> dict | list | str | None:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return raw.decode("utf-8", "replace")[:1000]


def _sanitize(value):
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            if key.lower() in {"token", "jwt", "access_token", "refresh_token", "set_cookie"}:
                redacted[key] = "[redacted]"
            else:
                redacted[key] = _sanitize(item)
        return redacted
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, str) and len(value) > 400:
        return value[:400] + "…"
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Run auth diagnostics against a dashboard instance.")
    parser.add_argument("base_url", help="Base URL, e.g. https://html-redesign-dashboard.maximo-seo.ai")
    parser.add_argument("--user", default=os.getenv("TEST_ADMIN_USER", "admin"))
    parser.add_argument("--email", default=os.getenv("TEST_ADMIN_EMAIL", DEFAULT_EMAIL))
    parser.add_argument("--password", default=os.getenv("TEST_ADMIN_PASSWORD", ""))
    parser.add_argument("--bad-attempts", type=int, default=12)
    parser.add_argument("--forwarded-ip", default="203.0.113.77")
    parser.add_argument("--spoof-forwarded-ip", action="store_true", help="Opt-in: send spoofed proxy/Cloudflare IP headers for controlled proxy tests only")
    parser.add_argument("--include-rate-limit", action="store_true", help="Opt-in: run bad-login rate-limit probe; disabled by default for production safety")
    args = parser.parse_args()

    summary: dict[str, object] = {
        "base_url": args.base_url.rstrip("/"),
        "checks": {},
        "warnings": [],
    }

    public_checks = [
        ("login_page", "/login"),
        ("auth_status", "/api/auth/status"),
        ("health", "/api/health"),
    ]
    for label, path in public_checks:
        code, headers, body = _request(args.base_url, path)
        summary["checks"][label] = {
            "status": code,
            "ok": 200 <= code < 300,
            "body": _sanitize(_decode_json(body)),
            "request_id": headers.get("X-Request-ID") or headers.get("x-request-id"),
        }

    if not args.password:
        summary["warnings"].append("No password provided; skipping credentialed login and rate-limit checks.")
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    cookie_jar = CookieJar()
    primary_headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 auth-doctor",
        "Origin": args.base_url.rstrip("/"),
        "Referer": args.base_url.rstrip("/") + "/login",
    }
    if args.spoof_forwarded_ip:
        primary_headers.update({
            "CF-Connecting-IP": args.forwarded_ip,
            "X-Forwarded-For": f"{args.forwarded_ip}, 10.0.0.1",
            "X-Real-IP": args.forwarded_ip,
        })
    code, headers, body = _request(
        args.base_url,
        "/api/auth/login",
        method="POST",
        body={"user": args.user, "password": args.password},
        headers=primary_headers,
        cookie_jar=cookie_jar,
    )
    login_data = _decode_json(body)
    summary["checks"]["login_primary"] = {
        "status": code,
        "ok": 200 <= code < 300,
        "body": _sanitize(login_data),
        "set_cookie": "Set-Cookie" in headers or "set-cookie" in {k.lower() for k in headers},
    }

    me_headers = None
    if isinstance(login_data, dict) and login_data.get("jwt"):
        me_headers = {"Authorization": f"Bearer {login_data['jwt']}"}
    code, _, body = _request(args.base_url, "/api/auth/me", headers=me_headers, cookie_jar=cookie_jar)
    me_body = _decode_json(body)
    summary["checks"]["auth_me_after_primary_login"] = {
        "status": code,
        "ok": 200 <= code < 300,
        "body": _sanitize(me_body),
        "transport": "bearer" if me_headers else "cookie",
    }
    if isinstance(me_body, dict) and not me_body.get("user") and str(args.base_url).startswith("http://"):
        summary["warnings"].append("HTTP local checks may not round-trip the Secure dash_auth cookie; bearer fallback is used when available.")

    code, headers, body = _request(
        args.base_url,
        "/api/login",
        method="POST",
        body={"username": args.user, "password": args.password},
        headers=primary_headers,
    )
    summary["checks"]["login_alias"] = {
        "status": code,
        "ok": 200 <= code < 300,
        "body": _sanitize(_decode_json(body)),
        "set_cookie": "Set-Cookie" in headers or "set-cookie" in {k.lower() for k in headers},
    }

    if args.email:
        email_cookie_jar = CookieJar()
        code, _, body = _request(
            args.base_url,
            "/api/auth/login",
            method="POST",
            body={"email": args.email, "password": args.password},
            headers=primary_headers,
            cookie_jar=email_cookie_jar,
        )
        summary["checks"]["login_email_alias"] = {
            "status": code,
            "ok": 200 <= code < 300,
            "body": _sanitize(_decode_json(body)),
        }

    rate_codes: list[int] = []
    retry_after = None
    forwarded_headers = dict(primary_headers)
    if args.include_rate_limit:
        for _ in range(max(1, args.bad_attempts)):
            code, headers, body = _request(
                args.base_url,
                "/api/auth/login",
                method="POST",
                body={"user": args.user, "password": "definitely-wrong-password"},
                headers=forwarded_headers,
            )
            rate_codes.append(code)
            if code == 429:
                retry_after = headers.get("Retry-After")
                summary["checks"]["rate_limit"] = {
                    "status": code,
                    "ok": True,
                    "retry_after": retry_after,
                    "body": _sanitize(_decode_json(body)),
                    "attempts": len(rate_codes),
                    "codes": rate_codes,
                }
                break
        else:
            summary["checks"]["rate_limit"] = {
                "status": rate_codes[-1] if rate_codes else None,
                "ok": False,
                "retry_after": retry_after,
                "attempts": len(rate_codes),
                "codes": rate_codes,
            }
            summary["warnings"].append("Rate limit did not trigger within the configured bad attempts window.")
    else:
        summary["checks"]["rate_limit"] = {
            "status": None,
            "ok": None,
            "skipped": True,
            "reason": "rate-limit probe disabled by default; pass --include-rate-limit to run it",
            "attempts": 0,
            "codes": [],
        }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if args.password:
        primary = summary["checks"].get("login_primary", {})
        me_after = summary["checks"].get("auth_me_after_primary_login", {}).get("body", {})
        login_ok = bool(primary.get("ok") and primary.get("set_cookie"))
        me_ok = bool(isinstance(me_after, dict) and me_after.get("user"))
        if not (login_ok and me_ok):
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
