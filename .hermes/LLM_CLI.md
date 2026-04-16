# llm — Multi-Provider LLM CLI

A simple command-line tool to chat with any configured AI provider.
API keys and settings live in `~/.hermes/.env`.

---

## Quick Reference

```bash
llm "your question"                          # use default provider
llm -p <provider-key> "your question"        # use a specific provider
llm --use <provider-key>                     # change default provider
llm --current                                # show active default
llm --list                                   # list all providers + status
llm --interactive                            # start a chat session
llm -i -p <provider-key>                     # chat with a specific provider
```

---

## Configured Providers

| Key | Provider | API Key |
|-----|----------|---------|
| `openrouter:gpt-5.4` | OpenRouter → GPT-5.4 | `OPENROUTER_API_KEY` |
| `openrouter:claude-sonnet-4-6` | OpenRouter → Claude Sonnet 4.6 ⬅ default | `OPENROUTER_API_KEY` |
| `openrouter:gemini-flash` | OpenRouter → Gemini 3 Flash | `OPENROUTER_API_KEY` |
| `openrouter:hermes-3-405b` | OpenRouter → Hermes 3 405B | `OPENROUTER_API_KEY` |
| `openrouter:hermes-3-70b` | OpenRouter → Hermes 3 70B | `OPENROUTER_API_KEY` |
| `openrouter:hermes-2-pro` | OpenRouter → Hermes 2 Pro 8B | `OPENROUTER_API_KEY` |
| `anthropic:claude-sonnet-4-6` | Anthropic Direct → Claude Sonnet 4.6 | `ANTHROPIC_API_KEY` |
| `glm:glm-4-plus` | GLM (z.ai) → GLM-4-Plus | `GLM_API_KEY` |
| `kimi:kimi-k2.5` | Kimi → kimi-k2.5 | `KIMI_API_KEY` |
| `minimax:text-01` | MiniMax → text-01 | `MINIMAX_API_KEY` |
| `opencode:zen` | OpenCode Zen → claude-opus-4.6 | `OPENCODE_ZEN_API_KEY` |
| `opencode:go` | OpenCode Go → GLM-5 | `OPENCODE_GO_API_KEY` |
| `hf:llama-3-8b` | HuggingFace → Llama-3.1-8B-Instruct | `HF_TOKEN` |
| `fireworks:llama-4-maverick` | Fireworks AI → Llama 4 Maverick | `FIREWORKS_API_KEY` |
| `fireworks:llama-4-scout` | Fireworks AI → Llama 4 Scout | `FIREWORKS_API_KEY` |
| `fireworks:deepseek-v3` | Fireworks AI → DeepSeek V3 | `FIREWORKS_API_KEY` |
| `fireworks:qwen3-235b` | Fireworks AI → Qwen3 235B | `FIREWORKS_API_KEY` |
| `ollama:phi3` | Ollama Local → phi3:mini | *(none — free, offline)* |

---

## Files

| File | Purpose |
|------|---------|
| `~/.hermes/.env` | API keys and environment variables |
| `~/.hermes/llm_config.json` | Default provider and settings |
| `~/llm` | CLI script (also at `/usr/local/bin/llm` if installed) |
| `~/test_providers.py` | Batch test script for all providers |

---

## Examples

```bash
# Single questions
llm "What is the difference between TCP and UDP?"
llm -p openrouter:gpt-5.4 "Write a Python function to reverse a string"
llm -p ollama:phi3 "Summarize the concept of RAG"   # works offline

# Switch your default provider
llm --use openrouter:gpt-5.4
llm --use anthropic:claude-sonnet-4-6
llm --use ollama:phi3                               # go fully local

# Interactive chat
llm --interactive
llm -i -p openrouter:gemini-flash

# Inside interactive mode
#   switch openrouter:gpt-5.4   → swap provider mid-chat
#   exit                        → quit
```

---

## Adding API Keys

Edit `~/.hermes/.env` and fill in the keys you have:

```bash
nano ~/.hermes/.env
```

Key variables:

```
OPENROUTER_API_KEY=sk-or-v1-...   # openrouter.ai/keys
ANTHROPIC_API_KEY=sk-ant-...      # console.anthropic.com
GLM_API_KEY=...                   # open.bigmodel.cn
KIMI_API_KEY=sk-kimi-...          # platform.kimi.ai
MINIMAX_API_KEY=...               # minimax.io
OPENCODE_ZEN_API_KEY=...          # opencode.ai/auth
OPENCODE_GO_API_KEY=...          # opencode.ai/auth
FIREWORKS_API_KEY=fw_...          # fireworks.ai/account/api-keys
HF_TOKEN=hf_...                   # huggingface.co/settings/tokens
```

---

## Ollama (Local / Offline)

Ollama is installed and running at `http://localhost:11434`.
Model `phi3:mini` (2.2 GB) is already downloaded.

```bash
# Pull more models
ollama pull llama3.2
ollama pull mistral
ollama list                        # see downloaded models

# Use any pulled model via llm
llm -p ollama:phi3 "your question"
```

To add a new Ollama model to the CLI, add an entry to the `PROVIDERS`
dict in `~/llm` following the pattern of `ollama:phi3`.

---

## Batch Testing

Test all configured providers at once:

```bash
python3 ~/test_providers.py                  # test all with API keys
python3 ~/test_providers.py ollama:phi3      # test one provider
python3 ~/test_providers.py --list           # list provider keys
```

---

## Changing Settings

Edit `~/.hermes/llm_config.json` (auto-created on first `--use`):

```json
{
  "default_provider": "openrouter:claude-sonnet-4-6",
  "max_tokens": 1024,
  "temperature": 0.7
}
```

---

## Setup Summary (what was installed)

| Component | Version | Notes |
|-----------|---------|-------|
| `openai` Python SDK | 2.32.0 | Used for all OpenAI-compatible providers |
| `anthropic` Python SDK | 0.95.0 | Used for direct Anthropic API calls |
| Ollama | latest | Local model server at port 11434 |
| phi3:mini | 2.2 GB | Default local model, no internet needed |
