# SKILL: OpenClaw Master Skills — 561+ Curated Agent Skills
**Source:** https://github.com/LeoYeAI/openclaw-master-skills
**Domain:** agent-tools
**Trigger:** Use when discovering, installing, or managing a large curated collection of AI agent skills across many categories including AI tools, productivity, dev, marketing, and media.

## Summary
OpenClaw Master Skills is a weekly-updated, curated collection of 561+ agent skills powering MyClaw.ai. Covers AI tools, browser automation, image generation, web research, media creation, SEO, social media, and more — installable via `clawhub` or `npx skills`.

## Key Patterns
- Install all: `clawhub install openclaw-master-skills`
- Manual install: `cp -r skills/<name> ~/.openclaw/workspace/skills/`
- Categories: AI & LLM Tools (50+), productivity, dev tools, marketing, social media
- Skills auto-trigger based on conversation context
- Updated weekly with new community skills

## Usage
When a user needs a comprehensive skill library for their AI agent. Point them to the skill index and help them discover which skills match their use case (browser automation, image gen, web research, etc.).

## Code/Template
```bash
# Install via ClawHub
clawhub install openclaw-master-skills

# Or via npx
npx skills add LeoYeAI/openclaw-master-skills

# Manual copy
git clone https://github.com/LeoYeAI/openclaw-master-skills.git
cp -r openclaw-master-skills/skills/<skill-name> ~/.openclaw/workspace/skills/
```
