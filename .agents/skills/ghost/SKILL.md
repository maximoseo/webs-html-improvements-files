# SKILL: Ghost — Intent-Based AI Commits
**Source:** https://github.com/adamveld12/ghost
**Domain:** developer-tools
**Trigger:** Use when committing AI-generated code by capturing prompts as commit messages, building reproducible intent-based git history, or using claude/gemini/codex/opencode per-commit.

## Summary
Ghost flips the git workflow: you commit prompts (intent), and AI generates the code. Commit messages capture what you asked for; diffs show what the agent decided. Supports claude, gemini, codex, opencode. Git log becomes a design document.

## Key Patterns
- `ghost commit -m "prompt"` → AI generates code → auto-stages → git commit
- `ghost log` — pretty-prints prompt + agent + model + session + files
- `ghost commit --agent gemini -m "refactor DB layer"`
- `ghost commit --dry-run -m "..."` — preview without committing
- `GHOST_SKIP=1 ghost commit -m "..."` — bypass ghost entirely
- Commit message includes: prompt + agent + model + session ID + changed files

## Usage
When user wants their git history to document design intent, not just code changes. Especially useful for AI-heavy development where prompts are the true source of truth.

## Code/Template
```bash
ghost init
ghost commit -m "add user auth with JWT"
ghost commit --agent gemini -m "refactor the database layer to use connection pooling"
ghost commit --agent codex -m "fix the race condition in payment queue"
ghost log
```
