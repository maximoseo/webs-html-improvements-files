---
name: Design-to-Code Renderer
description: Figma-to-code translation, JSON UI rendering, and Penpot workflows.
color: "#F59E0B"
emoji: 🎨
vibe: Pixel-perfect translation.
---

# Design-to-Code Renderer Skill

Synthesized from `vibeflowing-inc/vibe_figma`, `vercel-labs/json-render`, `penpot/penpot`, and `uiverse-io/galaxy`.

## 🧠 Core Capabilities
- **JSON UI Rendering:** Converts structured JSON data into accessible HTML/React components.
- **Vibe Translation:** Translates the "vibe" of a Figma/Penpot mockup into strict, semantic HTML/CSS without relying on absolute positioning traps.
- **Component Extraction:** Safely extracts hover states and micro-interactions from UI libraries (like Uiverse) into inline WordPress-safe styles.

## 🎯 When to Use
- When converting a mockup or wireframe into a functional HTML template.
- When a design system needs to be rendered dynamically from JSON payloads.

## 🚨 Anti-Patterns
- Do not generate absolute-positioned "spaghetti code". Always use Flexbox or CSS Grid.
