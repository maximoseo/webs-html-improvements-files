---
name: Seedance Video Generator
source: https://github.com/robonuggets/seedance-skill
category: Tools
purpose: Generate cinematic liquid glass motion graphics promo videos from app screenshots using ByteDance Seedance 2.0 via Fal AI
when_to_use: When creating promo videos, motion graphics ads, or abstract motion identity sequences from app screenshots
tags: [video-generation, motion-graphics, liquid-glass, fal-ai, seedance, promo-video]
---

# Seedance Video Generator

## Purpose
Turns any app into a cinematic motion graphics promo video. Screenshots → Apple-keynote-quality clips using ByteDance Seedance 2.0 on Fal AI.

## When To Use
- Screenshot a SaaS dashboard → 10-second liquid glass promo video
- Scrape App Store screenshots → motion graphics ad for any iOS app
- Text prompt → abstract motion identity sequence
- Creating marketing videos without a video production team

## How To Apply
**Setup:**
```bash
echo "FAL_KEY=your-fal-ai-key" >> .env
```

**Trigger:** "Generate a liquid glass motion graphics promo for https://linear.app"

**4 prompt patterns:**
1. **Liquid Glass** (default): translucent UI panels with reflections, light refractions, depth
2. **Floating Desktop**: MacBook/iPad product shots in black void
3. **Glass UI Ad**: close-ups on glass interactions
4. **Abstract Motion Identity**: timestamped sequences with geometric transformations

**Golden rules:**
1. NEVER describe logos in prompts — pass actual logo image as reference, overlay in post
2. Default to Pro tier (only 25% more than Fast, noticeably better)
3. Use temp JSON files for API calls — shell escaping breaks curl
4. No text in video — overlay text/logos in post-production
5. Max 5 reference images (quality degrades above 5)

**Sweet spot:** 5 refs + 10 seconds = $3.03 (Pro 720p)
**Budget test:** 3 refs + 4 seconds = $1.21

## Examples
- "Generate a 10-second promo for this dashboard" + 5 screenshots → liquid glass 720p video
- "Create a minimal motion identity sequence for my startup" → abstract motion identity pattern

## Integration Notes
- Fal AI API key required (fal.ai)
- Pro tier: $0.30/sec at 720p; Fast: $0.24/sec
- 1 reference image per 2 seconds = golden ratio for quality
