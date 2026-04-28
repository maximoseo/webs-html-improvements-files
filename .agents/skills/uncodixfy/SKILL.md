# SKILL: Uncodixfy
**Source:** https://github.com/cyxzdev/Uncodixfy
**Domain:** code
**Trigger:** When generating HTML, CSS, React, Vue, Svelte, or any frontend UI code — prevents generic AI UI patterns and enforces clean human-designed aesthetics

## Summary
A rule set that forces AI to stop relying on default UI habits (floating cards, gradients, oversized rounded corners, glass panels) and build interfaces that feel like Linear, Raycast, Stripe, or GitHub instead.

## Key Patterns
- Sidebars: 240-260px fixed width, solid background, simple border-right — no floating shells
- Buttons: solid fills or simple borders, 8-10px radius max — no pill shapes, no gradients
- Cards: 8-12px radius max, subtle borders, shadow ≤ 8px blur — no floating effect
- Typography: system fonts or simple sans-serif, 14-16px body, no mixed serif/sans combos
- Shadows: max `0 2px 8px rgba(0,0,0,0.1)` — no dramatic or colored shadows
- Transitions: 100-200ms ease — no bouncy animations, no transform effects
- Spacing: consistent 4/8/12/16/24/32px scale
- NO: glassmorphism, gradient backgrounds, pill overload, hero sections inside dashboards
- NO: decorative labels, fake charts, oversized rounded corners, metric-card grid as default
- NO: Segoe UI, Trebuchet MS, Arial (unless product already uses them)

## Usage
Include `uncodixify.md` in system instructions when generating UI. Install via `npx skills add cyxzdev/Uncodixfy` and invoke with `/uncodixfy`.

## Code/Template
```
Banned patterns (AI defaults to avoid):
- Gradient backgrounds on buttons/cards
- border-radius > 12px on cards, > 10px on buttons
- box-shadow > 8px blur
- backdrop-filter: blur() (glassmorphism)
- transform: scale/translateY on hover
- transition-duration > 200ms

Normal implementations:
- sidebar: width: 248px; background: #fff; border-right: 1px solid #e5e7eb
- button: padding: 8px 16px; border-radius: 8px; background: #2563eb; color: #fff
- card: border-radius: 8px; border: 1px solid #e5e7eb; padding: 16px
```
