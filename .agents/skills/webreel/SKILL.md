# SKILL: WebReel (Scripted Browser Video)
**Source:** https://github.com/vercel-labs/webreel
**Domain:** design
**Trigger:** When recording UI demos, product walkthroughs, or scripted browser interactions as MP4/GIF/WebM videos

## Summary
Records scripted browser videos as MP4 files with sound effects, cursor animation, and keystroke overlays. Define steps in JSON config (clicks, key presses, drags, pauses) and webreel drives headless Chrome, captures screenshots at ~60fps, and encodes with ffmpeg.

## Key Patterns
- **JSON-driven scripts**: Define steps declaratively — click, type, drag, scroll, pause, screenshot
- **Cursor animation**: Smooth cursor movement between interactions with easing
- **Keystroke HUD overlay**: Visual display of keyboard shortcuts pressed
- **Multiple output formats**: MP4 (default), WebM (VP9), GIF with frame-rate and loop control
- **Mobile viewport**: Record at any dimension (360×780 for mobile, 1080×1080 for square)
- **Shared steps**: `include` directive reuses setup sequences (e.g., dismiss cookie banner)
- **Multi-video configs**: Define multiple videos in one config file
- **Screenshots**: Capture PNG screenshots at specific steps alongside video
- **Auto-install**: Chrome and ffmpeg downloaded automatically on first use to `~/.webreel`

## Usage
```bash
npm install webreel
npx webreel init --name my-video --url https://example.com
npx webreel record
```

## Code/Template
```json
{
  "$schema": "https://webreel.dev/schema/v1.json",
  "videos": {
    "product-demo": {
      "url": "https://myapp.com",
      "viewport": { "width": 1280, "height": 720 },
      "defaultDelay": 500,
      "output": { "format": "mp4", "fps": 60 },
      "cursor": { "style": "macos", "smoothing": true },
      "keystrokes": { "show": true, "position": "bottom-right" },
      "steps": [
        { "type": "click", "selector": "#login-btn" },
        { "type": "type", "selector": "#email", "text": "user@example.com" },
        { "type": "type", "selector": "#password", "text": "secret", "masked": true },
        { "type": "click", "selector": "[data-testid='submit']" },
        { "type": "pause", "duration": 1000 },
        { "type": "scroll", "direction": "down", "amount": 500 },
        { "type": "screenshot", "name": "dashboard-loaded" },
        { "type": "drag", "from": "#card-1", "to": "#column-2" },
        { "type": "keypress", "keys": ["Meta", "k"] }
      ]
    }
  }
}
```
