---
name: MARP Slides Generator
source: https://github.com/robonuggets/marp-slides
category: Design Systems
purpose: Generate beautiful Marp presentation decks with SVG charts, custom CSS themes, and structured slide layouts from any topic
when_to_use: When creating slide decks for talks, pitches, internal presentations, or technical documentation presentations
tags: [presentations, slides, marp, svg, markdown, charts]
---
# MARP Slides Skill

## Purpose
Turns any topic or outline into a polished Marp presentation with custom CSS themes, SVG charts, and structured slide layouts.

## When To Use
- Creating talk slides
- Pitch decks
- Technical presentations
- Training material decks
- Status update slideshows

## What It Generates
- Complete `.md` Marp file with frontmatter
- Custom CSS theme block in the deck
- SVG charts and diagrams inline
- Speaker notes per slide
- Slide layouts: title, content, two-column, image-left, full-screen, quote

## 22 Example Decks Available
In `examples/` folder — covering: technical talks, product demos, architecture reviews, quarterly updates, onboarding decks, data stories.

## Export
```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Export to PDF
marp deck.md --pdf

# Export to PPTX
marp deck.md --pptx

# Export to HTML (self-contained)
marp deck.md --html
```

## How To Apply
```
"Create a 12-slide Marp deck about: [topic]"
"Build a pitch deck for [product] with [charts]"
"Turn these bullet points into a Marp presentation"
```

## Integration Notes
- Include `slide_count`, `theme`, `audience`, and `key_charts` for best results
- SVG charts are hand-authored for maximum quality (no lib dependencies)
- Pairs with `engineering-figure-banana` for complex academic figures
