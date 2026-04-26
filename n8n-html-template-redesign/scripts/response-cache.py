#!/usr/bin/env python3
"""
Simple file-based response cache for sub-agent calls.
Key: SHA256(model + prompt + pipeline_type)
Value: cached response JSON

Usage:
    python response-cache.py --get --model gpt-5.5 --prompt "..." --pipeline full
    python response-cache.py --set --model gpt-5.5 --prompt "..." --pipeline full --response response.json
    python response-cache.py --clear
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

CACHE_DIR = Path(__file__).parent.parent / "runs" / "cache"
CACHE_TTL_SECONDS = 3600  # 1 hour default


def _cache_key(model: str, prompt: str, pipeline: str) -> str:
    data = f"{model}::{pipeline}::{prompt}"
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _cache_path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / f"{key}.json"


def get_cached(model: str, prompt: str, pipeline: str) -> dict | None:
    key = _cache_key(model, prompt, pipeline)
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        # Simple TTL check
        import time
        if time.time() - data.get("cached_at", 0) > CACHE_TTL_SECONDS:
            path.unlink()
            return None
        return data.get("response")
    except (json.JSONDecodeError, OSError):
        return None


def set_cached(model: str, prompt: str, pipeline: str, response: dict) -> None:
    key = _cache_key(model, prompt, pipeline)
    path = _cache_path(key)
    import time
    data = {
        "cached_at": time.time(),
        "model": model,
        "pipeline": pipeline,
        "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
        "response": response,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Cached: {path}")


def clear_cache() -> None:
    if not CACHE_DIR.exists():
        print("Cache directory does not exist.")
        return
    count = 0
    for f in CACHE_DIR.glob("*.json"):
        f.unlink()
        count += 1
    print(f"Cleared {count} cached entries.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Response cache manager")
    parser.add_argument("--get", action="store_true", help="Retrieve cached response")
    parser.add_argument("--set", action="store_true", help="Store response in cache")
    parser.add_argument("--clear", action="store_true", help="Clear all cached entries")
    parser.add_argument("--model", default="", help="Model name")
    parser.add_argument("--prompt", default="", help="Prompt text")
    parser.add_argument("--pipeline", default="full", help="Pipeline type")
    parser.add_argument("--response", help="JSON file with response to cache")
    parser.add_argument("--ttl", type=int, default=CACHE_TTL_SECONDS, help="TTL in seconds")
    args = parser.parse_args()

    if args.clear:
        clear_cache()
        return 0

    if args.get:
        result = get_cached(args.model, args.prompt, args.pipeline)
        if result is None:
            print("MISS")
            return 1
        print(json.dumps(result, indent=2))
        return 0

    if args.set:
        if not args.response:
            print("ERROR: --response required with --set", file=sys.stderr)
            return 1
        with open(args.response, "r", encoding="utf-8") as f:
            response = json.load(f)
        set_cached(args.model, args.prompt, args.pipeline, response)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
