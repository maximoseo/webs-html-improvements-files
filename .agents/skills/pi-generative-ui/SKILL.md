# SKILL: Pi Generative UI
**Source:** https://github.com/Michaelliv/pi-generative-ui
**Domain:** design
**Trigger:** When implementing generative UI, streaming HTML widgets, or reproducing Claude.ai's visual rendering system in custom agents

## Summary
A reverse-engineered implementation of Claude.ai's generative UI system for the `pi` agent framework. Ask the AI to visualize anything and get a live interactive widget (sliders, charts, animations) streaming into a native macOS window token-by-token via morphdom DOM diffing.

## Key Patterns
- **5 design modules** extracted verbatim from claude.ai (72K total, loaded on demand):
  - `interactive` (19KB): Sliders, metric cards, live calculations
  - `chart` (22KB): Chart.js setup, custom legends, number formatting
  - `mockup` (19KB): UI component tokens, cards, forms, skeleton loading
  - `art` (17KB): SVG illustration, Canvas animation, creative patterns
  - `diagram` (59KB): Flowcharts, architecture diagrams, SVG arrow systems
- **Streaming architecture**: `toolcall_start` → `toolcall_delta` (150ms debounce + morphdom diff) → `toolcall_end` (execute scripts)
- **morphdom DOM diffing**: Only changed nodes update; new nodes fade in with 0.3s animation
- **Dark mode by default**: `#1a1a1a` background, designed for macOS WKWebView
- **Progressive disclosure**: Only name/description loaded at startup (~100 tokens); modules pulled on demand
- **Bidirectional bridge**: `window.glimpse.send(data)` sends data back to agent

## Usage
Triggers when user asks to visualize, create a dashboard, draw a diagram, or animate data.

LLM workflow:
1. Calls `visualize_read_me` → loads relevant design module
2. Calls `show_widget` → generates HTML fragment as tool call parameter
3. Extension intercepts stream → opens native window → morphdom diffs as tokens arrive

## Code/Template
```ts
// Streaming interception pattern
on('toolcall_start', ({ name }) => {
  if (name === 'show_widget') initStreaming();
});
on('toolcall_delta', debounce(({ arguments: args }) => {
  const html = parseStreamingJson(args)?.html ?? '';
  openWindowIfNeeded();
  morphdom(container, `<div>${html}</div>`, { childrenOnly: true });
}, 150));
on('toolcall_end', () => executeScripts(container));
```
```html
<!-- Widget output example (dark mode, Chart.js) -->
<div style="background:#1a1a1a;color:#fff;padding:24px;border-radius:12px">
  <h2 style="font-size:20px;margin-bottom:16px">Compound Interest</h2>
  <canvas id="chart" width="500" height="300"></canvas>
  <input type="range" min="1" max="20" value="10" oninput="updateChart(this.value)">
</div>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>/* chart initialization */</script>
```
