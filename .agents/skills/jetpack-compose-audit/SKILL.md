---
name: Jetpack Compose Audit
source: https://github.com/hamen/compose_skill
category: Coding
purpose: Evidence-based Android Jetpack Compose audit scoring 4 categories (Performance, State, Side Effects, API Quality) with compiler-generated measurements and cited deductions
when_to_use: When auditing Android Compose codebases for performance, stability, state management, and API quality
tags: [android, jetpack-compose, audit, performance, kotlin, stability, recomposition]
---

# Jetpack Compose Audit

## Purpose
Strict, evidence-based Compose audit. Scores 4 categories 0-10, produces COMPOSE-AUDIT-REPORT.md with file:line citations and official-doc URLs. Generates Compose Compiler reports automatically.

## When To Use
- Before shipping a Compose-heavy feature
- When recomposition rates are too high
- When performance complaints are reported
- After major refactoring of Compose code
- `/jetpack-compose-audit [repo path or module path]`

## How To Apply
**4 scored categories:**
1. **Performance (35%)**: Expensive work in composition, lazy keys, lambda modifiers, stability, Strong Skipping, backwards writes
2. **State Management (25%)**: Hoisting, single source of truth, rememberSaveable, lifecycle-aware collection, observable collections
3. **Side Effects (20%)**: Correct effect API, keys, stale captures, cleanup, composition-time work
4. **Composable API Quality (20%)**: Modifier conventions, parameter order, slot APIs, CompositionLocal usage, Modifier.Node

**Bands:** 0-3 fail · 4-6 needs work · 7-8 solid · 9-10 excellent

**Key differentiator:** Generated Compose Compiler reports via injected Gradle init script — measured `skippable%` not inferred. Performance score capped by actual measurements.

**Top fixes format:** file:line + official-doc URL + predicted impact ("skippable% 69% → 85%")

## Examples
- Module audit reveals 69% skippable% → caps Performance at 4 → fixes identified: 3 unstable params + wrong collectAsState
- "Audit :app module for Compose quality" → generates COMPOSE-AUDIT-REPORT.md with all 4 category scores

## Integration Notes
- Requires Kotlin 2.0.20+ / Compose Compiler 1.5.4+ (Strong Skipping default)
- Symlink: `ln -s "$(pwd)" ~/.claude/skills/jetpack-compose-audit`
- Out of scope: Material 3 compliance, accessibility scoring, test coverage, Compose Multiplatform
- Fallback: source-inferred findings if Gradle build fails (explicitly flagged)
