---
name: AntiVibe (Code Learning / Deep Dive)
source: https://github.com/mohi-devhub/antivibe
category: Coding
purpose: Learning-focused code explanation framework — generates deep-dive guides explaining What, Why, When, and Alternatives for AI-generated code
when_to_use: When you want to actually understand code AI wrote, not just accept it; for learning, onboarding, or code comprehension
tags: [learning, education, code-explanation, anti-vibe, deep-dive, comprehension]
---
# AntiVibe — Anti-Vibecoding Learning Framework

## Purpose
Transforms AI-generated code into educational content. Unlike generic summaries, explains the reasoning behind design decisions.

## Trigger Phrases
```
/antivibe                        # Start a deep dive
"deep dive"                      # Analyze recently written code
"learn from this code"
"explain what AI wrote"
"understand what AI wrote"
```

## Output Example
```markdown
# Deep Dive: Authentication System

## Overview
This auth system uses JWT tokens with refresh token rotation...

## Concepts Explained
### JWT (JSON Web Tokens)
- What: Stateless authentication tokens...
- Why: Server doesn't need to store sessions...
- When: APIs, SPAs, microservices...

## Learning Resources
- JWT.io: Official documentation
- Auth0 Guide: Best practices
```

## Auto-Trigger Hooks
```bash
cp framework/hooks/hooks.json your-project/.claude/hooks.json
```
Hooks: `SubagentStop` (after task), `Stop` (end of session).

## Principles
1. Why over what — always explain design decisions
2. Context matters — when/why to use patterns
3. Curated resources — quality links only
4. Concept mapping — connect code to CS principles

## Integration Notes
- Install: `cp -r antivibe ~/.claude/skills/antivibe`
- Works with any language/framework
- Output saved to `deep-dive/` directory
