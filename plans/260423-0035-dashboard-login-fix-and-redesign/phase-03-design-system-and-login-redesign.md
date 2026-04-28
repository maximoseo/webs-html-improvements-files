# Phase 03 — Design System + Login Redesign

## Overview
- **Priority:** P0
- **Status:** pending
- Build design tokens. Redesign login. Cascade tokens into nav + shell in phase 04.

## Design tokens
See master report §4. Ship as `styles/tokens.css` (loaded first, before any other CSS).

## Login redesign — acceptance
- **Layout:** two-column ≥900px, single column below. Left = hero, right = form card.
- **Form card:** `max-width: 420px`, `padding: var(--s-10)`, `background: var(--bg-1)`, `border-radius: var(--r-lg)`, `box-shadow: var(--shadow-lg)`.
- **Title:** "Welcome back" (`--fs-2xl`, weight 600). Subtitle in `--fg-2` at `--fs-sm`.
- **Field pattern:** label above input, `--s-2` gap. Input 44px min-height. Focus ring 2px `--accent`.
- **CTA button:** full-width, 44px, 600 weight, `--accent` bg, `--fg-1` text, hover `--accent-hover`, loading spinner prepended.
- **Error panel:** above form, `--danger` border + soft tint, `--s-3` padding, dismissible.
- **Success panel:** similar but `--success`.
- **Reveal "Forgot password"** → inline email input + submit, no modal.
- **Divider + Google button** (phase 3.2, after OAuth enabled in Supabase).
- **Footer line:** "Having trouble? Contact service@maximo-seo.com" with mailto.
- **A11y:** labels `for` connected to inputs; errors announced via `aria-live="polite"`; `prefers-reduced-motion` disables animations; focus-visible outlines.

## Related files
- **New:** `webs-html-improvements-files-clean/static/tokens.css`
- **New:** `webs-html-improvements-files-clean/static/login.css`
- **Modify:** `webs-html-improvements-files-clean/login-page.html` — extract styles to `login.css`, load tokens.

## Implementation steps
1. Create `/static/tokens.css` with the full token set from §4.
2. Create `/static/login.css` scoped to `.auth-page *`.
3. Rewrite `login-page.html` using BEM-ish classes: `.auth-page`, `.auth-hero`, `.auth-card`, `.auth-form`, `.auth-field`, `.auth-cta`, `.auth-error`.
4. Replace single POST fetch as per master report §2 Layer B.
5. Add loading spinner SVG inline.
6. Verify Lighthouse a11y ≥ 95, perf ≥ 90.

## Todo
- [ ] Token CSS.
- [ ] Login CSS.
- [ ] New login HTML with single-endpoint flow.
- [ ] `requestAnimationFrame` redirect.
- [ ] A11y audit (axe).
- [ ] Responsive smoke: 360 / 414 / 768 / 1024 / 1440 / 1920.

## Success criteria
- Login is faster to submit (1 fetch instead of 2).
- No race; cookie set before redirect.
- V7 + V8 pass.

## Design guardrails
- No gradients over text.
- No shadows >20px blur on cards (keep premium, not Vegas).
- No more than 3 font weights in use: 400 / 500 / 600.
- Max 2 accent uses per screen (button + active chip).
