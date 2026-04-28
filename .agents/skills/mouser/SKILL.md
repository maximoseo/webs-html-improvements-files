# SKILL: Mouser — Logitech Mouse Remapper
**Source:** https://github.com/TomBadash/Mouser
**Domain:** developer-tools
**Trigger:** Use when setting up Logitech mouse button remapping, DPI configuration, per-app profiles, or replacing Logitech Options+ with an open-source, offline alternative.

## Summary
Mouser is a lightweight open-source, fully local alternative to Logitech Options+ for remapping Logitech HID++ mice. Supports button remapping, per-app profiles, DPI control, Smart Shift, gesture actions, and runs on Windows/macOS/Linux with zero telemetry.

## Key Patterns
- Per-application profiles that auto-switch on app focus
- 30+ built-in actions + custom keyboard shortcuts
- DPI slider 200–8000 with live HID++ sync
- Interactive MX Master diagram with clickable hotspot UI
- Cross-platform: Windows (WH_MOUSE_LL), macOS (CGEventTap), Linux (evdev/uinput)
- Config stored as local JSON — no cloud, no account

## Usage
When a user wants to remap Logitech mouse buttons without Logitech Options+, set up per-app profiles, or control DPI programmatically.

## Code/Template
No special install commands in README. Download from releases page and configure JSON:
```json
{
  "buttons": {
    "back": "Alt+Left",
    "forward": "Alt+Right",
    "gesture": "passthrough"
  },
  "dpi": 1600
}
```
