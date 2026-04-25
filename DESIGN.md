---
version: alpha
name: HTML Redesign Dashboard
description: Dark operator dashboard for HTML redesign, workflow repair, and production oversight.
colors:
  primary: "#08090A"
  surface: "#131416"
  surfaceElevated: "#0F1011"
  border: "#C8CDD6"
  text: "#F7F8F8"
  textSecondary: "#D0D6E0"
  muted: "#8A8F98"
  accent: "#7170FF"
  accentStrong: "#5E6AD2"
  success: "#27A644"
  warning: "#EAB308"
  danger: "#F87171"
typography:
  h1:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.03em"
  h2:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.03em"
  body-md:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: Inter
    fontSize: 0.6875rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.08em"
rounded:
  sm: 10px
  md: 12px
  lg: 18px
spacing:
  xs: 4px
  sm: 8px
  md: 12px
  lg: 16px
  xl: 24px
components:
  app-shell:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
  card-muted:
    backgroundColor: "{colors.surfaceElevated}"
    textColor: "{colors.textSecondary}"
    rounded: "{rounded.md}"
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.primary}"
    rounded: "{rounded.md}"
    padding: 12px
  button-primary-hover:
    backgroundColor: "{colors.accentStrong}"
  button-secondary:
    backgroundColor: "rgba(255,255,255,0.03)"
    textColor: "{colors.textSecondary}"
    rounded: "{rounded.md}"
    padding: 10px
  status-success:
    backgroundColor: "rgba(39,166,68,0.16)"
    textColor: "{colors.success}"
    rounded: "{rounded.sm}"
  status-warning:
    backgroundColor: "rgba(234,179,8,0.16)"
    textColor: "{colors.warning}"
    rounded: "{rounded.sm}"
  status-danger:
    backgroundColor: "rgba(248,113,113,0.16)"
    textColor: "{colors.danger}"
    rounded: "{rounded.sm}"
  metadata-label:
    backgroundColor: "{colors.surfaceElevated}"
    textColor: "{colors.muted}"
    rounded: "{rounded.sm}"
---

## Overview

The dashboard should feel like a calm, high-signal operator console: dark, focused,
production-safe, and easy to scan under pressure. It is not a playful product.
It is a work surface for employees who need clarity, hierarchy, and trust.

## Colors

The palette is built around deep charcoal backgrounds, quiet borders, and a single
cool accent for primary actions.

- **Primary (#08090A):** Main application background.
- **Surface (#131416):** Cards, containers, and elevated modules.
- **Accent (#7170FF):** Primary actions and key interactive emphasis.
- **Text (#F7F8F8):** High-contrast content on dark surfaces.
- **Muted (#8A8F98):** Secondary metadata, timestamps, helper text.

Use success, warning, and danger colors sparingly and only for real state meaning.

## Typography

Typography should stay compact, crisp, and highly legible.

- Inter is the default family for headings, body text, and labels.
- Headings use tight tracking and strong weight.
- Labels use uppercase sparingly for system metadata and section markers.
- Avoid decorative type choices or oversized marketing-style headlines.

## Layout

Layout should prioritize scan speed and error prevention.

- Keep cards and forms aligned to a stable grid.
- Allow controls to wrap cleanly on laptop, tablet, and mobile.
- Prevent horizontal overflow at every viewport.
- Long filenames, workflow names, URLs, and API key labels must wrap or clamp gracefully.

## Elevation & Depth

Depth should be subtle.

- Use soft card separation rather than glossy effects.
- Prefer border contrast and small shadow depth over bright gradients.
- Keep visual emphasis on content hierarchy, not decoration.

## Shapes

Rounded corners should feel modern but restrained.

- Small controls: 10px
- Standard controls and pills: 12px
- Cards and major containers: 18px

Avoid overly soft, playful rounding.

## Components

- **Header:** compact, minimal, never crowded on mobile.
- **Project cards:** summary first, detailed file rows second.
- **File rows:** filenames must remain understandable even when long.
- **Analytics charts:** labels must reduce gracefully on small screens.
- **Settings rows:** metadata blocks must stack cleanly on mobile.
- **Fixer forms:** titles, descriptions, and selects must never force horizontal scrolling.

## Do's and Don'ts

### Do
- Preserve a professional, operator-first feel.
- Keep actions obvious and labels plain-English.
- Use spacing to reduce cognitive load.
- Prefer calm defaults and strong readability.

### Don't
- Don’t add unnecessary emoji or novelty styling.
- Don’t let metadata overwhelm primary actions.
- Don’t rely on horizontal scrolling for core workflows.
- Don’t hide important meaning behind weak contrast or tiny labels.
