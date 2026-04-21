# SKILL: React Kino (Cinematic Scroll Animation)
**Source:** https://github.com/btahir/react-kino
**Domain:** design
**Trigger:** When adding cinematic scroll-driven storytelling, parallax, pinned scenes, reveal animations, or Apple-style product launch pages to React apps

## Summary
Cinematic scroll-driven storytelling for React. Core scroll engine under 1 KB gzipped. Declarative components compose scroll experiences with pinned scenes, fade/scale/slide reveals, counters, parallax, sticky headers, marquees, and text reveals — all SSR-safe.

## Key Patterns
- **Ultra-tiny**: Core engine <1 KB gzipped vs GSAP ScrollTrigger at 33 KB
- **Declarative API**: `<Scene>`, `<Reveal>`, `<ScrollTransform>`, `<Parallax>`, `<Counter>`, `<StickyHeader>`, `<Marquee>`, `<TextReveal>`
- **`<Scene duration="300vh">`**: Pins content in viewport; progress 0→1 as user scrolls through spacer
- **`<Reveal animation="fade-up|scale|fade" at={0.3}>`**: Triggers reveal at scroll progress point
- **`<Counter from={0} to={10000} format={...}>`**: Animated counter on scroll
- **SSR-safe**: Renders children on server, animates on client
- **3 pre-built templates**: ProductLaunch (Apple-style), CaseStudy, Portfolio
- **CLI scaffolding**: `npx @react-kino/cli init` for quick page scaffolding

## Usage
```bash
npm install react-kino
# Optional templates:
npm install @react-kino/templates
```

Wrap page in `<Kino>`, then compose `<Scene>` blocks with reveal animations.

## Code/Template
```tsx
import { Kino, Scene, Reveal, Counter, Parallax } from "react-kino";

function HeroSection() {
  return (
    <Kino>
      <Scene duration="300vh">
        {(progress) => (
          <div style={{ height: "100vh", display: "grid", placeItems: "center" }}>
            <Reveal animation="fade-up" at={0}>
              <h1>Your Product</h1>
            </Reveal>
            <Reveal animation="scale" at={0.3}>
              <Counter from={0} to={50000} format={(n) => `${n.toLocaleString()}+ users`} />
            </Reveal>
          </div>
        )}
      </Scene>
      <Parallax speed={0.3}>
        <img src="/hero-bg.jpg" />
      </Parallax>
    </Kino>
  );
}

// Pre-built template
import { ProductLaunch } from "@react-kino/templates/product-launch";
<ProductLaunch
  name="YourApp"
  tagline="The tagline that changes everything."
  accentColor="#dc2626"
  stats={[{ value: 10000, label: "Users", format: (n) => `${n.toLocaleString()}+` }]}
  features={[{ title: "Fast", description: "Under 1 KB core.", icon: "⚡" }]}
/>
```
