#!/usr/bin/env python3
"""
Multi-provider LLM test script.
Reads API keys from ~/.hermes/.env and tests all configured providers.
Supports: OpenRouter (GPT-4.5, Claude, Gemini, Hermes),
          Anthropic Direct, GLM/z.ai, Kimi, MiniMax,
          OpenCode Zen/Go, HuggingFace, Ollama (local).

Usage:
  python3 test_providers.py                  # test all configured providers
  python3 test_providers.py ollama:phi3       # test one specific provider
  python3 test_providers.py --list           # list all provider keys
"""

import os
import sys
import time
from pathlib import Path

# ── Load ~/.hermes/.env ───────────────────────────────────────────────────────
ENV_FILE = Path.home() / ".hermes" / ".env"

def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            env[key.strip()] = val.strip()
    return env

_env = load_env(ENV_FILE)

def get(key: str, default: str = "") -> str:
    """Get value from environment or .env file."""
    return os.environ.get(key) or _env.get(key, default)


# ── Provider registry ─────────────────────────────────────────────────────────
# Format: key -> (display_label, backend, model_id, base_url, api_key)
PROVIDERS = {

    # ── OpenRouter: routes to every major provider ───────────────────────────
    "openrouter:gpt-5.4": (
        "OpenRouter → GPT-5.4",
        "openai",
        "openai/gpt-5.4",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),
    "openrouter:claude-sonnet-4-6": (
        "OpenRouter → Claude Sonnet 4.6",
        "openai",
        "anthropic/claude-sonnet-4-6",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),
    "openrouter:gemini-flash": (
        "OpenRouter → Gemini 3 Flash",
        "openai",
        "google/gemini-3-flash-preview",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),
    "openrouter:hermes-3-405b": (
        "OpenRouter → Hermes 3 405B",
        "openai",
        "nousresearch/hermes-3-llama-3.1-405b",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),
    "openrouter:hermes-3-70b": (
        "OpenRouter → Hermes 3 70B",
        "openai",
        "nousresearch/hermes-3-llama-3.1-70b",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),
    "openrouter:hermes-2-pro": (
        "OpenRouter → Hermes 2 Pro 8B",
        "openai",
        "nousresearch/hermes-2-pro-llama-3-8b",
        "https://openrouter.ai/api/v1",
        get("OPENROUTER_API_KEY"),
    ),

    # ── Anthropic Direct (needs ANTHROPIC_API_KEY, not OpenRouter) ───────────
    "anthropic:claude-sonnet-4-6": (
        "Anthropic Direct → Claude Sonnet 4.6",
        "anthropic",
        "claude-sonnet-4-6",
        None,
        get("ANTHROPIC_API_KEY"),
    ),

    # ── GLM / z.ai ───────────────────────────────────────────────────────────
    "glm:glm-4-plus": (
        "GLM (z.ai) → GLM-4-Plus",
        "openai",
        "glm-4-plus",
        get("GLM_BASE_URL", "https://api.z.ai/api/paas/v4"),
        get("GLM_API_KEY"),
    ),

    # ── Kimi / Moonshot ──────────────────────────────────────────────────────
    "kimi:kimi-k2.5": (
        "Kimi → kimi-k2.5",
        "openai",
        "kimi-k2.5",
        get("KIMI_BASE_URL", "https://api.kimi.com/coding/v1"),
        get("KIMI_API_KEY"),
    ),

    # ── MiniMax ──────────────────────────────────────────────────────────────
    "minimax:text-01": (
        "MiniMax → text-01",
        "openai",
        "text-01",
        get("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
        get("MINIMAX_API_KEY"),
    ),

    # ── OpenCode Zen ─────────────────────────────────────────────────────────
    "opencode:zen": (
        "OpenCode Zen → claude-opus-4.6",
        "openai",
        "anthropic/claude-opus-4.6",
        get("OPENCODE_ZEN_BASE_URL", "https://opencode.ai/zen/v1"),
        get("OPENCODE_ZEN_API_KEY"),
    ),

    # ── OpenCode Go ──────────────────────────────────────────────────────────
    "opencode:go": (
        "OpenCode Go → GLM-5",
        "openai",
        "zhipuai/glm-5",
        get("OPENCODE_GO_BASE_URL", "https://opencode.ai/zen/go/v1"),
        get("OPENCODE_GO_API_KEY"),
    ),

    # ── Hugging Face Inference ────────────────────────────────────────────────
    "hf:llama-3-8b": (
        "HuggingFace → Llama-3.1-8B-Instruct",
        "openai",
        "meta-llama/Llama-3.1-8B-Instruct",
        "https://api-inference.huggingface.co/v1",
        get("HF_TOKEN"),
    ),

    # ── Venice AI ────────────────────────────────────────────────────────────
    "venice:glm-4.7": (
        "Venice AI → GLM 4.7 (reasoning)",
        "openai",
        "zai-org-glm-4.7",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:uncensored": (
        "Venice AI → Venice Uncensored",
        "openai",
        "venice-uncensored",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:mistral-31-24b": (
        "Venice AI → Mistral 3.1 24B (vision)",
        "openai",
        "mistral-31-24b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:llama-3.3-70b": (
        "Venice AI → Llama 3.3 70B",
        "openai",
        "llama-3.3-70b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),

    # ── Fireworks AI ───────────────────────────────────────────────────────
    "fireworks:deepseek-v3p2": (
        "Fireworks AI → DeepSeek V3 P2",
        "openai",
        "accounts/fireworks/models/deepseek-v3p2",
        "https://api.fireworks.ai/inference/v1",
        get("FIREWORKS_API_KEY"),
    ),
    "fireworks:kimi-k2p5": (
        "Fireworks AI → Kimi K2.5",
        "openai",
        "accounts/fireworks/models/kimi-k2p5",
        "https://api.fireworks.ai/inference/v1",
        get("FIREWORKS_API_KEY"),
    ),
    "fireworks:gpt-oss-120b": (
        "Fireworks AI → GPT OSS 120B",
        "openai",
        "accounts/fireworks/models/gpt-oss-120b",
        "https://api.fireworks.ai/inference/v1",
        get("FIREWORKS_API_KEY"),
    ),
    "fireworks:glm-5": (
        "Fireworks AI → GLM-5",
        "openai",
        "accounts/fireworks/models/glm-5",
        "https://api.fireworks.ai/inference/v1",
        get("FIREWORKS_API_KEY"),
    ),

    # ── Ollama (local, no key required) ──────────────────────────────────────
    "ollama:phi3": (
        "Ollama Local → phi3:mini",
        "openai",
        "phi3:mini",
        "http://localhost:11434/v1",
        "ollama",  # dummy key; Ollama doesn't require auth
    ),
}

PROMPT = "In one sentence, what is the capital of France and why is it famous?"


# ── Backend callers ───────────────────────────────────────────────────────────
def call_openai(model: str, base_url: str, api_key: str) -> dict:
    from openai import OpenAI
    client = OpenAI(base_url=base_url, api_key=api_key or "no-key")
    start = time.time()
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": PROMPT}],
            max_tokens=150,
            temperature=0.7,
        )
        elapsed = time.time() - start
        content = resp.choices[0].message.content
        tokens = resp.usage.total_tokens if resp.usage else "N/A"
        return {"status": "ok", "response": content, "tokens": tokens, "time": elapsed}
    except Exception as e:
        return {"status": "error", "error": str(e), "time": time.time() - start}


def call_anthropic(model: str, api_key: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    start = time.time()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=150,
            messages=[{"role": "user", "content": PROMPT}],
        )
        elapsed = time.time() - start
        content = resp.content[0].text
        tokens = resp.usage.input_tokens + resp.usage.output_tokens
        return {"status": "ok", "response": content, "tokens": tokens, "time": elapsed}
    except Exception as e:
        return {"status": "error", "error": str(e), "time": time.time() - start}


# ── Main runner ───────────────────────────────────────────────────────────────
def run(filter_key: str | None = None):
    # Build target list
    if filter_key:
        if filter_key not in PROVIDERS:
            print(f"Unknown provider '{filter_key}'.")
            print("Available keys:")
            for k in PROVIDERS:
                print(f"  {k}")
            return
        targets = {filter_key: PROVIDERS[filter_key]}
    else:
        # Auto-skip providers with no API key set
        targets = {}
        for k, v in PROVIDERS.items():
            label, backend, model, base_url, api_key = v
            has_key = api_key and api_key not in ("",)
            if has_key:
                targets[k] = v

    if not targets:
        print("No providers have API keys configured.")
        print("Set keys in ~/.hermes/.env or as environment variables.")
        print("Provider keys:", list(PROVIDERS.keys()))
        return

    print(f"Prompt : {PROMPT}")
    print(f"Testing: {len(targets)} provider(s)\n")

    results = []
    for key, (label, backend, model, base_url, api_key) in targets.items():
        print(f"\n{'='*62}")
        print(f" {label}")
        print(f" Model: {model}")
        print(f"{'='*62}")

        if backend == "anthropic":
            if not api_key:
                print(" SKIPPED — ANTHROPIC_API_KEY not set")
                results.append({"key": key, "label": label, "status": "skipped", "time": 0})
                continue
            result = call_anthropic(model, api_key)
        else:
            result = call_openai(model, base_url, api_key)

        result["key"] = key
        result["label"] = label

        if result["status"] == "ok":
            print(f" Response : {result['response']}")
            print(f" Tokens   : {result.get('tokens', 'N/A')} | Time: {result['time']:.2f}s")
        else:
            print(f" Error    : {result['error']}")

        results.append(result)
        time.sleep(0.3)

    # ── Summary ───────────────────────────────────────────────────────────────
    ok      = [r for r in results if r["status"] == "ok"]
    skipped = [r for r in results if r["status"] == "skipped"]
    failed  = [r for r in results if r["status"] == "error"]

    print(f"\n{'='*62}")
    print(" SUMMARY")
    print(f"{'='*62}")
    print(f" Passed  : {len(ok)}/{len(results)}")
    if skipped:
        print(f" Skipped : {', '.join(r['key'] for r in skipped)}")
    if failed:
        print(f" Failed  : {', '.join(r['key'] for r in failed)}")
    if ok:
        fastest = min(ok, key=lambda r: r["time"])
        print(f" Fastest : {fastest['label']} ({fastest['time']:.2f}s)")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--list":
        print("Available provider keys:")
        for k, (label, *_) in PROVIDERS.items():
            print(f"  {k:<35}  {label}")
    else:
        run(args[0] if args else None)
