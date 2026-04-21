---
name: MiniMax Skills Suite
source: https://github.com/MiniMax-AI/skills
category: Coding
purpose: 17 development skills covering frontend, fullstack, Android, iOS, Flutter, React Native, shaders, PDF/PPTX/XLSX/DOCX generation, vision analysis, and multimodal content (TTS, music, video, image)
when_to_use: When generating rich media, building cross-platform apps, creating documents, or producing multimedia content via MiniMax APIs
tags: [minimax, frontend, android, ios, flutter, multimodal, pdf, video, music, tts, shaders]
---

# MiniMax Skills Suite

## Purpose
17 production skills powered by MiniMax APIs and official development frameworks. Covers the full spectrum from UI development to multimodal content generation.

## When To Use
- **frontend-dev**: React/Next.js + Tailwind with Framer Motion, GSAP, AI media assets via MiniMax API
- **fullstack-dev**: REST APIs, auth flows, real-time features, database integration
- **android-native-dev**: Kotlin/Jetpack Compose + Material Design 3
- **ios-application-dev**: UIKit, SnapKit, SwiftUI with Apple HIG compliance
- **flutter-dev**: Riverpod/Bloc, GoRouter, cross-platform patterns
- **shader-dev**: GLSL ray marching, SDF modeling, fluid simulation (ShaderToy-compatible)
- **minimax-multimodal-toolkit**: TTS, voice cloning, music, video, image generation via MiniMax APIs
- **gif-sticker-maker**: Convert photos to animated GIF stickers (Funko Pop style)
- **minimax-pdf / pptx-generator / minimax-xlsx / minimax-docx**: Professional document creation

## How To Apply
```bash
# Claude Code
claude plugin marketplace add https://github.com/MiniMax-AI/skills
claude plugin install minimax-skills
```

## Examples
- "Build a premium landing page with cinematic animations" → frontend-dev skill
- "Generate a TTS audio from this script with voice cloning" → minimax-multimodal-toolkit
- "Create a PDF report from this data" → minimax-pdf with 15 cover styles

## Integration Notes
- MiniMax API key required for multimodal features
- Document skills use OpenXML SDK (.NET) for DOCX; pandas + XML templates for XLSX
- Vision analysis supports fallback to OpenAI GPT-4V
