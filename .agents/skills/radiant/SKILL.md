# SKILL: Radiant — Open-Source Web Shaders & Visual Effects
**Source:** https://github.com/pbakaus/radiant
**Domain:** frontend-development
**Trigger:** Use when creating animated website backgrounds, hero section effects, particle systems, or drop-in canvas animations for web projects — zero dependencies, zero build step.

## Summary
Radiant is a library of 94 self-contained shader HTML files (Canvas 2D + WebGL) for website backgrounds, hero sections, presentations, and digital signage. Mouse/touch interactive, DPR-aware, 60fps targeting, controllable via postMessage at runtime.

## Key Patterns
- Embed as `<iframe src="shader.html" style="position:fixed;inset:0;...">` for full-screen background
- Control parameters via `postMessage({ type: 'param', name: 'ROTATION_SPEED', value: 0.6 })`
- 6 color schemes via CSS `filter` on iframe (no shader modification needed)
- Tags: fill, object, particles, physics, noise, organic, geometric
- Every shader: mouse/touch interaction, visibility-based pause, DPR-aware, 60fps

## Usage
When user wants stunning animated backgrounds or visual effects on a website. Embed as iframe, control via postMessage, swap colors via CSS filter.

## Code/Template
```html
<iframe
  src="event-horizon.html"
  style="position: fixed; inset: 0; width: 100%; height: 100%; border: 0; z-index: -1;"
></iframe>
<script>
  // Change color scheme
  iframe.style.filter = 'hue-rotate(175deg)'; // Blue scheme
  // Control parameters
  iframe.contentWindow.postMessage({ type: 'param', name: 'SPEED', value: 0.5 }, '*');
</script>
```
