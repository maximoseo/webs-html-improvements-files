# SKILL: yoyo-evolve - Self-Evolving Coding Agent in Rust
**Source:** https://github.com/yologdev/yoyo-evolve
**Domain:** code
**Trigger:** When building self-improving AI coding agents, implementing autonomous evolution loops via GitHub Actions, or studying agent self-modification patterns

## Summary
Rust-based coding agent (200 initial lines, now 42,000+ after 37 days of self-evolution) that reads its own source, plans improvements, implements them, runs tests, commits if passing, and reverts if failing. Runs every ~8 hours via GitHub Actions with social memory synthesis.

## Key Patterns
- Evolution loop: read source → check GitHub issues → plan → edit → test → commit/revert
- Social sessions: reads/replies to GitHub Discussions, learns from community
- Active memory: JSONL archives with time-weighted compression (recent=full, old=themed)
- Community input via agent-input label on GitHub Issues (votes = priority)
- 60+ slash commands in the REPL: multi-file edits, git management, codebase navigation
- Available as `cargo install yoyo-agent` (crates.io)

## Usage
```bash
cargo install yoyo-agent
# Or run locally from source
# Contribute: open GitHub Issue with agent-input label, thumbs-up to prioritize
```

## Code/Template
```yaml
# GitHub Actions workflow pattern (evolve.yml)
# Every 8 hours: checkout → read source → check issues → plan/edit → test → commit/revert
# Every 4 hours (offset): social session (read/reply discussions)
# Daily: memory synthesis (JSONL → time-weighted compression → active_learnings.md)
```
