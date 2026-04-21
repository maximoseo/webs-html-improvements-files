# Telegram AI Bot — Oz CLI Bridge

A Telegram bot that routes every message through a locally-installed **Oz CLI** agent. Responses are returned to the user in Telegram. Per-user conversation history persists across bot restarts.

---

## Architecture

```
Telegram ──► bot.py ──► oz agent run --prompt "…" ──► reply
                │
                └── data/{user_id}.json   (persists across restarts)
```

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.10+ | `python3 --version` |
| Oz CLI | Installed at `/home/seoadmin/.local/bin/oz` |
| Telegram bot token | From [@BotFather](https://t.me/BotFather) |
| Ubuntu / WSL | systemd user services supported |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/maximoseo/telegram-ai-bot.git
cd telegram-ai-bot
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy and edit the `.env` file:

```bash
cp .env.example .env   # or create from scratch
```

`.env` contents:

```env
TELEGRAM_TOKEN=<your BotFather token>
OZ_COMMAND=/home/seoadmin/.local/bin/oz
OZ_WORKDIR=/home/seoadmin
OZ_TIMEOUT_SECONDS=180
```

| Variable | Description |
|---|---|
| `TELEGRAM_TOKEN` | Token from @BotFather |
| `OZ_COMMAND` | Full path to the `oz` binary |
| `OZ_WORKDIR` | Working directory for Oz file operations |
| `OZ_TIMEOUT_SECONDS` | Max seconds to wait for an Oz response (default: 180) |

### 4. Install and authenticate Oz CLI

```bash
# Download and install
curl -L https://releases.warp.dev/oz/latest/oz-linux-amd64.tar.gz | tar xz
mv oz ~/.local/bin/oz
chmod +x ~/.local/bin/oz

# Authenticate
oz login
```

---

## Running the bot

### Option A — systemd user service (recommended, auto-starts on boot)

```bash
# Install service
mkdir -p ~/.config/systemd/user
cp telegram-ai-bot.service ~/.config/systemd/user/

# Enable and start
systemctl --user daemon-reload
systemctl --user enable telegram-ai-bot
systemctl --user start telegram-ai-bot

# Enable linger (start at boot without login)
loginctl enable-linger $USER
```

### Option B — Run directly

```bash
python3 bot.py
```

---

## Service management

```bash
# Status
systemctl --user status telegram-ai-bot

# Live logs
journalctl --user -u telegram-ai-bot -f

# Restart (e.g. after config change)
systemctl --user restart telegram-ai-bot

# Stop
systemctl --user stop telegram-ai-bot

# Disable auto-start
systemctl --user disable telegram-ai-bot
```

---

## Bot commands

| Command | Description |
|---|---|
| `/start` | Show help message |
| `/clear` | Clear your conversation history |
| *(any text)* | Send a message to the Oz agent |

---

## Conversation memory

- History is stored per-user in `data/{telegram_user_id}.json`
- The last **10 messages** are kept (configurable via `MAX_HISTORY_MESSAGES` in `bot.py`)
- History **persists across bot restarts** and is loaded lazily on first message
- `/clear` deletes both the in-memory cache and the JSON file
- If a JSON file is corrupted, the bot falls back to an empty history gracefully
- If Oz returns an error, the user's message is rolled back from history

---

## File layout

```
telegram-ai-bot/
├── bot.py                  # Core bot logic
├── .env                    # Secrets (not committed)
├── .gitignore
├── requirements.txt
├── telegram-ai-bot.service # systemd unit file
├── test_persistence.py     # Test suite (15 checks)
└── data/                   # Runtime: per-user history (git-ignored)
```

---

## Running tests

```bash
python3 test_persistence.py
```

Expected output:

```
[1] Fresh user — no history file
  ✓  returns empty list
  ✓  no file on disk

[2] Save history → simulate restart → reload
  ✓  JSON file created on disk
  ...

15/15 checks passed
All tests passed ✓
```

---

## Deployment checklist

- [ ] `.env` created with valid `TELEGRAM_TOKEN`
- [ ] `oz login` completed (check with `oz whoami`)
- [ ] systemd service enabled and running
- [ ] `loginctl enable-linger` enabled for boot persistence
- [ ] Test suite passing (`python3 test_persistence.py`)

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Bot doesn't respond | Check `journalctl --user -u telegram-ai-bot -f` |
| `Oz CLI not installed` error | Verify `OZ_COMMAND` path and run `oz whoami` |
| `Conflict: terminated by other getUpdates` | Kill duplicate processes: `pkill -f "python3 bot.py"` |
| Oz times out | Increase `OZ_TIMEOUT_SECONDS` in `.env` |
| History not saved | Check write permissions on `data/` directory |

---

## License

MIT
