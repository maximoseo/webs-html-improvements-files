---
name: ui-design-brain
description: Generate production-grade UI using real component patterns and best practices from 60+ documented interface components. Use when the user asks to build web interfaces, pages, dashboards, forms, navigation, or any UI — ensures modern, minimal, SaaS-quality output grounded in design system conventions rather than generic AI patterns.
license: MIT
---

# SKILL: UI Design Brain
**Source:** https://github.com/carmahhawwari/ui-design-brain
**Domain:** design
**Trigger:** When building web UI, pages, dashboards, forms, navigation — any interface component

## Summary
A Cursor/Claude skill providing curated knowledge of 60+ UI component patterns sourced from component.gallery. Replaces AI guessing with real design-system knowledge: best practices, layout patterns, aliases, and explicit anti-patterns for each component.

## Key Patterns
- **60 components covered**: Accordion, Alert, Avatar, Badge, Breadcrumbs, Button, Card, Carousel, Checkbox, Combobox, Datepicker, Drawer, Dropdown, Empty State, Form, Header, Hero, Modal, Navigation, Pagination, Popover, Progress, Radio, Rating, Search, Select, Slider, Spinner, Table, Tabs, Toast, Toggle, Tooltip, Tree View...
- **5 design presets**: Modern SaaS (default), Apple-level Minimal, Enterprise/Corporate, Creative/Portfolio, Data Dashboard
- **Core principle**: Restraint > decoration; typography carries hierarchy; one strong color accent; 8px grid
- **Anti-patterns**: No purple-on-white gradients, no Inter/Roboto defaults, no evenly-spaced card grids
- Always provide: empty states, loading states, error states, accessible focus indicators

## Usage
Install: `git clone https://github.com/carmahhawwari/ui-design-brain.git ~/.cursor/skills/ui-design-brain`

Activates automatically when building UI. Workflow:
1. Identify components needed from user request
2. Look up best practices per component in components.md
3. Choose design direction (Modern SaaS is default)
4. Generate production-ready code following patterns

## Code/Template
```
Buttons: verb-first labels ("Save changes"), one primary per section, 44px min touch target
Modals: always X + Cancel + Escape; trap focus; return focus on close
Toasts: auto-dismiss 4-6s, allow manual dismiss, newest on top
Forms: single-column, labels above inputs, placeholder as format hint only
Tables: fixed-width slots for icons/actions, consistent vertical lanes
Loading: skeleton screens preferred over spinners (show after 300ms delay)
Validation: inline on blur, not on every keystroke
```
