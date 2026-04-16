# llm-providers

A lightweight CLI tool to chat with multiple LLM providers from the terminal.
Reads API keys from `~/.hermes/.env` and routes requests to any configured backend.

---

## Quick Start

```bash
llm "your question"                          # use default provider
llm -p openrouter:claude-sonnet-4-6 "..."   # specific provider
llm --interactive                            # start a chat session
llm --list                                   # show all providers
llm --use anthropic:claude-sonnet-4-6        # change default
```

---

## Files

| File | Purpose |
|------|---------|
| `~/llm` | CLI entrypoint (executable, on PATH) |
| `~/test_providers.py` | Batch test all configured providers |
| `~/.hermes/.env` | API keys (never committed) |
| `~/.hermes/llm_config.json` | Default provider + settings |
| `~/.hermes/LLM_CLI.md` | Full usage documentation |

---

## Configured Providers

### OpenRouter (via `OPENROUTER_API_KEY`)
Routes to any model through a single API endpoint.

| Key | Model |
|-----|-------|
| `openrouter:gpt-5.4` | GPT-5.4 |
| `openrouter:claude-sonnet-4-6` | Claude Sonnet 4.6 ⬅ default |
| `openrouter:gemini-flash` | Gemini 3 Flash |
| `openrouter:hermes-3-405b` | Hermes 3 405B |
| `openrouter:hermes-3-70b` | Hermes 3 70B |
| `openrouter:hermes-2-pro` | Hermes 2 Pro 8B |

### Anthropic Direct (via `ANTHROPIC_API_KEY`)

| Key | Model |
|-----|-------|
| `anthropic:claude-sonnet-4-6` | Claude Sonnet 4.6 |

### Venice AI (via `VENICE_API_KEY`)
Privacy-first, uncensored models. Base URL: `https://api.venice.ai/api/v1`

| Key | Model |
|-----|-------|
| `venice:glm-4.7` | GLM 4.7 (reasoning) |
| `venice:uncensored` | Venice Uncensored |
| `venice:mistral-31-24b` | Mistral 3.1 24B (vision) |
| `venice:llama-3.3-70b` | Llama 3.3 70B |

### Fireworks AI (via `FIREWORKS_API_KEY`)
Fast open-source model inference. Base URL: `https://api.fireworks.ai/inference/v1`

| Key | Model |
|-----|-------|
| `fireworks:deepseek-v3p2` | DeepSeek V3 P2 |
| `fireworks:kimi-k2p5` | Kimi K2.5 |
| `fireworks:gpt-oss-120b` | GPT OSS 120B |
| `fireworks:glm-5` | GLM-5 |

### Other Providers (require additional API keys)

| Key | Provider | Env Var |
|-----|----------|---------|
| `glm:glm-4-plus` | GLM / z.ai | `GLM_API_KEY` |
| `kimi:kimi-k2.5` | Kimi / Moonshot | `KIMI_API_KEY` |
| `minimax:text-01` | MiniMax | `MINIMAX_API_KEY` |
| `opencode:zen` | OpenCode Zen | `OPENCODE_ZEN_API_KEY` |
| `opencode:go` | OpenCode Go | `OPENCODE_GO_API_KEY` |
| `hf:llama-3-8b` | HuggingFace | `HF_TOKEN` |

### Ollama (Local — no API key required)

| Key | Model | Notes |
|-----|-------|-------|
| `ollama:phi3` | phi3:mini (2.2 GB) | Free, offline, runs at localhost:11434 |

Start Ollama: `sudo systemctl start ollama`
Pull more models: `ollama pull llama3.2`

---

## Installation Summary

| Component | Version | Notes |
|-----------|---------|-------|
| `openai` Python SDK | 2.32.0 | All OpenAI-compatible providers |
| `anthropic` Python SDK | 0.95.0 | Direct Anthropic API |
| Ollama | latest | Local model server, port 11434 |
| phi3:mini | 2.2 GB | Default local model |

---

## Adding API Keys

```bash
nano ~/.hermes/.env
```

Key variables:

```
OPENROUTER_API_KEY=sk-or-v1-...    # openrouter.ai/keys
ANTHROPIC_API_KEY=sk-ant-...       # console.anthropic.com
VENICE_API_KEY=VENICE_ADMIN_KEY_.. # venice.ai/settings/api
FIREWORKS_API_KEY=fw_...           # fireworks.ai/account/api-keys
GLM_API_KEY=...                    # open.bigmodel.cn
KIMI_API_KEY=sk-kimi-...           # platform.kimi.ai
MINIMAX_API_KEY=...                # minimax.io
HF_TOKEN=hf_...                    # huggingface.co/settings/tokens
```

---

## Settings

Edit `~/.hermes/llm_config.json`:

```json
{
  "default_provider": "openrouter:claude-sonnet-4-6",
  "max_tokens": 1024,
  "temperature": 0.7
}
```

---

## Test All Providers

```bash
python3 ~/test_providers.py           # test all configured
python3 ~/test_providers.py --list    # list all provider keys
python3 ~/test_providers.py venice:llama-3.3-70b   # test one
```

---

## Last Test Results (2026-04-16)

| Provider | Status | Fastest |
|----------|--------|---------|
| OpenRouter × 6 | ✅ | Hermes 2 Pro 8B — 1.13s |
| Anthropic Direct | ✅ | 1.99s |
| Venice AI × 4 | ✅ | Mistral 3.1 24B — 0.94s |
| Fireworks AI × 4 | ✅ | GPT OSS 120B — 1.34s |
| Ollama phi3:mini | ✅ | 140s (no GPU) |
