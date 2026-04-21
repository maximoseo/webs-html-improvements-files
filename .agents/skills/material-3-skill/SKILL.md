---
name: Material Design 3 (MD3 / Material You)
source: https://github.com/hamen/material-3-skill
category: Design Systems
purpose: Implement Google Material Design 3 UI — components, theming, dynamic color, Expressive, compliance audit — primary focus: Jetpack Compose
when_to_use: When building Android (Compose), Flutter, or web UI that must follow Material Design 3 standards
tags: [material-design, android, jetpack-compose, flutter, theming, dark-mode, accessibility]
---
# Material Design 3 Skill

## Purpose
Guides Claude in generating MD3-compliant UI with correct design tokens, components, theming, layout, and accessibility.

## Platform Support
| Platform | Role | Notes |
|---|---|---|
| Jetpack Compose | **Primary** | Best match for MD3, Expressive motion, adaptive navigation |
| Flutter | Secondary | `ThemeData(useMaterial3: true)`, `ColorScheme.fromSeed` |
| Web | Limited | `@material/web` in maintenance mode; no Expressive parity |

## Capabilities
- 30+ components with Compose-oriented mappings
- Color roles, tonal palettes, dynamic color (ColorScheme.fromSeed)
- Typography scale, shape system, elevation, motion
- M3 Expressive (May 2025) with per-platform matrix
- Navigation patterns, adaptive layouts, edge-to-edge/insets
- MD3 compliance audit across 10 categories (0-10 per category)

## How To Apply
```
/material-3 component Create a login form with email and password fields
/material-3 theme Generate a theme from seed color #1A73E8
/material-3 scaffold Create a responsive app shell with navigation
/material-3 audit [URL or file path]
```

## Integration Notes
- Install: `cp -r material-3-skill ~/.claude/skills/material-3`
- Audit works for Compose/Kotlin, Flutter/Dart, and web/CSS
- References: m3.material.io, developer.android.com, @material/web
- Pairs with `compose-audit-skill` for full Android UI quality review
