# SKILL: Notchy — Claude Code in macOS Notch
**Source:** https://github.com/adamlyttleapps/notchy
**Domain:** developer-tools
**Trigger:** Use when integrating Claude Code sessions into the macOS MacBook notch, running multiple Claude sessions with Xcode project auto-detection, or building notch-aware macOS apps with SwiftTerm.

## Summary
Notchy is a macOS menu bar app that reveals a floating Claude Code terminal panel by hovering over the MacBook notch. Supports multi-session tabs, Xcode project auto-detection, live status in notch, and Cmd+S git checkpoints.

## Key Patterns
- Hover notch or click menu bar to open Claude Code terminal panel
- Auto-detects open Xcode projects and `cd`s into them
- Multi-session tabs for parallel Claude Code sessions
- Animated pill in notch: working / waiting / done states
- Cmd+S = git checkpoint snapshot before agent changes
- Built with SwiftTerm (terminal emulator) via SPM
- Requires macOS 26.0+ and MacBook with notch

## Usage
When user wants a seamless Claude Code workflow on MacBook — especially for iOS/macOS development with automatic Xcode project context.

## Code/Template
```bash
# Build
xcodebuild -project Notchy.xcodeproj -scheme Notchy -configuration Debug build

# Dependencies (Swift Package Manager)
# SwiftTerm: https://github.com/migueldeicaza/SwiftTerm
```
