# Hermes Agent — Configuration

Self-improving AI agent (Nous Research) running on Google AI Studio Gemini 2.5 Pro.

---

## Active Configuration

| Setting | Value |
|---------|-------|
| **Primary model** | `gemini-2.5-pro` |
| **Provider** | `gemini` (Google AI Studio) |
| **Base URL** | `https://generativelanguage.googleapis.com/v1beta` |
| **Fallback model** | `gemini-2.5-flash` (same provider) |
| **Smart routing cheap model** | `gemini-2.5-flash` |
| **Gateway** | systemd user service, auto-start |
| **Telegram** | configured |

---

## Quick Start

```bash
# Single question
hermes -z "Your question here"

# Interactive TUI
hermes

# Check status
hermes status

# View active model
hermes status | grep Model
```

---

## Google AI Studio — Gemini Setup

### 1. Get an API key

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click **Create API key**
3. Copy the key (format: `AIzaSy...`, 39 characters)

### 2. Add the key to Hermes

```bash
hermes auth add gemini --type api-key --label "google-ai-studio-primary"
# Paste your key when prompted
```

Alternatively, set it as an environment variable in `~/.hermes/.env`:

```bash
GOOGLE_API_KEY=AIzaSy...your-key-here
GEMINI_API_KEY=AIzaSy...your-key-here   # optional second slot
```

### 3. Verify the key is registered

```bash
hermes auth list gemini
# Should show your key listed alongside the env-var slots
```

### 4. Test the integration

```bash
# Quick API test via curl
GOOGLE_API_KEY="AIzaSy..."
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent" \
  -H "Content-Type: application/json" \
  -H "X-goog-api-key: $GOOGLE_API_KEY" \
  -X POST \
  -d '{"contents":[{"parts":[{"text":"Say: GEMINI_OK"}]}]}' | python3 -c \
  "import json,sys; r=json.load(sys.stdin); print(r['candidates'][0]['content']['parts'][0]['text'])"

# End-to-end Hermes test
hermes -z "What model are you? Reply in one sentence."
```

---

## Available Gemini Models (this key)

Models confirmed available via `GET /v1beta/models`:

| Model | Notes |
|-------|-------|
| `gemini-2.5-pro` | **Primary** — most capable |
| `gemini-2.5-flash` | **Fallback / cheap routing** — fast and cost-efficient |
| `gemini-2.0-flash` | Available but deprecated for new users |
| `gemini-2.0-flash-lite` | Lightweight variant |
| `gemma-3-27b-it` | Open-weights, Google-hosted |
| `gemini-flash-latest` | Alias for latest Flash |
| `gemini-pro-latest` | Alias for latest Pro |

---

## Switching Models

```bash
# Use a different model for one query
hermes -z "Your question" -m gemini-2.5-flash

# Change the default model permanently
# Edit ~/.hermes/config.yaml:
#   model:
#     default: gemini-2.5-flash   ← change this line
hermes gateway restart            # apply the change
```

---

## Credential Pool

Hermes uses a credential pool for the `gemini` provider with `fill_first` strategy (tries keys in order, skips exhausted ones):

```
#1  GOOGLE_API_KEY          env var lookup
#2  GEMINI_API_KEY          env var lookup
#3  google-ai-studio-primary  stored key (added 2026-04-30)
```

To add another key (e.g. a second account for quota rotation):

```bash
hermes auth add gemini --type api-key --label "google-ai-studio-2"
```

---

## Gateway Management

```bash
hermes gateway restart    # restart after config changes
hermes gateway status     # check if running
hermes status             # full status (model, keys, platform)
hermes doctor             # detailed diagnostics
```

---

## Files

| File | Purpose |
|------|---------|
| `config.yaml` | Main Hermes configuration (tracked in git) |
| `.env` | API keys and environment variables (**not** in git) |
| `auth.json` | Stored credentials / OAuth tokens (**not** in git) |
| `LLM_CLI.md` | Legacy `llm` CLI tool reference |
| `SOUL.md` | Agent personality / system prompt |

---

## Setup History

| Date | Change |
|------|--------|
| 2026-04-18 | Initial Hermes install, multi-provider LLM CLI |
| 2026-04-23 | Switched primary to Kimi / Telegram integration |
| 2026-04-24 | OpenRouter provider added |
| 2026-04-30 | **Switched primary to Google AI Studio `gemini-2.5-pro`** |
