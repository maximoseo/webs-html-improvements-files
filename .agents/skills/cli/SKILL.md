# SKILL: Google Workspace CLI (gws)
**Source:** https://github.com/googleworkspace/cli
**Domain:** code
**Trigger:** When automating Google Workspace (Drive, Gmail, Calendar, Sheets, Chat) from CLI or AI agents

## Summary
A CLI (`gws`) that covers all Google Workspace APIs — Drive, Gmail, Calendar, Sheets, Chat, and more. Dynamically built from Google's Discovery Service, so it picks up new API endpoints automatically. 40+ agent skills included. Structured JSON output for AI agents.

## Key Patterns
- Dynamic command surface from Google Discovery API — no stale docs
- `gws drive files list --params '{"pageSize": 10}'` — list Drive files
- `gws sheets spreadsheets create --json '{"properties": {"title": "Q1"}}'` — create spreadsheet
- `--dry-run` preview mode; `--page-all` for auto-pagination as NDJSON
- `gws schema <method>` — introspect request/response schema
- 40+ agent skills for common Workspace workflows
- Auth: `gws auth setup` (requires gcloud) or manual OAuth setup
- `GOOGLE_WORKSPACE_CLI_TOKEN` env var for pre-obtained access tokens
- Credentials encrypted at rest (AES-256-GCM) in OS keyring
- Service account support via `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE`

## Usage
Install via npm: `npm install -g @googleworkspace/cli` or download binary from GitHub Releases. Run `gws auth setup` for first-time OAuth. Then use any `gws <service> <resource> <method>` command.

## Code/Template
```bash
# Auth setup
gws auth setup        # one-time (needs gcloud)
gws auth login -s drive,gmail,sheets   # scope selection

# Common operations
gws drive files list --params '{"pageSize": 10}'
gws sheets spreadsheets create --json '{"properties": {"title": "Budget"}}'
gws gmail users messages list --params '{"userId": "me", "maxResults": 5}'

# Introspect schema
gws schema drive.files.list

# Paginate all results
gws drive files list --params '{"pageSize": 100}' --page-all | jq -r '.files[].name'
```
