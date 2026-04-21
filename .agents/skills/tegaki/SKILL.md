# SKILL: Tegaki (Handwriting Animation)
**Source:** https://github.com/KurtGokhan/tegaki
**Domain:** design
**Trigger:** When adding handwriting animation, text drawing effect, stroke-by-stroke reveal, or calligraphic animation to any web app

## Summary
Tegaki (手書き) turns any font into animated handwriting — text draws itself stroke by stroke with natural timing. No manual path authoring, no native dependencies; works with React, Svelte, Vue, SolidJS, Astro, Web Components, and vanilla JS.

## Key Patterns
- **Zero manual work**: Just pick a font; library extracts stroke paths automatically
- **Cross-framework**: Single API across React, Svelte, Vue, SolidJS, Astro, Web Components
- **4 built-in fonts**: Caveat, Italianno, Tangerine, Parisienne
- **Custom fonts**: Interactive generator at gkurt.com/tegaki/generator/
- **Natural timing**: Stroke-by-stroke with variable speed for organic feel
- **Lightweight**: No native dependencies, pure TypeScript

## Usage
```bash
npm install tegaki
```

Use `TegakiRenderer` from framework-specific import. Works server-side (SSR-safe).

## Code/Template
```tsx
// React
import { TegakiRenderer } from 'tegaki/react';
import caveat from 'tegaki/fonts/caveat';

function App() {
  return (
    <TegakiRenderer font={caveat} style={{ fontSize: '48px' }}>
      Hello World
    </TegakiRenderer>
  );
}
```
```svelte
<!-- Svelte -->
<script>
  import { TegakiRenderer } from 'tegaki/svelte';
  import italianno from 'tegaki/fonts/italianno';
</script>
<TegakiRenderer font={italianno} style="font-size: 64px">Welcome</TegakiRenderer>
```
```ts
// Vanilla JS
import { TegakiEngine } from 'tegaki/core';
const engine = new TegakiEngine({ font: caveat, container: document.getElementById('text') });
engine.write('Hello');
```
