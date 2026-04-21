# SKILL: VideoZero Skills — Motion Canvas Animation
**Source:** https://github.com/VideoZero/skills
**Domain:** creative-tools
**Trigger:** Use when creating programmatic animations with Motion Canvas, building animated videos via code, or controlling the Motion Canvas editor via HTTP API.

## Summary
A skill collection for building animated videos with Motion Canvas (TypeScript-based animation framework). Provides framework reference documentation, agent HTTP API for editor control, and motion graphics fundamentals.

## Key Patterns
- `motion-canvas` skill: components, signals, refs, layout, transitions, filters, shaders
- `motion-canvas-agent` skill: HTTP API for seek, screenshot, scene graph, settings, rendering
- `motion-graphics-fundamentals`: 12 principles of animation and timing
- Install via `npx skills add videozero/skills`
- Docs at https://archive.canvascommons.io/

## Usage
When user wants to generate animated explainer videos, motion graphics, or programmatic animations using Motion Canvas. Use the agent HTTP API skill to control the editor from within an AI agent.

## Code/Template
```bash
npx skills add videozero/skills

# Available skills:
# motion-canvas           — framework reference
# motion-canvas-agent     — HTTP editor control API
# motion-graphics-fundamentals — 12 animation principles
```
