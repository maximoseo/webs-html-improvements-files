# SKILL: FontTrio (Font Pairings for shadcn/ui)
**Source:** https://github.com/kapishdima/fonttrio
**Domain:** design
**Trigger:** When choosing font pairings for shadcn/ui projects, or when improving typography in Tailwind/Next.js apps

## Summary
Curated font trio pairings optimized for shadcn/ui design system. Each trio consists of a display font, a body font, and a mono font — tested for visual harmony and readability in modern SaaS UIs built with Tailwind CSS.

## Key Patterns
- **Three-font system**: Display (headings/hero), Body (prose/labels), Mono (code/data)
- **shadcn/ui optimized**: Each trio tested against shadcn component library
- **Next.js font loading**: Uses `next/font/google` for optimal performance
- **CSS custom property integration**: Sets `--font-sans`, `--font-display`, `--font-mono`
- **Curated pairings**: Avoids generic defaults (Inter/Roboto/Open Sans) in favor of distinctive choices

## Usage
Pick a trio → install fonts via next/font or Google Fonts → apply CSS variables to Tailwind config.

## Code/Template
```tsx
// Next.js font setup with shadcn/ui
import { GeistSans } from 'geist/font/sans';
import { GeistMono } from 'geist/font/mono';
import localFont from 'next/font/local';

// Example trio: Cal Sans + Geist + Geist Mono
const calSans = localFont({
  src: '../fonts/CalSans-SemiBold.woff2',
  variable: '--font-display',
});

export default function RootLayout({ children }) {
  return (
    <html className={`${calSans.variable} ${GeistSans.variable} ${GeistMono.variable}`}>
      <body className="font-sans">{children}</body>
    </html>
  );
}
```
```css
/* globals.css — wire fonts into shadcn/ui tokens */
:root {
  --font-sans: var(--font-geist-sans), ui-sans-serif, system-ui;
  --font-display: var(--font-cal-sans), var(--font-geist-sans);
  --font-mono: var(--font-geist-mono), ui-monospace;
}
```
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-sans)'],
        display: ['var(--font-display)'],
        mono: ['var(--font-mono)'],
      }
    }
  }
}
```
