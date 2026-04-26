#!/usr/bin/env python3
"""
Agent 5 Local Replacement
Handles mechanical work: variable substitution, UTM tagging, tracking pixel, metadata.
Zero API cost. Skips GLM/Z.ai entirely for standard runs.

Usage:
    python agent-5-local.py \
        --input templates/agent-4-output.html \
        --output templates/final.html \
        --campaign-id "{{$json.campaign_id}}" \
        --tracking-pixel "{{$json.tracking_pixel_url}}"
"""

import argparse
import re
import sys
from datetime import datetime, timezone

# Standard variable mapping: placeholder -> n8n expression
DEFAULT_VARIABLE_MAP = {
    "{{TITLE}}": "{{$json.article_title}}",
    "{{SUBTITLE}}": "{{$json.article_subtitle}}",
    "{{AUTHOR}}": "{{$json.author_name}}",
    "{{DATE}}": "{{$json.publish_date}}",
    "{{HERO_IMAGE}}": "{{$json.hero_image_url}}",
    "{{BODY}}": "{{$json.article_body}}",
    "{{SOURCE_URL}}": "{{$json.source_url}}",
    "{{CAMPAIGN_ID}}": "{{$json.campaign_id}}",
    "{{UNSUBSCRIBE_URL}}": "{{$json.unsubscribe_url}}",
    "{{FORWARD_URL}}": "{{$json.forward_url}}",
}


def replace_variables(html: str, custom_map: dict | None = None) -> str:
    """Swap placeholders for n8n expressions."""
    var_map = {**DEFAULT_VARIABLE_MAP, **(custom_map or {})}
    for placeholder, n8n_expr in var_map.items():
        html = html.replace(placeholder, n8n_expr)
    return html


def append_utm_params(html: str, campaign_id: str = "{{$json.campaign_id}}") -> str:
    """Append UTM tracking to all external http/https links."""
    utm = f"utm_source=newsletter&utm_medium=email&utm_campaign={campaign_id}"

    def _utm_replacer(match: re.Match) -> str:
        url = match.group(1)
        if url.startswith(("mailto:", "tel:", "#")):
            return match.group(0)
        sep = "&" if "?" in url else "?"
        return f'href="{url}{sep}{utm}"'

    return re.sub(r'href="(https?://[^"]+)"', _utm_replacer, html)


def insert_tracking_pixel(html: str, pixel_url: str) -> str:
    """Append 1x1 tracking pixel before closing </body>."""
    pixel_tag = (
        f'<img src="{pixel_url}" width="1" height="1" alt="" '
        'style="display:none;border:0;" />'
    )
    # Insert before </body> if present; otherwise append at end
    if "</body>" in html:
        return html.replace("</body>", f"{pixel_tag}</body>")
    return html + pixel_tag


def add_version_metadata(html: str, version: str | None = None) -> str:
    """Insert HTML comment with generation metadata."""
    version = version or datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    meta = f"<!-- Generated: {version} | Pipeline: n8n-html-template-redesign | Agent5: local -->\n"
    return meta + html


def validate_n8n_syntax(html: str) -> list[str]:
    """Check for broken n8n placeholders (unclosed brackets, nested braces, etc.)."""
    issues = []
    # Find all {{...}} expressions properly
    for match in re.finditer(r"\{\{([^{}]*)\}\}", html):
        inner = match.group(1)
        if not inner.strip():
            issues.append(f"Empty expression at position {match.start()}")
    # Check for unclosed {{ (opening brace without closing }}}
    open_count = html.count("{{")
    close_count = html.count("}}")
    if open_count != close_count:
        issues.append(f"Mismatched braces: {open_count} open, {close_count} close")
    # Check for nested braces inside expressions (simplified)
    for match in re.finditer(r"\{\{[^{}]*\{\{[^{}]*\}\}[^{}]*\}\}", html):
        issues.append(f"Nested expression (may be invalid): {match.group(0)[:50]}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent 5 local mechanical integration")
    parser.add_argument("--input", "-i", required=True, help="Input HTML file path")
    parser.add_argument("--output", "-o", required=True, help="Output HTML file path")
    parser.add_argument("--campaign-id", default="{{$json.campaign_id}}", help="Campaign ID for UTM")
    parser.add_argument("--tracking-pixel", default="{{$json.tracking_pixel_url}}", help="Tracking pixel URL")
    parser.add_argument("--version", default=None, help="Version string (default: UTC timestamp)")
    parser.add_argument("--custom-map", default=None, help="JSON file with extra placeholder mappings")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        return 1

    custom_map = None
    if args.custom_map:
        import json
        with open(args.custom_map, "r", encoding="utf-8") as f:
            custom_map = json.load(f)

    html = replace_variables(html, custom_map)
    html = append_utm_params(html, args.campaign_id)
    html = insert_tracking_pixel(html, args.tracking_pixel)
    html = add_version_metadata(html, args.version)

    issues = validate_n8n_syntax(html)
    if issues:
        print("WARN: n8n validation issues found:", file=sys.stderr)
        for issue in issues:
            print(f"  - {issue}", file=sys.stderr)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    size = len(html.encode("utf-8"))
    print(f"OK: {args.output} ({size} bytes)")
    if size > 102400:
        print("WARN: HTML exceeds Gmail 102KB clipping threshold", file=sys.stderr)
    elif size > 80000:
        print("WARN: HTML exceeds 80KB soft target", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
