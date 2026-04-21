# SKILL: Obsidian Headless Sync Docker
**Source:** https://github.com/Belphemur/obsidian-headless-sync-docker
**Domain:** productivity
**Trigger:** Use when setting up headless/automated Obsidian vault synchronization via Docker, or when running Obsidian Sync without a desktop environment.

## Summary
Minimal rootless Docker image that continuously syncs an Obsidian vault via the official `obsidian-headless` client. Uses s6-overlay for process supervision, supports bidirectional/pull-only/mirror sync modes, and runs as non-root.

## Key Patterns
- Get auth token once: `docker run --rm -it --entrypoint get-token ghcr.io/belphemur/obsidian-headless-sync-docker:latest`
- Configure via env vars: `OBSIDIAN_AUTH_TOKEN`, `VAULT_NAME`, `VAULT_HOST_PATH`
- Start with `docker compose up -d`
- Supports PUID/PGID for file ownership matching host user
- Sync modes: `bidirectional` (default), `pull-only`, `mirror-remote`

## Usage
When a user needs continuous Obsidian vault sync on a server/NAS without running a desktop. Requires active Obsidian Sync subscription.

## Code/Template
```yaml
# .env
OBSIDIAN_AUTH_TOKEN=<token>
VAULT_NAME=My Vault
VAULT_HOST_PATH=./vault
PUID=1000
PGID=1000
SYNC_MODE=bidirectional
```
