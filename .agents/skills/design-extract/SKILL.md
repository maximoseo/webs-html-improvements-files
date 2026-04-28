# SKILL: Designlang (Design Language Extractor)
**Source:** https://github.com/Manavarya09/design-extract
**Domain:** design
**Trigger:** When extracting design systems from websites, reverse-engineering design tokens, cloning visual style, generating Tailwind/shadcn/Figma configs from live sites

## Summary
`designlang` crawls any website with a headless browser, extracts computed styles from the live DOM, and generates 8 output files: AI-optimized markdown, HTML preview, Tailwind config, React theme, shadcn/ui CSS, Figma variables, W3C design tokens, and CSS custom properties. Also captures layout patterns, responsive behavior, interaction states, and WCAG accessibility scores.

## Key Patterns
- **8 output files**: design-language.md, preview.html, design-tokens.json, tailwind.config.js, variables.css, figma-variables.json, theme.js, shadcn-theme.css
- **19 markdown sections**: Color, Typography, Spacing, Border Radii, Shadows, CSS vars, Breakpoints, Transitions, Component Patterns, Layout System, Responsive Design, Interaction States, Accessibility (WCAG 2.1), Gradients, Z-Index Map, SVG Icons, Font Files, Image Style, Quick Start
- **Layout extraction**: Grid patterns, flex direction, container widths, gap values (not just colors/fonts)
- **Responsive capture**: 4 viewports (375/768/1280/wide) — maps exactly what changes between breakpoints
- **Interaction states**: Programmatically hovers/focuses elements, captures hover/focus CSS transitions
- **Live sync**: `designlang sync` treats deployed site as source of truth, detects design drift
- **Agent rules**: `--emit-agent-rules` generates .cursor/, .claude/, CLAUDE.md.fragment, agents.md
- **Platform output**: `--platforms ios,android,flutter,wordpress-theme`

## Usage
```bash
npx designlang https://stripe.com           # Basic extract
npx designlang https://stripe.com --full    # All 8 outputs
npx designlang https://vercel.com --responsive   # Multi-breakpoint capture
npx designlang https://stripe.com --interactions # Hover/focus states
designlang sync https://stripe.com --out ./src/tokens  # Live sync
```

As agent skill: `npx skills add Manavarya09/design-extract`

## Code/Template
```js
// Generated tailwind.config.js
module.exports = {
  theme: {
    colors: {
      primary: '#635BFF',  // Stripe violet
      background: '#FFFFFF',
      text: { DEFAULT: '#0A2540', muted: '#425466' }
    },
    fontFamily: { sans: ['Sohne', 'ui-sans-serif'] },
    spacing: { xs: '4px', sm: '8px', md: '16px', lg: '24px', xl: '48px' }
  }
}
```
```css
/* Generated variables.css */
:root {
  --color-primary: #635BFF;
  --radius-md: 6px;
  --shadow-card: 0 2px 8px rgba(0,0,0,0.08);
  --font-display: 'Sohne', sans-serif;
  --transition-fast: 150ms ease-out;
}
```
