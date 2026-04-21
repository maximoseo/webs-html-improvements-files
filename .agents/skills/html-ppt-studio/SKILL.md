---
name: HTML PPT Studio
source: https://github.com/lewislulu/html-ppt-skill
category: Tools
purpose: World-class AgentSkill for producing professional HTML presentations — 36 themes, 15 full-deck templates, 31 page layouts, 47 animations (27 CSS + 20 canvas FX), presenter mode
when_to_use: When creating any presentation, pitch deck, data dashboard, product showcase, weekly report, or educational slide deck
tags: [presentations, html, slides, themes, animations, presenter-mode, css-animations]
---

# HTML PPT Studio

## Purpose
Pure static HTML/CSS/JS presentation system. No build step. 36 themes × 31 layouts × 47 animations = professional deck output. Includes real presenter mode (S key) with 4 magnetic cards.

## When To Use
- "做一份 8 页的技术分享 slides，用 cyberpunk 主题"
- "Turn this outline into a pitch deck"
- "Build a fitness dashboard presentation from this CSV"
- Creating XiaoHongShu image posts (9 slides, 3:4 ratio)

## How To Apply
**Install:** `npx skills add https://github.com/lewislulu/html-ppt-skill`

**36 themes include:** minimal-white, cyberpunk-neon, tokyo-night, glassmorphism, bauhaus, swiss-grid, neo-brutalism, xiaohongshu-white, vaporwave, and 27 more

**31 layouts:** cover, toc, bullets, two-column, big-quote, stat-highlight, kpi-grid, table, code, flow-diagram, timeline, roadmap, comparison, gantt, arch-diagram, cta, etc.

**47 animations:** 27 CSS (rise-in, zoom-pop, glitch-in, typewriter, neon-glow) + 20 Canvas FX (particle-burst, confetti-cannon, matrix-rain, knowledge-graph physics, neural-net pulses)

**15 full-deck templates:** pitch-deck, product-launch, tech-sharing, weekly-report, xhs-post, presenter-mode-reveal, hermes-cyber-terminal, obsidian-claude-gradient, etc.

**Presenter mode (S key):** current slide, next slide preview, speaker script (150-300 words), timer — all synced via BroadcastChannel

**Export:** `npx @marp-team/marp-cli slides.md --pdf --allow-local-files`

## Examples
- "Create a cyberpunk-themed 8-slide tech talk" → cyberpunk-neon theme + tech-sharing template
- "Build a venture pitch deck with KPI metrics and charts" → pitch-deck template + stat-highlight + chart-bar layouts

## Integration Notes
- Token-driven: swap one CSS link to reskin entire deck
- Iframe isolation for previews — guaranteed visual consistency
- Chinese + English first-class (Noto Sans SC / Noto Serif SC)
- Keyboard: ← → Space navigate, S presenter, O overview grid, T cycle themes
