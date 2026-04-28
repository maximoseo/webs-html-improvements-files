# Agent Change Log

This file records cross-agent notifications after merges that affect other Hermes agents.

## [2026-04-28] Multi-agent collaboration protocol added

- Added dashboard-specific multi-agent guide: `docs/hermes-multi-agent-git-collaboration.md`
- Added ownership helper: `scripts/check-agent-ownership.sh`
- Added directories for future change requests and locks:
  - `.github/change-requests/`
  - `.github/locks/`
- Important adaptation: this dashboard uses monolithic `index.html`; do not apply generic React `/src/components` ownership rules blindly.
