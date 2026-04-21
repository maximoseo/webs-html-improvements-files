# SKILL: Animated Icons (CSS-Only)
**Source:** https://github.com/gorkem-bwl/animated-icons
**Domain:** design
**Trigger:** When adding animated icons, icon hover effects, or CSS icon animations to web UIs

## Summary
A curated collection of CSS-only animated icons and interactive icon hover effects. No JavaScript, no dependencies — pure CSS animations for common UI icons. Drop in ready-to-use classes.

## Key Patterns
- **CSS-only**: No JS dependencies, works in any framework or plain HTML
- **Hover-triggered**: Most animations activate on `:hover` for interactive feel
- **Common icons**: Menu/hamburger, search, close/X, arrows, loading spinners, checkmarks, notifications
- **Animation types**: Spin, pulse, morph (hamburger → X), bounce, shake, draw (SVG stroke)
- **Performance**: Uses `transform` and `opacity` only — compositor-layer animations, no layout thrash
- **Customizable**: CSS custom properties for color, size, animation duration

## Usage
Copy the CSS class or import the stylesheet, then add the class to any icon element.

## Code/Template
```css
/* Hamburger → X morph on hover */
.icon-menu { width: 24px; height: 18px; position: relative; cursor: pointer; }
.icon-menu span {
  display: block; height: 2px; background: currentColor;
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.icon-menu:hover span:nth-child(1) { transform: translateY(8px) rotate(45deg); }
.icon-menu:hover span:nth-child(2) { opacity: 0; }
.icon-menu:hover span:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

/* CSS spinner */
.icon-spin {
  width: 24px; height: 24px; border: 2px solid currentColor;
  border-top-color: transparent; border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* SVG stroke draw animation */
.icon-check path {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  transition: stroke-dashoffset 0.5s ease;
}
.icon-check:hover path { stroke-dashoffset: 0; }

/* Notification shake */
.icon-bell:hover { animation: shake 0.5s ease; }
@keyframes shake {
  0%, 100% { transform: rotate(0); }
  25% { transform: rotate(-15deg); }
  75% { transform: rotate(15deg); }
}
```
