---
version: alpha
name: Prompt Studio Professional Popup
description: Professional, intuitive, mobile-first modal for building and running Hermes n8n template redesign prompts.
colors:
  primary: "#1A1A2E"
  background: "#F5F5F5"
  surface: "#FFFFFF"
  surfaceMuted: "#F8F9FA"
  border: "#E9ECEF"
  text: "#1A1A2E"
  muted: "#6C757D"
  success: "#06D6A0"
  warning: "#FFD166"
typography:
  h1:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 1.25rem
    fontWeight: 700
    lineHeight: 1.25
  h2:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 1rem
    fontWeight: 700
    lineHeight: 1.35
  body-md:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  body-sm:
    fontFamily: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
    fontSize: 0.875rem
    fontWeight: 500
    lineHeight: 1.45
rounded:
  sm: 8px
  md: 12px
  lg: 16px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px
  button-primary-accent:
    backgroundColor: "#FFE8ED"
    textColor: "#8F1730"
    rounded: "{rounded.sm}"
    padding: 12px
  button-secondary:
    backgroundColor: "{colors.surfaceMuted}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: 12px
  modal-surface:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: 24px
  modal-backdrop:
    backgroundColor: "{colors.background}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: 24px
  status-success:
    backgroundColor: "{colors.success}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-warning:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.primary}"
    rounded: "{rounded.sm}"
    padding: 8px
  status-danger:
    backgroundColor: "#FFE8ED"
    textColor: "#8F1730"
    rounded: "{rounded.sm}"
    padding: 8px
  helper-chip:
    backgroundColor: "{colors.border}"
    textColor: "{colors.text}"
    rounded: "{rounded.sm}"
    padding: 8px
  helper-chip-muted:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.muted}"
    rounded: "{rounded.sm}"
    padding: 8px
  accent-outline:
    backgroundColor: "#FFE8ED"
    textColor: "#8F1730"
    rounded: "{rounded.sm}"
    padding: 8px
  danger-outline:
    backgroundColor: "#FFE8ED"
    textColor: "#8F1730"
    rounded: "{rounded.sm}"
    padding: 8px
---

## Overview

Prompt Studio is the professional command center for the n8n HTML template redesign pipeline. It must feel like a reliable internal production tool, not a prototype. The interface emphasizes clarity, safe approvals, model/provider visibility, and a one-click path from structured inputs to a Hermes 5-agent pipeline prompt.

## Colors

- **Primary (#1A1A2E):** deep editorial navy for headings and text.
- **Accent (#E94560):** active tabs, outlines, badges, and accent surfaces. For filled buttons, use primary navy or pair pale accent backgrounds with #8F1730 text because white-on-accent is below WCAG AA.
- **Surface (#FFFFFF):** modal body and form cards.
- **Surface Muted (#F8F9FA):** secondary buttons, subtle panels, input backgrounds.
- **Success/Warning/Danger:** provider readiness status dots and pipeline state.

Contrast targets: all text must meet WCAG AA. Status color cannot be the only signal; pair dots with labels such as Connected, Needs Verification, Not Configured.

## Typography

Use system UI stack only. Keep labels concise, with strong hierarchy between popup title, tab sections, form labels, and helper text.

## Layout

Desktop modal: 900px wide, max-width 95vw, max-height 85vh, scrollable content, sticky header/tabs/footer. Mobile modal: full-screen, no rounded corners, horizontally scrollable tabs, stacked actions.

## Elevation & Depth

Use one strong modal shadow: `0 25px 60px rgba(0,0,0,0.15)`. Avoid nested heavy shadows. Use borders and spacing for internal hierarchy.

## Shapes

16px modal radius on desktop, 8-12px controls/cards, circular status dots.

## Components

- Tabs must use semantic `role="tablist"`, `role="tab"`, `aria-selected`, and keyboard support.
- Pipeline progress must use `role="progressbar"` and live status text.
- Provider status must have visible text labels.
- Prompt preview textarea must be large, editable, and copyable.
- Destructive actions like pipeline cancel need secondary styling unless confirmed.

## Do's and Don'ts

Do:
- Keep default output target as local + Obsidian only.
- Show provider limitations before run.
- Use plain labels instead of excessive emoji/icon clutter.
- Preserve manual approval gates for GitHub/dashboard/n8n.

Don't:
- Store API keys in the front-end.
- Auto-push to GitHub or update n8n without approval.
- Hide unavailable providers.
- Depend on color alone for status.
