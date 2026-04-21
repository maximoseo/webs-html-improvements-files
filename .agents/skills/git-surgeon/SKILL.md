# SKILL: git-surgeon — AI Agent Git Hunk Control
**Source:** https://github.com/raine/git-surgeon
**Domain:** developer-tools
**Trigger:** Use when an AI agent needs to stage/unstage/commit individual git hunks without interactive prompts, split commits by concern, fold fixes into earlier commits, or commit to a branch without checking it out.

## Summary
git-surgeon gives AI agents surgical, non-interactive git control: stage/commit individual hunks by ID, split commits mixing concerns, fold fixups, reword/reorder history, and undo hunks from previous commits. Prevents agents from destructively resetting files when asked to commit separately.

## Key Patterns
- `git-surgeon hunks` — list all hunks with IDs
- `git-surgeon commit <id1> <id2> -m "message"` — stage + commit selected hunks
- `git-surgeon split <commit-sha>` — split a commit into focused pieces
- `git-surgeon fixup <fix-sha> <target-sha>` — fold fix into earlier commit
- `git-surgeon stage/unstage/discard <id>` — granular hunk management
- `git-surgeon commit-to <branch> <ids> -m "msg"` — commit to another branch without checkout
- Install skill: `git-surgeon install-skill --claude`

## Usage
Install as a Claude Code skill, then ask Claude to make granular commits. Claude will use git-surgeon automatically instead of destructive `git checkout` workarounds.

## Code/Template
```bash
cargo install git-surgeon
git-surgeon install-skill --claude  # or --opencode, --codex

git-surgeon hunks
git-surgeon commit ac34353 15baf94 -m "allow edit commands during attribute input"
git-surgeon split HEAD~3
git-surgeon fixup <fix-sha> <target-sha>
```
