# SKILL: Skill Lab — Agent Skills Evaluation Framework
**Source:** https://github.com/8ddieHu0314/Skill-Lab
**Domain:** agent-tools
**Trigger:** Use when evaluating, testing, or auditing AI agent skills for quality, security, token efficiency, and trigger reliability. Run before deploying skills to production.

## Summary
Skill Lab is a Python CLI (`sklab`) that evaluates agent skills across 37 checks in 5 dimensions: structure, naming, description, content, and security. Scores 0–100, catches token waste, security issues, and skills that never fire.

## Key Patterns
- `sklab evaluate ./my-skill` — full static + LLM quality review with 0-100 score
- `sklab scan ./my-skill` — security scan (prompt injection, jailbreak, Unicode obfuscation)
- `sklab trigger ./my-skill` — auto-generates ~13 trigger test cases via LLM
- `sklab check ./my-skill` — CI-friendly pass/fail (exit 0 or 1)
- `sklab info ./my-skill` — token cost estimates for discovery vs activation
- Use `--all` or `--repo` flags to evaluate every skill in scope

## Usage
Run `sklab evaluate` before publishing any skill. Use `sklab check` in CI pipelines. Use `sklab scan` for security-sensitive skills. Use `sklab trigger` to verify description triggers the skill reliably.

## Code/Template
```bash
pip install skill-lab

# Evaluate a skill
sklab evaluate ./my-skill --verbose

# Security scan
sklab scan ./my-skill

# Trigger testing (needs ANTHROPIC_API_KEY)
sklab generate ./my-skill
sklab trigger ./my-skill

# CI gate
sklab check ./my-skill  # exits 0=pass, 1=fail

# Batch evaluate all skills
sklab evaluate --repo
```
