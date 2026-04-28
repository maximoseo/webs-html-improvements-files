# SKILL: CYCLE - macOS Pomodoro Work/Rest Timer
**Source:** https://github.com/saint-angels/CYCLE
**Domain:** code
**Trigger:** When building macOS menu bar productivity timers or work/rest cycle enforcement apps

## Summary
macOS pomodoro-style timer that tracks work time and escalates rest reminders after 25 minutes. Stays visible during rest mode, auto-switches back to work on input detection. Built with Swift for macOS 14+.

## Key Patterns
- Work time tracking with escalating rest nudges
- Input detection for automatic work mode resumption
- Unsigned app distribution (bypasses Apple Developer requirement)
- Minimal SwiftUI timer app structure

## Usage
Download Cycle.zip from Releases, drag to /Applications. Build from source: `swift build && .build/debug/Tracker`. Requires macOS 14+.

## Code/Template
```bash
# Build from source
swift build
.build/debug/Tracker
```
