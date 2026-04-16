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

    # ── Venice AI (all models) ──────────────────────────────────────────────
    "venice:zai-org-glm-5-1": (
        "Venice → zai-org-glm-5-1  [ctx:200000]",
        "openai", "zai-org-glm-5-1",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:zai-org-glm-5": (
        "Venice → zai-org-glm-5  [ctx:198000]",
        "openai", "zai-org-glm-5",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:z-ai-glm-5-turbo": (
        "Venice → z-ai-glm-5-turbo  [ctx:200000]",
        "openai", "z-ai-glm-5-turbo",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:z-ai-glm-5v-turbo": (
        "Venice → z-ai-glm-5v-turbo  [ctx:200000]",
        "openai", "z-ai-glm-5v-turbo",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:olafangensan-glm-4-7-flash-heretic": (
        "Venice → olafangensan-glm-4.7-flash-heretic  [ctx:200000]",
        "openai", "olafangensan-glm-4.7-flash-heretic",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:zai-org-glm-4-7-flash": (
        "Venice → zai-org-glm-4.7-flash  [ctx:128000]",
        "openai", "zai-org-glm-4.7-flash",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:zai-org-glm-4-6": (
        "Venice → zai-org-glm-4.6  [ctx:198000]",
        "openai", "zai-org-glm-4.6",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:zai-org-glm-4-7": (
        "Venice → zai-org-glm-4.7  [ctx:198000]",
        "openai", "zai-org-glm-4.7",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:venice-uncensored": (
        "Venice → venice-uncensored  [ctx:32000]",
        "openai", "venice-uncensored",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:venice-uncensored-role-play": (
        "Venice → venice-uncensored-role-play  [ctx:128000]",
        "openai", "venice-uncensored-role-play",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen-3-6-plus": (
        "Venice → qwen-3-6-plus  [ctx:1000000]",
        "openai", "qwen-3-6-plus",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-5-9b": (
        "Venice → qwen3-5-9b  [ctx:256000]",
        "openai", "qwen3-5-9b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-5-397b-a17b": (
        "Venice → qwen3-5-397b-a17b  [ctx:128000]",
        "openai", "qwen3-5-397b-a17b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-5-35b-a3b": (
        "Venice → qwen3-5-35b-a3b  [ctx:256000]",
        "openai", "qwen3-5-35b-a3b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-235b-a22b-thinking-2507": (
        "Venice → qwen3-235b-a22b-thinking-2507  [ctx:128000]",
        "openai", "qwen3-235b-a22b-thinking-2507",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-235b-a22b-instruct-2507": (
        "Venice → qwen3-235b-a22b-instruct-2507  [ctx:128000]",
        "openai", "qwen3-235b-a22b-instruct-2507",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-next-80b": (
        "Venice → qwen3-next-80b  [ctx:256000]",
        "openai", "qwen3-next-80b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-coder-480b-a35b-instruct": (
        "Venice → qwen3-coder-480b-a35b-instruct  [ctx:256000]",
        "openai", "qwen3-coder-480b-a35b-instruct",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-vl-235b-a22b": (
        "Venice → qwen3-vl-235b-a22b  [ctx:256000]",
        "openai", "qwen3-vl-235b-a22b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:qwen3-coder-480b-a35b-instruct-turbo": (
        "Venice → qwen3-coder-480b-a35b-instruct-turbo  [ctx:256000]",
        "openai", "qwen3-coder-480b-a35b-instruct-turbo",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:google-gemma-4-26b-a4b-it": (
        "Venice → google-gemma-4-26b-a4b-it  [ctx:256000]",
        "openai", "google-gemma-4-26b-a4b-it",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:google-gemma-4-31b-it": (
        "Venice → google-gemma-4-31b-it  [ctx:256000]",
        "openai", "google-gemma-4-31b-it",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:google-gemma-3-27b-it": (
        "Venice → google-gemma-3-27b-it  [ctx:198000]",
        "openai", "google-gemma-3-27b-it",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:arcee-trinity-large-thinking": (
        "Venice → arcee-trinity-large-thinking  [ctx:256000]",
        "openai", "arcee-trinity-large-thinking",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:grok-41-fast": (
        "Venice → grok-41-fast  [ctx:1000000]",
        "openai", "grok-41-fast",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:grok-4-20": (
        "Venice → grok-4-20  [ctx:2000000]",
        "openai", "grok-4-20",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:grok-4-20-multi-agent": (
        "Venice → grok-4-20-multi-agent  [ctx:2000000]",
        "openai", "grok-4-20-multi-agent",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:mistral-small-3-2-24b-instruct": (
        "Venice → mistral-small-3-2-24b-instruct  [ctx:256000]",
        "openai", "mistral-small-3-2-24b-instruct",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:mistral-small-2603": (
        "Venice → mistral-small-2603  [ctx:256000]",
        "openai", "mistral-small-2603",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:hermes-3-llama-3-1-405b": (
        "Venice → hermes-3-llama-3.1-405b  [ctx:128000]",
        "openai", "hermes-3-llama-3.1-405b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:gemini-3-1-pro-preview": (
        "Venice → gemini-3-1-pro-preview  [ctx:1000000]",
        "openai", "gemini-3-1-pro-preview",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:gemini-3-flash-preview": (
        "Venice → gemini-3-flash-preview  [ctx:256000]",
        "openai", "gemini-3-flash-preview",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:claude-opus-4-6": (
        "Venice → claude-opus-4-6  [ctx:1000000]",
        "openai", "claude-opus-4-6",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:claude-opus-4-6-fast": (
        "Venice → claude-opus-4-6-fast  [ctx:1000000]",
        "openai", "claude-opus-4-6-fast",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:claude-opus-4-5": (
        "Venice → claude-opus-4-5  [ctx:198000]",
        "openai", "claude-opus-4-5",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:claude-sonnet-4-6": (
        "Venice → claude-sonnet-4-6  [ctx:1000000]",
        "openai", "claude-sonnet-4-6",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:claude-sonnet-4-5": (
        "Venice → claude-sonnet-4-5  [ctx:198000]",
        "openai", "claude-sonnet-4-5",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-oss-120b": (
        "Venice → openai-gpt-oss-120b  [ctx:128000]",
        "openai", "openai-gpt-oss-120b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:kimi-k2-thinking": (
        "Venice → kimi-k2-thinking  [ctx:256000]",
        "openai", "kimi-k2-thinking",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:kimi-k2-5": (
        "Venice → kimi-k2-5  [ctx:256000]",
        "openai", "kimi-k2-5",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:deepseek-v3-2": (
        "Venice → deepseek-v3.2  [ctx:160000]",
        "openai", "deepseek-v3.2",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:aion-labs-aion-2-0": (
        "Venice → aion-labs-aion-2-0  [ctx:128000]",
        "openai", "aion-labs-aion-2-0",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:llama-3-2-3b": (
        "Venice → llama-3.2-3b  [ctx:128000]",
        "openai", "llama-3.2-3b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:llama-3-3-70b": (
        "Venice → llama-3.3-70b  [ctx:128000]",
        "openai", "llama-3.3-70b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-52": (
        "Venice → openai-gpt-52  [ctx:256000]",
        "openai", "openai-gpt-52",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-52-codex": (
        "Venice → openai-gpt-52-codex  [ctx:256000]",
        "openai", "openai-gpt-52-codex",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-53-codex": (
        "Venice → openai-gpt-53-codex  [ctx:400000]",
        "openai", "openai-gpt-53-codex",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-54": (
        "Venice → openai-gpt-54  [ctx:1000000]",
        "openai", "openai-gpt-54",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-54-pro": (
        "Venice → openai-gpt-54-pro  [ctx:1000000]",
        "openai", "openai-gpt-54-pro",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-54-mini": (
        "Venice → openai-gpt-54-mini  [ctx:400000]",
        "openai", "openai-gpt-54-mini",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-4o-2024-11-20": (
        "Venice → openai-gpt-4o-2024-11-20  [ctx:128000]",
        "openai", "openai-gpt-4o-2024-11-20",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:openai-gpt-4o-mini-2024-07-18": (
        "Venice → openai-gpt-4o-mini-2024-07-18  [ctx:128000]",
        "openai", "openai-gpt-4o-mini-2024-07-18",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:minimax-m25": (
        "Venice → minimax-m25  [ctx:198000]",
        "openai", "minimax-m25",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:minimax-m27": (
        "Venice → minimax-m27  [ctx:198000]",
        "openai", "minimax-m27",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:mercury-2": (
        "Venice → mercury-2  [ctx:128000]",
        "openai", "mercury-2",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:nvidia-nemotron-3-nano-30b-a3b": (
        "Venice → nvidia-nemotron-3-nano-30b-a3b  [ctx:128000]",
        "openai", "nvidia-nemotron-3-nano-30b-a3b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:nvidia-nemotron-cascade-2-30b-a3b": (
        "Venice → nvidia-nemotron-cascade-2-30b-a3b  [ctx:256000]",
        "openai", "nvidia-nemotron-cascade-2-30b-a3b",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-venice-uncensored-24b-p": (
        "Venice → e2ee-venice-uncensored-24b-p  [ctx:32000]",
        "openai", "e2ee-venice-uncensored-24b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-gemma-3-27b-p": (
        "Venice → e2ee-gemma-3-27b-p  [ctx:40000]",
        "openai", "e2ee-gemma-3-27b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-glm-4-7-p": (
        "Venice → e2ee-glm-4-7-p  [ctx:128000]",
        "openai", "e2ee-glm-4-7-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-glm-4-7-flash-p": (
        "Venice → e2ee-glm-4-7-flash-p  [ctx:198000]",
        "openai", "e2ee-glm-4-7-flash-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-gpt-oss-20b-p": (
        "Venice → e2ee-gpt-oss-20b-p  [ctx:128000]",
        "openai", "e2ee-gpt-oss-20b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-gpt-oss-120b-p": (
        "Venice → e2ee-gpt-oss-120b-p  [ctx:128000]",
        "openai", "e2ee-gpt-oss-120b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-qwen-2-5-7b-p": (
        "Venice → e2ee-qwen-2-5-7b-p  [ctx:32000]",
        "openai", "e2ee-qwen-2-5-7b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-qwen3-30b-a3b-p": (
        "Venice → e2ee-qwen3-30b-a3b-p  [ctx:256000]",
        "openai", "e2ee-qwen3-30b-a3b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-qwen3-vl-30b-a3b-p": (
        "Venice → e2ee-qwen3-vl-30b-a3b-p  [ctx:128000]",
        "openai", "e2ee-qwen3-vl-30b-a3b-p",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-glm-5": (
        "Venice → e2ee-glm-5  [ctx:198000]",
        "openai", "e2ee-glm-5",
        "https://api.venice.ai/api/v1",
        get("VENICE_API_KEY"),
    ),
    "venice:e2ee-qwen3-5-122b-a10b": (
        "Venice → e2ee-qwen3-5-122b-a10b  [ctx:128000]",
        "openai", "e2ee-qwen3-5-122b-a10b",
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
    "fireworks:minimax-m2p7": (
        "Fireworks AI → MiniMax M2.7",
        "openai",
        "accounts/fireworks/models/minimax-m2p7",
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
    "fireworks:glm-5p1": (
        "Fireworks AI → GLM-5 P1",
        "openai",
        "accounts/fireworks/models/glm-5p1",
        "https://api.fireworks.ai/inference/v1",
        get("FIREWORKS_API_KEY"),
    ),
    "fireworks:qwen3p6-plus": (
        "Fireworks AI → Qwen3 P6 Plus",
        "openai",
        "accounts/fireworks/models/qwen3p6-plus",
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
