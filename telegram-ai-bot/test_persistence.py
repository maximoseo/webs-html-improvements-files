#!/usr/bin/env python3
"""
Tests for conversation history persistence.
Verifies that history survives bot restarts by directly exercising
the load/save/clear helpers in bot.py.
"""

import json
import os
import sys
import tempfile
import importlib

# ── helpers ────────────────────────────────────────────────────────────────

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
results = []


def check(label: str, condition: bool, detail: str = "") -> None:
    status = PASS if condition else FAIL
    print(f"  {status}  {label}" + (f"  ({detail})" if detail else ""))
    results.append((label, condition))


# ── setup: point DATA_DIR at a temp directory ──────────────────────────────

tmp_dir = tempfile.mkdtemp(prefix="bot_test_")

# Patch env so bot.py doesn't need real credentials
os.environ.setdefault("TELEGRAM_TOKEN", "test-token")
os.environ.setdefault("OZ_COMMAND", "oz")
os.environ.setdefault("OZ_WORKDIR", "/tmp")

# Import bot module and override DATA_DIR before any tests run
import bot
bot.DATA_DIR = tmp_dir
os.makedirs(tmp_dir, exist_ok=True)

TEST_USER = 999_999_999  # fake Telegram user ID


def reset_cache() -> None:
    """Simulate a bot restart by clearing the in-memory cache."""
    bot._history_cache.clear()


# ── Test 1: fresh user has no history ─────────────────────────────────────

print("\n[1] Fresh user — no history file")
reset_cache()
h = bot._load_history(TEST_USER)
check("returns empty list", h == [])
check("no file on disk", not os.path.exists(bot._history_path(TEST_USER)))


# ── Test 2: save and reload ────────────────────────────────────────────────

print("\n[2] Save history → simulate restart → reload")

messages = [
    {"role": "user",      "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user",      "content": "What is 2+2?"},
    {"role": "assistant", "content": "4"},
]

reset_cache()
bot._save_history(TEST_USER, messages)

# Verify file was written
path = bot._history_path(TEST_USER)
check("JSON file created on disk", os.path.exists(path))

with open(path) as f:
    on_disk = json.load(f)
check("file contains correct number of messages", len(on_disk) == len(messages),
      f"expected {len(messages)}, got {len(on_disk)}")
check("first message preserved",
      on_disk[0] == {"role": "user", "content": "Hello"})
check("last message preserved",
      on_disk[-1] == {"role": "assistant", "content": "4"})

# Simulate restart: wipe in-memory cache, then reload
reset_cache()
reloaded = bot._load_history(TEST_USER)
check("history reloaded after cache wipe", reloaded == messages,
      f"got {len(reloaded)} messages")


# ── Test 3: history trimmed to MAX_HISTORY_MESSAGES ────────────────────────

print(f"\n[3] History trimmed to MAX_HISTORY_MESSAGES={bot.MAX_HISTORY_MESSAGES}")

long_history = [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"msg {i}"}
    for i in range(bot.MAX_HISTORY_MESSAGES + 6)
]

reset_cache()
bot._save_history(TEST_USER, long_history)

reset_cache()
loaded = bot._load_history(TEST_USER)
check(
    f"trimmed to {bot.MAX_HISTORY_MESSAGES} messages",
    len(loaded) == bot.MAX_HISTORY_MESSAGES,
    f"got {len(loaded)}",
)
check(
    "keeps the LATEST messages (not oldest)",
    loaded[-1] == long_history[-1],
)


# ── Test 4: cache is used on second access (no extra disk read) ───────────

print("\n[4] In-memory cache hit on second access")

reset_cache()
bot._save_history(TEST_USER, messages)
reset_cache()

h1 = bot._load_history(TEST_USER)   # reads from disk
h2 = bot._load_history(TEST_USER)   # should hit cache (same object)
check("second load returns same list object (cache hit)", h1 is h2)


# ── Test 5: clear removes file and cache ──────────────────────────────────

print("\n[5] /clear — removes file and resets cache")

reset_cache()
bot._save_history(TEST_USER, messages)
check("file exists before clear", os.path.exists(bot._history_path(TEST_USER)))

bot._clear_history(TEST_USER)
check("file deleted after clear", not os.path.exists(bot._history_path(TEST_USER)))
check("cache entry empty after clear", bot._history_cache.get(TEST_USER) == [])

# Reload after clear should return empty
reset_cache()
h = bot._load_history(TEST_USER)
check("reload after clear returns empty list", h == [])


# ── Test 6: error on load returns empty list gracefully ───────────────────

print("\n[6] Corrupted history file → graceful fallback")

with open(bot._history_path(TEST_USER), "w") as f:
    f.write("{ this is not valid json }")

reset_cache()
h = bot._load_history(TEST_USER)
check("returns empty list on corrupt file", h == [])


# ── cleanup ───────────────────────────────────────────────────────────────

import shutil
shutil.rmtree(tmp_dir, ignore_errors=True)


# ── summary ───────────────────────────────────────────────────────────────

passed = sum(1 for _, ok in results if ok)
total  = len(results)
print(f"\n{'─'*40}")
print(f"  {passed}/{total} checks passed")
if passed == total:
    print("  \033[32mAll tests passed ✓\033[0m")
    sys.exit(0)
else:
    failed = [label for label, ok in results if not ok]
    print(f"  \033[31mFailed: {', '.join(failed)}\033[0m")
    sys.exit(1)
