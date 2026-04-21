---
name: Jetpack Compose Audit
source: https://github.com/hamen/compose_skill
category: Coding
purpose: Strict, evidence-based audit of Android Jetpack Compose repos — scores Performance/State/Side-effects/API quality, generates compiler reports
when_to_use: When reviewing Android Compose code for performance issues, stability problems, or skippability percentages
tags: [android, jetpack-compose, performance, audit, kotlin, stability]
---
# Jetpack Compose Audit

## Purpose
Scores Compose repos on 4 categories (0-10), generates compiler reports automatically, and produces a cited Markdown audit report.

## When To Use
- Performance review of a Compose codebase
- Checking recomposition/skippability rates
- Pre-production quality gate for Android UI code
- Audit before adding new Compose screens

## Categories Scored
| Category | Weight | Focus |
|---|---|---|
| Performance | 35% | Expensive work in composition, lazy keys, lambda modifiers, stability, backwards writes |
| State Management | 25% | Hoisting, single source of truth, `rememberSaveable`, lifecycle-aware collection |
| Side Effects | 20% | Correct effect API, keys, stale captures, cleanup |
| API Quality | 20% | Modifier conventions, parameter order, slot APIs, `CompositionLocal` usage |

Bands: `0-3` fail · `4-6` needs work · `7-8` solid · `9-10` excellent

## How To Apply
```
/jetpack-compose-audit [repo path]
# or natural language:
"Audit this Compose repo"
"Score the :app module for Compose quality"
```

Generates real Compose Compiler reports via bundled Gradle init script — no edits to target's `build.gradle`.

## Integration Notes
- Install: `ln -s "$(pwd)" ~/.claude/skills/jetpack-compose-audit`
- Performance score is capped by measured `skippable%` — 69% skippability caps Performance at 4
- Every deduction cites `developer.android.com` URL
- Pairs with `material-3-skill` for complete Android UI quality review
