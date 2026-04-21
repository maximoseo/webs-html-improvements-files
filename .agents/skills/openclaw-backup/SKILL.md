# SKILL: OpenClaw Backup — One-Click Backup & Restore
**Source:** https://github.com/LeoYeAI/openclaw-backup
**Domain:** code
**Trigger:** When you need to backup or migrate an OpenClaw/MyClaw agent instance including credentials and sessions

## Summary
Backs up workspace, memory, skills, credentials, bot tokens, API keys, and session history into a single archive. Restore to any new OpenClaw instance with zero re-pairing.

## Key Patterns
- Backs up: MEMORY.md, skills, openclaw.json (tokens/keys), channel pairing state, sessions, cron jobs, scripts
- Browser UI for download/upload/restore (requires --token, server refuses without it)
- --dry-run before any restore
- Archives are chmod 600 automatically

## Usage
Use before migrating servers or as regular backup. Restore preserves all channel connections.

## Code/Template
```bash
clawhub install myclaw-backup
# Or: tell OpenClaw "Help me install backup"

bash scripts/backup.sh /path/to/backups
bash scripts/restore.sh backup_TIMESTAMP.tar.gz --dry-run
bash scripts/restore.sh backup_TIMESTAMP.tar.gz

# Browser UI for download/upload:
bash scripts/serve.sh start --token $(openssl rand -hex 16) --port 7373
# http://localhost:7373/?token=YOUR_TOKEN
```
