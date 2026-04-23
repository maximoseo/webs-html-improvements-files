# SKILL: codex-autoresearch
**Source:** https://github.com/leo-lilinxiao/codex-autoresearch
**Domain:** code
**Trigger:** When wanting to run autonomous iterative improvement loops on any codebase metric (test coverage, type errors, latency, lint) using Codex

## Summary
Inspired by Karpathy's autoresearch, this generalizes the autonomous experiment loop beyond ML to any mechanically verifiable goal. Codex infers metric, scope, and verify command from one sentence; loops modify→verify→keep/discard with escalating strategies when stuck.

## Key Patterns
- One sentence → Codex maps to 7 modes: loop, plan, debug, fix, security, ship, exec
- Codex auto-infers: goal, scope, metric, direction, verify command, guard
- Foreground or background execution (detached overnight runs)
- Escalation: 3 failures → REFINE, 5 → PIVOT, 2 PIVOTs → web search, 3 PIVOTs → stop
- Results log: `autoresearch-results/results.tsv` (iteration, commit, metric, delta, status)
- Dual-gate: separate verify (improved?) and guard (anything break?)
- Parallel experiments via git worktrees (up to 3 simultaneous)

## Usage
```bash
# Install via Codex skill
$skill-installer install https://github.com/leo-lilinxiao/codex-autoresearch
# Then in Codex:
# "$codex-autoresearch I want to eliminate all `any` types in my TypeScript"
```

## Code/Template
```
# Example prompts that trigger the loop
"Improve my test coverage"        → loops until target or interrupted
"Fix the 12 failing tests"        → repairs one by one
"Is this code secure?"            → STRIDE + OWASP audit
"Ship it"                         → verifies readiness, gates release
```
