#!/usr/bin/env python3
"""Production/browser QA for the Template Improvements dashboard page.

This script intentionally avoids printing credentials. It can authenticate in two ways:

1. Preferred for CI/local secure runs: provide DASHBOARD_USER and DASHBOARD_PASSWORD.
2. On the Hermes VPS only: pass --use-render-env to fetch those values from Render env-vars
   using the stored Render API key in ~/.hermes/secure/logins.json.

It validates the Template Improvements page across common responsive viewports:
- page exists and opens through the same showPage() mechanism used by dashboard tabs
- required controls are present
- all five agent markers are present
- no horizontal overflow
- no console errors or failed requests
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

DEFAULT_BASE_URL = "https://html-redesign-dashboard.maximo-seo.ai"
DEFAULT_RENDER_SERVICE_ID = "srv-d75p488gjchc73eta3i0"
DEFAULT_VIEWPORTS = [
    ("desktop", 1440, 1000),
    ("laptop", 1280, 800),
    ("tablet", 768, 1024),
    ("mobile", 390, 844),
]
REQUIRED_CONTROLS = [
    "ti-domain",
    "ti-subdomain",
    "ti-template-name",
    "ti-original-html",
    "ti-change-instructions",
    "ti-jobs-list",
]
REQUIRED_AGENTS = [
    "gpt-5.4-agent",
    "opus-4.7-agent",
    "gemini-3.1-agent",
    "kimi-k2.6-agent",
    "glm-4.6-agent",
]
IGNORED_CONSOLE_PATTERNS = re.compile(
    r"favicon|ResizeObserver loop|net::ERR_ABORTED",
    re.IGNORECASE,
)


def _load_render_env(service_id: str) -> dict[str, str]:
    secrets_path = Path.home() / ".hermes" / "secure" / "logins.json"
    if not secrets_path.exists():
        raise RuntimeError("missing ~/.hermes/secure/logins.json for --use-render-env")
    secure = json.loads(secrets_path.read_text(encoding="utf-8"))
    token = (secure.get("render_webs") or {}).get("api_key")
    if not token:
        raise RuntimeError("missing render_webs.api_key in secure logins for --use-render-env")
    req = urllib.request.Request(
        f"https://api.render.com/v1/services/{service_id}/env-vars?limit=100",
        headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=25) as response:
        env_data = json.loads(response.read().decode("utf-8"))
    env: dict[str, str] = {}
    for item in env_data:
        row = item.get("envVar", item) if isinstance(item, dict) else {}
        key = row.get("key")
        if key:
            env[key] = row.get("value", "")
    return env


def _credentials(args: argparse.Namespace) -> tuple[str, str]:
    env = os.environ.copy()
    if args.use_render_env:
        env.update(_load_render_env(args.render_service_id))
    user = env.get("DASHBOARD_USER") or env.get("DASHBOARD_EMAIL")
    password = env.get("DASHBOARD_PASSWORD")
    if not user or not password:
        raise RuntimeError(
            "missing dashboard credentials; set DASHBOARD_USER/DASHBOARD_PASSWORD "
            "or use --use-render-env on the Hermes VPS"
        )
    return user, password


def run(args: argparse.Namespace) -> dict:
    base_url = args.base_url.rstrip("/")
    user, password = _credentials(args)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary = []
    critical_console = []
    request_failures = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for name, width, height in DEFAULT_VIEWPORTS:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                ignore_https_errors=True,
            )
            page = context.new_page()
            console_messages = []
            failures = []
            page.on(
                "console",
                lambda msg, messages=console_messages: messages.append(
                    {"type": msg.type, "text": msg.text[:500]}
                ),
            )
            page.on(
                "pageerror",
                lambda exc, messages=console_messages: messages.append(
                    {"type": "pageerror", "text": str(exc)[:500]}
                ),
            )
            page.on(
                "response",
                lambda resp, rows=failures: rows.append(
                    {"url": resp.url, "status": resp.status}
                )
                if resp.status >= 400
                else None,
            )

            page.goto(base_url + "/", wait_until="domcontentloaded", timeout=60_000)
            if "/login" in page.url:
                page.fill(
                    'input[name="user"], input[type="email"], input[autocomplete="username"]',
                    user,
                )
                page.fill('input[name="password"], input[type="password"]', password)
                page.click('button[type="submit"], button:has-text("Sign in")')
                try:
                    page.wait_for_url(lambda url: "/login" not in url, timeout=30_000)
                except PlaywrightTimeoutError:
                    page.goto(base_url + "/", wait_until="domcontentloaded", timeout=60_000)

            page.wait_for_function(
                "() => typeof window.showPage === 'function' && document.getElementById('page-template-improvements')",
                timeout=60_000,
            )
            page.evaluate("window.showPage('template-improvements')")
            page.wait_for_timeout(1500)

            checks = page.evaluate(
                """
                ({ requiredControls, requiredAgents }) => {
                  const page = document.getElementById('page-template-improvements');
                  const style = page ? getComputedStyle(page) : null;
                  const html = document.documentElement.innerHTML;
                  const rect = page ? page.getBoundingClientRect() : null;
                  const tab = document.querySelector('[data-testid="tab-template-improvements"], #tab-template-improvements');
                  return {
                    pageExists: !!page,
                    display: style ? style.display : null,
                    active: page ? page.classList.contains('active') : false,
                    titleVisible: document.body.innerText.includes('Template Improvements'),
                    controls: requiredControls.filter(id => !!document.getElementById(id)),
                    agents: requiredAgents.filter(agent => html.includes(agent)),
                    stableTabHook: !!tab,
                    stablePageHook: !!document.querySelector('[data-testid="page-template-improvements"], #page-template-improvements'),
                    startFn: typeof window.templateImprovementsStartJob === 'function',
                    loadFn: typeof window.templateImprovementsLoadJobs === 'function',
                    bodyScrollWidth: document.body.scrollWidth,
                    viewportWidth: window.innerWidth,
                    horizontalOverflow: document.body.scrollWidth > window.innerWidth + 6,
                    pageTop: rect ? Math.round(rect.top) : null,
                    pageWidth: rect ? Math.round(rect.width) : null
                  };
                }
                """,
                {"requiredControls": REQUIRED_CONTROLS, "requiredAgents": REQUIRED_AGENTS},
            )

            screenshot_path = output_dir / f"{name}-template-improvements.png"
            page.screenshot(path=str(screenshot_path), full_page=True)

            errors = [
                row
                for row in console_messages
                if row["type"] in ("error", "pageerror")
                and not IGNORED_CONSOLE_PATTERNS.search(row["text"])
            ]
            real_failures = []
            for row in failures:
                if "favicon" in row["url"]:
                    continue
                real_failures.append(row)

            critical_console.extend({"viewport": name, **row} for row in errors)
            request_failures.extend({"viewport": name, **row} for row in real_failures)
            summary.append(
                {
                    "viewport": name,
                    "size": f"{width}x{height}",
                    "url": page.url,
                    "checks": checks,
                    "console_errors": len(errors),
                    "request_failures": len(real_failures),
                    "screenshot": str(screenshot_path),
                }
            )
            context.close()
        browser.close()

    ok = all(
        row["checks"]["pageExists"]
        and row["checks"]["display"] != "none"
        and row["checks"]["active"]
        and row["checks"]["titleVisible"]
        and len(row["checks"]["controls"]) == len(REQUIRED_CONTROLS)
        and len(row["checks"]["agents"]) == len(REQUIRED_AGENTS)
        and row["checks"]["stableTabHook"]
        and row["checks"]["stablePageHook"]
        and row["checks"]["startFn"]
        and row["checks"]["loadFn"]
        and not row["checks"]["horizontalOverflow"]
        for row in summary
    ) and not critical_console and not request_failures

    return {
        "ok": ok,
        "base_url": base_url,
        "summary": summary,
        "critical_console": critical_console[:25],
        "request_failures": request_failures[:25],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--output-dir", default="/tmp/dashboard-template-improvements-qa")
    parser.add_argument("--use-render-env", action="store_true")
    parser.add_argument("--render-service-id", default=DEFAULT_RENDER_SERVICE_ID)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
