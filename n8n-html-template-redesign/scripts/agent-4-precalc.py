#!/usr/bin/env python3
"""
Agent 4 Pre-Compute Scanner
Runs cheap local optimizations and metrics BEFORE calling the Kimi API.
Reduces input size and focuses the agent on AI-hard problems only.

Usage:
    python agent-4-precalc.py --input agent-3-output.html --output precalc.html --metrics metrics.json
"""

import argparse
import json
import re
import sys
from pathlib import Path


def strip_comments(html: str) -> str:
    return re.sub(r"<!--[\s\S]*?-->", "", html)


def collapse_whitespace(html: str) -> str:
    # Preserve whitespace inside <pre> and <textarea>
    def _preserve(match: re.Match) -> str:
        return match.group(0)
    html = re.sub(r"<(pre|textarea)[^>]*>[\s\S]*?</\1>", _preserve, html)
    # Collapse multiple whitespace outside tags
    html = re.sub(r">\s+<", "><", html)
    html = re.sub(r"\s{2,}", " ", html)
    return html


def remove_empty_styles(html: str) -> str:
    return re.sub(r'\s*style=""', "", html)


def remove_empty_classes(html: str) -> str:
    return re.sub(r'\s*class=""', "", html)


def scan_outlook_issues(html: str) -> list[str]:
    issues = []
    if "mso-" not in html and r"<!\[if mso\]>" not in html:
        issues.append("No MSO conditionals detected; may need Outlook fixes")
    if html.count("<table") > 15:
        issues.append("High table count; consider nesting reduction")
    # Check for common Outlook-unfriendly CSS
    if "display: flex" in html:
        issues.append("Flexbox detected; Outlook may fail")
    if "grid-template" in html:
        issues.append("CSS Grid detected; Outlook may fail")
    return issues


def precompute(html: str) -> tuple[str, dict]:
    original_size = len(html.encode("utf-8"))

    html = strip_comments(html)
    html = collapse_whitespace(html)
    html = remove_empty_styles(html)
    html = remove_empty_classes(html)

    optimized_size = len(html.encode("utf-8"))
    inline_styles = len(re.findall(r'style="', html))
    images = len(re.findall(r"<img", html))
    tables = len(re.findall(r"<table", html))
    outlook_issues = scan_outlook_issues(html)

    metrics = {
        "original_bytes": original_size,
        "optimized_bytes": optimized_size,
        "saved_bytes": original_size - optimized_size,
        "saved_percent": round((original_size - optimized_size) / original_size * 100, 1) if original_size else 0,
        "inline_styles": inline_styles,
        "images": images,
        "tables": tables,
        "over_gmail_limit": optimized_size > 102400,
        "over_soft_limit": optimized_size > 80000,
        "outlook_issues": outlook_issues,
        "needs_vml": len(outlook_issues) > 0,
    }
    return html, metrics


def build_prompt(html: str, metrics: dict) -> str:
    focus = []
    if metrics["over_gmail_limit"]:
        focus.append("CRITICAL: reduce size below 102KB")
    if metrics["over_soft_limit"]:
        focus.append("Reduce size below 80KB soft target")
    if metrics["needs_vml"]:
        focus.append("Add Outlook VML/conditional fixes")
    if metrics["inline_styles"] > 30:
        focus.append(f"Consolidate {metrics['inline_styles']} inline styles")

    if not focus:
        focus.append("General polish and compatibility check")

    prompt = f"""HTML stats (pre-computed):
- Size: {metrics['optimized_bytes']} bytes ({'OVER' if metrics['over_gmail_limit'] else 'under'} Gmail limit)
- Inline styles: {metrics['inline_styles']}
- Images: {metrics['images']}
- Tables: {metrics['tables']}
- Outlook issues detected: {len(metrics['outlook_issues'])}

Optimize this HTML. Focus on:
{"\n".join("- " + f for f in focus)}

Output: optimized HTML only. No explanation. No markdown fences."""
    return prompt


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent 4 pre-calc scanner")
    parser.add_argument("--input", "-i", required=True, help="Input HTML")
    parser.add_argument("--output", "-o", required=True, help="Optimized HTML output")
    parser.add_argument("--metrics", "-m", required=True, help="Metrics JSON output")
    parser.add_argument("--prompt-only", action="store_true", help="Print prompt to stdout instead of writing files")
    args = parser.parse_args()

    try:
        html = Path(args.input).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"ERROR: Input not found: {args.input}", file=sys.stderr)
        return 1

    optimized_html, metrics = precompute(html)

    if args.prompt_only:
        print(build_prompt(optimized_html, metrics))
        return 0

    Path(args.output).write_text(optimized_html, encoding="utf-8")
    Path(args.metrics).write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print(f"OK: {args.output} ({metrics['optimized_bytes']} bytes, saved {metrics['saved_percent']}%)")
    print(f"Metrics: {args.metrics}")
    if metrics["over_gmail_limit"]:
        print("WARN: Still over Gmail limit after local optimization", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
