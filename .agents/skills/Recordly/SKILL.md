# SKILL: Recordly (Screen Recorder & Editor)
**Source:** https://github.com/webadderall/Recordly
**Domain:** design
**Trigger:** When creating polished screen recordings, product demos, walkthroughs, or tutorial videos with professional design quality

## Summary
An open-source desktop screen recorder and editor for macOS/Windows/Linux with motion-driven presentation tools built in. Handles auto-zooms, cursor polish, webcam overlays, timeline editing, styled frames, and export — all in one app. No motion designer needed.

## Key Patterns
- **Auto-zoom suggestions**: Based on cursor activity, emphasizes key moments automatically
- **Cursor controls**: Smoothing, motion blur, click bounce, sway, size adjustment, macOS-style assets
- **Frame styling**: Wallpapers, solid/gradient backgrounds, padding, rounded corners, drop shadows, aspect ratio presets
- **Webcam bubble**: Position presets, mirror, size, shadow, roundness, zoom-reactive scaling
- **Timeline editing**: Drag-and-drop zooms, trim, speed regions (fast/slow), text/image/figure annotations, extra audio regions
- **Export**: MP4/GIF (frame-rate + loop + size presets), aspect ratio and output dimension controls
- **Extension marketplace**: Community plugins for cursor sounds, device frames, browser mockups, wallpapers
- **Project files**: Save/reopen `.recordly` project files with full editor state

## Usage
Download from recordly.dev. Record → Jump to editor → Polish → Export.

Use when creating:
- SaaS product demos with professional polish
- Developer tool documentation walkthroughs
- Tutorial videos with cursor emphasis
- Marketing videos with branded frames

## Code/Template
```
Cursor settings for clean demos:
- Enable cursor smoothing (reduces jittery movement)
- Set cursor size: 1.5x default
- Enable click bounce (visual click feedback)
- Use macOS-style cursor assets for consistent look
- Enable cursor loop mode for looping GIFs

Frame settings for professional look:
- Background: gradient or wallpaper
- Padding: 40-80px
- Corner radius: 12-16px
- Drop shadow: medium

Export settings:
- Product demos: MP4, 60fps, high quality
- Documentation: GIF, 15fps, medium quality, 800px preset
- Social: 1:1 or 16:9 aspect ratio

Zoom workflow:
1. Record normally
2. Let auto-zoom suggest emphasis points
3. Review and adjust in timeline
4. Add manual zooms for key moments
```
