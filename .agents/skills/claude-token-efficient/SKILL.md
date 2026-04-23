# SKILL: Claude Token Efficient
**Source:** https://github.com/drona23/claude-token-efficient
**Domain:** code
**Trigger:** When reducing Claude output verbosity in high-volume automation pipelines or agent loops to cut token costs

## Summary
A minimal CLAUDE.md configuration that eliminates Claude's default filler patterns (affirmations, restatements, unsolicited suggestions) and reduces output tokens by ~63% on output-heavy workflows. Best for automation pipelines with >100 prompts/day.

## Key Patterns
- Drop-and-forget: place `CLAUDE.md` in project root, zero code changes
- Eliminates: "Sure!", "Great question!", restatements, unsolicited suggestions, over-engineered abstractions
- Reduces output ~63% without signal loss (benchmarked on 5-prompt directional test)
- 17.4% cost reduction vs best-known alternative in external benchmark
- Trade-off: file adds input tokens every message — only net-positive at high output volume
- Not suitable for: exploratory/architectural work, single short queries, fresh multi-session pipelines
- For guaranteed structure use JSON mode / tool schemas — not prompt rules

## Usage
Copy CLAUDE.md to your project root. Effective immediately for all Claude Code sessions in that directory. For one-off: paste `Rules: Read files first. Write complete solution. Test once. No over-engineering.` into chat.

## Code/Template
```markdown
# CLAUDE.md core rules (7 lines)
- No affirmations ("Sure!", "Great!", "Absolutely!")
- No restatements of the question
- No unsolicited suggestions beyond what was asked
- No over-engineered abstractions
- Write complete solutions, not partial scaffolds
- Test once, not repeatedly
- Correct errors directly, don't apologize first
```
