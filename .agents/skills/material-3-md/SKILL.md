---
name: Material Design 3 Skill
source: https://github.com/hamen/material-3-skill
category: Design Systems
purpose: Comprehensive MD3 implementation guide covering 30+ components, color system, typography, M3 Expressive, adaptive layouts — Jetpack Compose primary, Flutter secondary, Web limited
when_to_use: When implementing Google Material Design 3 UI in Compose/Flutter/Web, generating themes from seed colors, or auditing MD3 compliance
tags: [material-design, md3, jetpack-compose, flutter, theming, components, accessibility]
---

# Material Design 3 Skill

## Purpose
Guides AI in generating MD3-compliant UI with correct design tokens, components, theming, layout, and accessibility. Primary focus: Jetpack Compose with MaterialTheme and adaptive layouts.

## When To Use
- Building MD3 components in Jetpack Compose
- Generating a theme from a seed color
- Scaffolding a new MD3-compliant app shell
- Auditing existing UI for MD3 compliance
- Implementing M3 Expressive motion/shape

## How To Apply
**4 commands:**
```
/material-3 component Create a login form with email and password
/material-3 theme Generate a theme from seed color #1A73E8
/material-3 scaffold Create a responsive app shell with navigation
/material-3 audit [URL or file path]
```

**Platform hierarchy:**
1. Jetpack Compose (Primary): MaterialTheme, Material 3 composables, adaptive layouts, edge-to-edge
2. Flutter (Secondary): ThemeData(useMaterial3: true), ColorScheme.fromSeed
3. Web (Limited): @material/web in maintenance mode — M3 Expressive NOT available on Web

**8 reference files:** color-system, component-catalog, theming-and-dynamic-color, typography-and-shape, navigation-patterns, layout-and-responsive, CONTRIBUTING

**Audit scores 10 categories:** color tokens, typography, shape, elevation, components, layout, navigation, motion, accessibility, theming

## Examples
- `/material-3 theme Generate a theme from seed color #E91E63` → MaterialTheme setup with tonal palette
- `/material-3 audit ./app/src/main` → 10-category compliance report with specific fixes

## Integration Notes
- Install: `cp -r material-3-skill ~/.claude/skills/material-3`
- M3 Expressive (May 2025): motion, emphasized type, shape morphing — Compose only, not Web
- May drift as Google updates spec — verify API signatures against official Android docs
