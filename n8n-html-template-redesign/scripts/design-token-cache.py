#!/usr/bin/env python3
"""
Design Token Cache Manager
Caches Opus-generated design tokens to avoid repeated expensive calls.

Usage:
    python design-token-cache.py --save tokens.json --brand maximo-seo --version v3
    python design-token-cache.py --load --brand maximo-seo --version latest
    python design-token-cache.py --list
"""

import argparse
import json
import sys
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "templates" / "design-systems"


def save_tokens(path: Path, brand: str, version: str) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(path, "r", encoding="utf-8") as f:
        tokens = json.load(f)
    out_path = CACHE_DIR / f"{brand}-tokens-{version}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2)
    # Update latest symlink / copy
    latest_path = CACHE_DIR / f"{brand}-tokens-latest.json"
    latest_path.write_text(out_path.read_text(), encoding="utf-8")
    print(f"Saved: {out_path}")
    print(f"Updated latest: {latest_path}")


def load_tokens(brand: str, version: str) -> dict:
    if version == "latest":
        path = CACHE_DIR / f"{brand}-tokens-latest.json"
    else:
        path = CACHE_DIR / f"{brand}-tokens-{version}.json"
    if not path.exists():
        print(f"ERROR: Token file not found: {path}", file=sys.stderr)
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_tokens() -> None:
    if not CACHE_DIR.exists():
        print("No cached tokens.")
        return
    for f in sorted(CACHE_DIR.glob("*.json")):
        size = f.stat().st_size
        print(f"  {f.name} ({size} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Design token cache manager")
    parser.add_argument("--save", help="Path to tokens JSON to cache")
    parser.add_argument("--load", action="store_true", help="Load cached tokens to stdout")
    parser.add_argument("--list", action="store_true", help="List cached tokens")
    parser.add_argument("--brand", default="default", help="Brand slug")
    parser.add_argument("--version", default="latest", help="Version tag or 'latest'")
    args = parser.parse_args()

    if args.save:
        save_tokens(Path(args.save), args.brand, args.version)
        return 0
    if args.load:
        tokens = load_tokens(args.brand, args.version)
        print(json.dumps(tokens, indent=2))
        return 0
    if args.list:
        list_tokens()
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
