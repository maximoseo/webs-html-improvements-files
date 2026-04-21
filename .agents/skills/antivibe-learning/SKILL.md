---
name: AntiVibe Learning Framework
source: https://github.com/mohi-devhub/antivibe
category: Coding
purpose: Learning-focused code explanation framework that transforms AI-generated code into educational content — explaining WHAT, WHY, WHEN, and WHAT ALTERNATIVES exist
when_to_use: When you want to understand AI-written code, not just use it — generates deep-dive learning guides with concept mapping, resources, and phase-aware explanations
tags: [learning, anti-vibecoding, code-explanation, education, deep-dive]
---

# AntiVibe Learning Framework

## Purpose
Prevents vibecoding: AI writes code, developer copy-pastes, nobody learns. AntiVibe generates comprehensive learning guides from AI-generated code.

## When To Use
- "deep dive" / "learn from this code" / "explain what AI wrote" / "understand what AI wrote"
- After implementing a complex feature with AI assistance
- When you want to actually understand the patterns being used
- When onboarding to new frameworks or patterns
- As a post-session learning ritual

## How To Apply
**Install:**
```bash
cp -r antivibe ~/.claude/skills/antivibe
```

**Usage:**
```
/antivibe              # Start a deep dive
"deep dive"            # Analyze recently written code
"learn from this code" # Generate learning guide
```

**Output format (deep-dive/*.md):**
- Overview: what was built + architectural decisions
- Code Walkthrough: file-by-file purpose + key components
- Concepts Explained: What / Why / When / Alternatives for each pattern
- Learning Resources: curated docs, tutorials, videos (not random results)
- Dependency Analysis: what each dep does + alternatives

**5 principles:**
1. Why over What — always explain design decisions
2. Context matters — when/why to use these patterns
3. Curated resources — quality links, not random results
4. Phase-aware — group explanations by implementation phase
5. Concept mapping — connect code to underlying CS concepts

## Examples
- After building JWT auth system → deep-dive explains JWT vs sessions, bcrypt vs argon2, refresh token rotation
- After Prisma migration → deep-dive explains ORM patterns, migration strategies, schema design

## Integration Notes
- Auto-trigger hooks available: SubagentStop (phase-based), Stop (end-of-session summary)
- Multi-language: JS/TS, Python, Go, Rust, Java, extensible
- Output saved to deep-dive/ directory in project
