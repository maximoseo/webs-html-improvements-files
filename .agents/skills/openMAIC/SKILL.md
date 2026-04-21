# SKILL: OpenMAIC — Multi-Agent Interactive Classroom
**Source:** https://github.com/THU-MAIC/OpenMAIC
**Domain:** code
**Trigger:** When building AI-powered educational experiences with multi-agent orchestration, slides, quizzes, and simulations

## Summary
Turns any topic or document into an interactive classroom with AI teachers and AI classmates. Generates slides, quizzes, interactive HTML simulations, PBL activities. OpenClaw integration for messaging apps. Built on LangGraph, Next.js 16, React 19.

## Key Patterns
- One-click lesson generation from topic/document → slides + quizzes + simulations
- Whiteboard drawing + TTS for AI teachers
- Export: .pptx or interactive .html
- OpenClaw integration: `clawhub install openmaic` then "teach me X"

## Usage
Use for AI tutoring apps, educational content generation, or interactive learning platforms.

## Code/Template
```bash
git clone https://github.com/THU-MAIC/OpenMAIC && cd OpenMAIC
cp .env.example .env    # add LLM API keys
pnpm install && pnpm dev    # http://localhost:3000

# Via OpenClaw:
clawhub install openmaic
# Tell agent: "teach me quantum physics"

# Deploy to Vercel:
# vercel deploy (one-click button in README)
```
