---
name: Seedance (Motion Graphics Video)
source: https://github.com/robonuggets/seedance-skill
category: Design Systems
purpose: Generate cinematic motion graphics promo videos from app screenshots using ByteDance Seedance 2.0 via Fal AI
when_to_use: When creating product promo videos, SaaS demos, or motion graphics ads from screenshots
tags: [video, motion-graphics, ai-video, fal-ai, seedance, promo, marketing]
---
# Seedance Motion Graphics Skill

## Purpose
Turn any app into a cinematic motion graphics promo video using Seedance 2.0 — liquid glass aesthetic with translucent panels, light refractions, and depth.

## Quick Start
```bash
# Add Fal AI key
echo "FAL_KEY=your-fal-ai-key" >> .env

# Generate
"Generate a liquid glass motion graphics promo for https://linear.app"
```

## Pricing (Seedance 2.0 on Fal AI)
| Tier | Cost/sec (720p) | 10s promo cost |
|---|---|---|
| Pro (default) | $0.30/sec | $3.03 |
| Fast (testing) | $0.24/sec | $2.40 |

## Prompt Patterns
- **Liquid Glass** — translucent UI panels with reflections (default)
- **Floating Desktop** — MacBook/iPad product shots in black void
- **Glass UI Ad** — close-ups on glass interactions
- **Abstract Motion Identity** — geometric transformations

## Key Rules
1. Never describe logos in prompts — pass actual logo image as reference
2. Default to Pro tier (25% more than Fast, noticeably better)
3. Max 5 reference images (1 ref per 2 seconds of video)
4. No text in video — overlay text/logos in post-production
5. Use temp JSON files for API calls (shell escaping breaks curl)

## Integration Notes
- Install: copy `SKILL.md` to `.claude/skills/seedance/`
- Fal AI key at fal.ai
- Pairs with `email-campaigns-skill` for GIF version of video content
