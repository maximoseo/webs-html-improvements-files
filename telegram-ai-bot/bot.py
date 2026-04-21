import asyncio
import json
import logging
import os
import shutil

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OZ_COMMAND = os.getenv("OZ_COMMAND", "oz")
OZ_WORKDIR = os.getenv("OZ_WORKDIR", "/home/seoadmin")
OZ_TIMEOUT_SECONDS = int(os.getenv("OZ_TIMEOUT_SECONDS", "180"))
SYSTEM_PROMPT = (
    "You are Oz running through a Telegram bridge. "
    "Be concise and helpful."
)
MAX_HISTORY_MESSAGES = 10

# Directory where per-user history JSON files are stored
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# In-memory cache; populated lazily from disk on first access
_history_cache: dict[int, list[dict[str, str]]] = {}


def _history_path(user_id: int) -> str:
    return os.path.join(DATA_DIR, f"{user_id}.json")


def _load_history(user_id: int) -> list[dict[str, str]]:
    """Load history from disk into cache and return it."""
    if user_id in _history_cache:
        return _history_cache[user_id]
    path = _history_path(user_id)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
            logger.info("Loaded %d history messages for user %d", len(history), user_id)
        except Exception as exc:
            logger.warning("Could not read history for user %d: %s", user_id, exc)
            history = []
    else:
        history = []
    _history_cache[user_id] = history
    return history


def _save_history(user_id: int, history: list[dict[str, str]]) -> None:
    """Persist the last MAX_HISTORY_MESSAGES entries to disk."""
    trimmed = history[-MAX_HISTORY_MESSAGES:]
    _history_cache[user_id] = trimmed
    path = _history_path(user_id)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(trimmed, f, ensure_ascii=False, indent=2)
    except Exception as exc:
        logger.warning("Could not save history for user %d: %s", user_id, exc)


def _clear_history(user_id: int) -> None:
    """Delete history from cache and disk."""
    _history_cache[user_id] = []
    path = _history_path(user_id)
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception as exc:
            logger.warning("Could not delete history file for user %d: %s", user_id, exc)


def _oz_available() -> bool:
    return shutil.which(OZ_COMMAND) is not None


def _build_prompt(history: list[dict[str, str]]) -> str:
    recent_history = history[-MAX_HISTORY_MESSAGES:]
    lines = [SYSTEM_PROMPT, "", "Conversation so far:"]
    for item in recent_history:
        role = item["role"].capitalize()
        lines.append(f"{role}: {item['content']}")
    lines.append("")
    lines.append("Reply to the latest user message.")
    return "\n".join(lines)


async def _run_oz_agent(prompt: str) -> str:
    process = await asyncio.create_subprocess_exec(
        OZ_COMMAND,
        "agent",
        "run",
        "--prompt",
        prompt,
        cwd=OZ_WORKDIR,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        stdout, stderr = await asyncio.wait_for(
            process.communicate(),
            timeout=OZ_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError:
        process.kill()
        await process.communicate()
        raise RuntimeError("Oz agent timed out")

    if process.returncode != 0:
        error_output = stderr.decode().strip() or stdout.decode().strip() or "unknown error"
        raise RuntimeError(error_output)

    raw = stdout.decode().strip()
    # Remove Oz CLI startup lines (e.g. "New conversation started with debug ID: ...")
    lines = raw.splitlines()
    cleaned = [l for l in lines if not l.startswith("New conversation started with debug ID")]
    return "\n".join(cleaned).strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "👋 Hi! I'm an AI assistant bridged to a local Oz agent.\n\n"
        "Just send me any message and I'll reply.\n\n"
        "Commands:\n"
        "/start - Show this message\n"
        "/clear - Clear conversation history"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    _clear_history(user_id)
    await update.message.reply_text("🗑️ Conversation history cleared!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text
    if not _oz_available():
        await update.message.reply_text(
            "⚠️ The Oz CLI is not installed or not on PATH yet."
        )
        return

    history = _load_history(user_id)
    history.append({"role": "user", "content": user_message})

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        prompt = _build_prompt(history)
        assistant_message = await _run_oz_agent(prompt)

        history.append({"role": "assistant", "content": assistant_message})
        _save_history(user_id, history)

        await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error("Error calling Oz CLI: %s", e)
        # Roll back the user message we just appended so history stays clean
        if history and history[-1]["role"] == "user":
            history.pop()
            _save_history(user_id, history)
        if "timed out" in str(e).lower():
            await update.message.reply_text("⚠️ The Oz agent took too long to respond. Please try again.")
        else:
            await update.message.reply_text("⚠️ The Oz bridge failed. Check that `oz` is installed and authenticated.")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("Missing TELEGRAM_TOKEN in .env")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running... Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
