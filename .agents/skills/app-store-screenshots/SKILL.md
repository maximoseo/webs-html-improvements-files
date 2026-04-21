# SKILL: App Store Screenshots Generator
**Source:** https://github.com/ParthJadhav/app-store-screenshots
**Domain:** marketing
**Trigger:** Use when generating production-ready App Store or Google Play marketing screenshots for iOS or Android apps, including all required resolutions and localized sets.

## Summary
A coding agent skill that scaffolds a Next.js project and generates advertisement-style screenshots for App Store and Google Play at all required resolutions. Supports iPhone mockups, CSS Android frames, RTL layouts, multi-locale sets, and reusable theme presets.

## Key Patterns
- Ask about app brand, features, style, number of slides before building
- Design as advertisements, not UI showcases — benefits over features
- Write compelling copy using proven App Store copywriting patterns
- Export PNGs at all required Apple and Google sizes
- Support locale-based screenshot sets and RTL-aware layouts
- Reusable theme presets for quick art direction swaps

## Usage
When user needs App Store or Google Play screenshots. Ask: app description (1 sentence), top 3-5 features, visual style, number of slides, languages needed.

## Code/Template
```bash
# Install
npx skills add ParthJadhav/app-store-screenshots

# Scaffold structure
project/
├── public/mockup.png           # iPhone frame
├── public/screenshots/         # iOS output
│   └── android/               # Android output
└── src/slides/                # Slide components
```

Example prompt:
```
Build App Store screenshots for my habit tracker.
Clean/minimal style, warm neutrals, calm premium feel. 6 slides.
```
