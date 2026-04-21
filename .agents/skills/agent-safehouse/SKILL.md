# SKILL: Agent Safehouse
**Source:** https://github.com/eugene1g/agent-safehouse
**Domain:** code
**Trigger:** When sandboxing LLM coding agents on macOS to limit filesystem and network access using least-privilege policies

## Summary
Sandboxes AI coding agents on macOS using `sandbox-exec` with composable policy profiles and a deny-first model. Prevents agents from accessing files/integrations they don't need while keeping normal development practical.

## Key Patterns
- Deny-first model: start from deny-all, allow only what agent needs
- Composable profiles: combine built-in + custom + appended profiles
- `HOME_DIR` grants metadata-only traversal, not recursive read
- `--add-dirs-ro` for read-only shared folders; `--add-dirs` for read-write
- `--append-profile` for machine-local policy exceptions (loads last, can deny earlier rules)
- Git worktrees auto-detected at launch for cross-tree inspection
- Built-in path resolution: symlinks in `/etc` auto-resolved to `/private/etc`
- Shell wrappers: `safe-claude()`, `safe-codex()` functions for daily use
- `SAFEHOUSE_APPEND_PROFILE` env var for persistent machine-local overrides
- Policy Builder UI at agent-safehouse.dev/policy-builder

## Usage
Install: `brew install eugene1g/safehouse/agent-safehouse`. Wrap agent invocations: `safehouse claude --dangerously-skip-permissions`. Create shell aliases for daily use.

## Code/Template
```bash
# Install
brew install eugene1g/safehouse/agent-safehouse

# Basic usage
safehouse claude --dangerously-skip-permissions

# Shell wrapper (zsh/bash)
safe-claude() { safehouse --add-dirs-ro="$HOME/projects" claude --dangerously-skip-permissions "$@" }

# Machine-local overrides (~/.config/agent-safehouse/local-overrides.sb)
(allow file-read*
  (home-subpath "/Library/Application Support/CleanShot/media")
  (subpath "/Volumes/Shared/Engineering")
)
```
