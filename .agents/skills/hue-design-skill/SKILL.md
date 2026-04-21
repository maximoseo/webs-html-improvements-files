---
name: Hue (Brand Design System Generator)
source: https://github.com/dominikmartn/hue
category: Design Systems
purpose: Learn any brand from a URL, name, or screenshot and generate a complete design system — color tokens, typography, spacing, components, light/dark mode
when_to_use: When you need to build UI that matches a specific brand, or when creating a design language for a new product
tags: [design-system, brand, typography, color-tokens, ui, dark-mode]
---
# Hue (Brand Design System Generator)

## Purpose
Generates a complete design language as an AI coding skill from any brand source — URL, name, or screenshot.

## When To Use
- Build components matching an existing brand
- Create a consistent design language for a new product
- Generate light + dark mode variants from brand colors
- Extract hero stage recipes and icon kit selection

## How To Apply
```bash
# Install
git clone https://github.com/dominikmartn/hue ~/.claude/skills/hue

# Trigger in session
"make a design skill from cursor.com"
"create a design language inspired by raycast"
"generate a hue skill from this screenshot"
```

Output includes:
- `design-model.yaml` — complete design system spec
- `landing-page.html` — rendered example
- Color tokens (primary, secondary, accent, neutral scales)
- Typography scale (heading, body, caption, code)
- Spacing grid and border radius system
- Component patterns (cards, buttons, forms)
- Light + dark mode variants
- Hero stage recipes

## Examples (17 brands in repo)
atlas (maritime), auris (audio), drift (fashion), fizz (y2k), halcyon (glass), kiln (earth), ledger (editorial), meadow (warm cream), oxide (brutalist), prism (cyberpunk), ridge (slate dev), velvet (noir)

## Integration Notes
- Visit: hueapp.io for live demo
- Each generated skill is consistent across sessions — two sessions using same skill produce visually consistent output
- Pairs with `skillui` for full design extraction pipeline
